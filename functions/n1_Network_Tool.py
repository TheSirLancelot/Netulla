import socket
import ipaddress
import math
import subprocess
import re
import urllib.parse
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import nmap
import plotly.express as px
import dns.resolver
import dns.reversename


from ip2geotools.databases.noncommercial import (
    DbIpCity,
    InvalidRequestError,
    LimitExceededError,
)
from pythonping import ping
import whois


def ip_geolocation():
    # Function to get the public IP address using an external service
    def get_public_ip():
        try:
            # Using curl to fetch the IP address from ipify API, suppressing output
            result = subprocess.run(
                ["curl", "https://api.ipify.org"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return result.stdout.decode("utf-8").strip()
        except subprocess.SubprocessError:
            st.error("Failed to fetch the public IP address.")
            return None

    # Function to get the geolocation of an IP address
    @st.cache_resource
    def get_geolocation(ip_address):
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        response.raise_for_status()  # Ensure we got a valid response
        return response.json()

    st.markdown("# IP Geolocation")

    ip_address = get_public_ip()
    if ip_address:
        location = get_geolocation(ip_address)
        latitude = location["lat"]
        longitude = location["lon"]

        st.markdown(f"### Geolocation of IP: {ip_address}")
        st.markdown(f"**Latitude:** {latitude}")
        st.markdown(f"**Longitude:** {longitude}")

        # Display IP location on a map
        map_data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})
        layer = pdk.Layer(
            "ScatterplotLayer",
            map_data,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius=1000,
        )

        # Set the initial view
        view_state = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=12,
            pitch=50,
        )

        # Render the deck.gl map in the Streamlit app as a PyDeck chart
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.error("Failed to determine the IP address.")


def network_analysis():
    st.markdown("# Network Analysis")

    # Add separator
    st.markdown("---")

    # Move the ip_input to the sidebar
    ip_input = st.text_input("Enter IP address (e.g., 8.8.8.8, 45.33.32.156)")

    well_known_ports = st.checkbox("Scan only well-known ports")

    # Add separator
    st.markdown("---")

    # Add Execute button
    execute = st.button("Execute")

    # Set a boolean flag in the session state to indicate
    # whether the "Execute" button has been clicked
    if execute:
        st.session_state["executed"] = True
    if "executed" not in st.session_state:
        st.session_state["executed"] = False

    # Only show the description if the "Execute" button has not been clicked
    if not st.session_state["executed"]:
        st.markdown(
            """This tool provides information about the network related to the provided IP address. 
            It scans for open ports, the corresponding service for well-known ports, and 
            geographical information related to the IP. Please input an IP address and click 
            'Execute' to start the analysis.
            """
        )

    # Read port descriptions from file
    well_known_ports_dict = {}
    with open("functions/port_descriptions.txt", "r", encoding="utf-8") as file:
        for line in file:
            port, description = line.strip().split(",")
            well_known_ports_dict[int(port)] = description

    if execute and ip_input:
        try:
            # Validate the IP address
            ipaddress.ip_address(ip_input)

            # Attempt to find a hostname
            try:
                host_name = socket.gethostbyaddr(ip_input)[0]
            except socket.herror:
                host_name = "No hostname found"

            response = requests.get(f"http://ip-api.com/json/{ip_input}", timeout=5)
            response.raise_for_status()  # Ensure we got a valid response
            data = response.json()

            st.session_state["host_name"] = host_name
            st.session_state["ISP"] = data["isp"]
            st.session_state["Region"] = data["regionName"]
            st.session_state["City"] = data["city"]
            st.session_state["ZIP"] = data["zip"]

            # Use Nmap to get open ports
            scanner = nmap.PortScanner()
            ports_to_scan = (
                ",".join(map(str, well_known_ports_dict.keys()))
                if well_known_ports
                else "1-1024"
            )
            scanner.scan(ip_input, ports_to_scan)

            # Initialize ports DataFrame
            ports_data = []

            for port in scanner[ip_input]["tcp"].keys():
                status = scanner[ip_input]["tcp"][port]["state"]
                description = well_known_ports_dict.get(port, "N/A")
                ports_data.append(
                    {"Port": port, "Status": status, "Description": description}
                )

            st.session_state[
                "ports_data"
            ] = ports_data  # Store ports data in session state

        except ValueError:
            st.error("Invalid IP address.")
        except requests.exceptions.RequestException:
            st.error("Request failed.")
    # Display information if scan has been executed
    if "executed" in st.session_state and st.session_state["executed"]:
        st.write(f"Hostname: {st.session_state['host_name']}")
        st.write(f"ISP: {st.session_state['ISP']}")
        st.write(f"Region: {st.session_state['Region']}")
        st.write(f"City: {st.session_state['City']}")
        st.write(f"ZIP: {st.session_state['ZIP']}")

        # If scan has finished, allow user to filter ports
        if "ports_data" in st.session_state:
            ports_filter = st.checkbox("Show only open ports")

            # Update the ports_data if filter is applied
            if ports_filter:
                ports_data = [
                    data
                    for data in st.session_state["ports_data"]
                    if data["Status"] == "open"
                ]
            else:
                ports_data = st.session_state["ports_data"]

            ports_df = pd.DataFrame(ports_data)
            st.dataframe(
                ports_df.set_index("Port")
            )  # Display the data in a more interactive table


def subnet_calculator():
    st.markdown("# Subnet Calculator")

    ip_input = st.text_input("Enter IP address (e.g., 192.168.0.1)", "")
    cidr_input = st.number_input(
        "Enter CIDR (e.g., 24)", min_value=0, max_value=32, value=24
    )

    if ip_input and cidr_input:
        try:
            # Create network object
            network = ipaddress.IPv4Network(f"{ip_input}/{cidr_input}", strict=False)
            st.success("Valid IP address and CIDR")

            st.markdown("### Subnet Details")

            details = {
                "Total IPs": str(network.num_addresses),
                "Usable IPs": str(network.num_addresses - 2)
                if network.prefixlen != 32
                else "1",
                "Network Address": str(network.network_address),
                "Broadcast Address": str(network.broadcast_address),
                "Subnet Mask": str(network.netmask),
                "Wildcard Mask": str(network.hostmask),
                "Binary Subnet Mask": bin(int(network.netmask)),
            }

            # Converting the dictionary to a list of tuples
            details_list = list(details.items())
            # Creating the DataFrame
            df = pd.DataFrame(details_list, columns=["Information", "Value"])
            st.table(df.set_index("Information"))

            # Pie chart for the IP address allocation
            if network.prefixlen < 32:
                allocation = {
                    "Usable IP Range": network.num_addresses - 2,
                    "Network and Broadcast": 2,
                }

                df = pd.DataFrame(allocation.items(), columns=["Category", "Count"])
                fig = px.pie(
                    df, values="Count", names="Category", title="IP Allocation"
                )
                st.plotly_chart(fig)

        except ValueError:
            st.error("Invalid IP address or CIDR.")


def certificate_lookup():
    st.markdown("# Certificate Lookup")
    st.markdown(
        "The Certificate Lookup tool allows you to retrieve SSL "
        "certificate information for a given URL. Enter the URL "
        "in the format 'example.com' and click 'Get Certificate'."
    )

    url = st.text_input("Enter a Domain Name (e.g., google.com)", "example.com")
    if st.button("Get Certificate"):
        if url:
            try:
                # Run the 'openssl' command to fetch the SSL certificates
                openssl_command = f"openssl s_client -showcerts -connect\
                    {url}:443 < /dev/null 2>/dev/null | openssl x509 -noout -text"
                result = subprocess.run(
                    openssl_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    # Raise error on non-zero exit status
                    check=True,
                )

                if result.returncode == 0:
                    st.text(f"Certificate Information for {url}:")
                    st.text(result.stdout)
                else:
                    st.error(f"Failed to retrieve the certificate: {result.stderr}")

            except subprocess.CalledProcessError as e:
                # Handle errors from the subprocess itself
                st.error(f"Failed to retrieve the certificate: {e.stderr}")
            except subprocess.TimeoutExpired as e:
                # Handle a timeout error
                st.error(f"The command timed out: {e}")
            # except Exception as e:
            #    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a URL before clicking the button.")


def ns_lookup():
    st.markdown("# NS Lookup")

    # Ask for domain
    domain = st.text_input("Enter Domain (e.g., google.com)", "")

    # Check if the input is empty and display a message
    if not domain.strip():  # strip() removes leading/trailing whitespaces
        st.error("Please enter a domain.")
        return

    try:
        # Perform lookup
        ip_addresses = [ip.address for ip in dns.resolver.resolve(domain, "A")]

        # Perform reverse lookup
        reverse_name = dns.reversename.from_address(str(ip_addresses[0]))
        hostname = str(dns.resolver.resolve(reverse_name, "PTR")[0])

        # Display results
        st.success("Valid Domain")

        st.markdown("### Domain Details")

        st.markdown("**IP Address:**")
        for ip in ip_addresses:
            st.markdown(f"- {ip}")

        st.markdown(f"**Hostname:**\n- {hostname}")

    except dns.resolver.NoAnswer:
        st.error("No DNS record found for the domain.")
    except dns.resolver.NXDOMAIN:
        st.error("Domain does not exist.")
    except dns.resolver.Timeout:
        st.error("The request timed out while trying to contact the DNS server.")
    except dns.exception.DNSException as e:
        st.error(f"A DNS-related error occurred: {e}")


def subnet_scanner():
    @st.cache_data
    def get_geolocation(ip_address):
        # Free account access token, limited to 50K requests/month
        response = requests.get(
            f"http://ipinfo.io/{ip_address}/" "json?token=6f3b7503f7de89", timeout=5
        )
        response.raise_for_status()  # Ensure we got a valid response
        return response.json()

    st.markdown("# Subnet Scanner")

    ip_address = st.text_input("Enter IP address", "")

    if ip_address:
        try:
            ipaddress.ip_address(ip_address)  # Validates IP
            ip_address = ip_address.split(".")
            ip_address = ".".join(ip_address[:3])

            ip_coords = []
            ip_coords_unique = set()  # Showing duplicates on map makes dots too opaque

            host = 0
            while host < 256:
                try:
                    current_ip = ip_address + "." + str(host)
                    location = get_geolocation(current_ip)

                    if "bogon" in location and location["bogon"]:
                        st.error(
                            "That IP is reserved for special use and cannot be located."
                        )
                        return

                    lat_lon = location["loc"].split(",")

                    ip_coords.append(
                        {
                            "IP": current_ip,
                            "City": location["city"],
                            "Country": location["country"],
                        }
                    )
                    ip_coords_unique.add(
                        (float(lat_lon[0]), float(lat_lon[1]))
                    )  # Latitude, then longitude

                    host += 1

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        st.error("Monthly request limit reached.")
                        return
                    else:
                        raise e

            # Scatter Plot
            # Plot needs particular data format
            map_data = [
                {"lat": coord[0], "lon": coord[1]} for coord in ip_coords_unique
            ]

            ip_coords_layer = pdk.Layer(
                "ScatterplotLayer",
                map_data,
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius=1000,
                radius_min_pixels=5,
            )

            st.pydeck_chart(
                pdk.Deck(
                    layers=[ip_coords_layer],
                    initial_view_state=pdk.ViewState(
                        latitude=0,
                        longitude=0,
                        zoom=0,
                        pitch=0,
                    ),
                )
            )

            # Table
            data_frame = pd.DataFrame(ip_coords)

            st.dataframe(
                data_frame, height=35 * len(data_frame) + 38
            )  # Full table instead of small, scrollable one allows testing to work properly

        except ValueError:
            st.error("Invalid IP address.")
        except requests.exceptions.RequestException:
            st.error("Request failed.")
    else:
        st.error("Please enter an IP address.")


def traceroute_visualizer():
    # Function to calculate initial zoom
    def calculate_initial_zoom(max_lat, min_lat, max_lon, min_lon):
        earth_equator_radius = 6378.137  # in kilometers
        margin = 1.3  # to avoid cutting off arcs
        zoom_offset = 1  # adjust this value to get the desired zoom

        x_diff = (
            (max_lon - min_lon)
            * (math.pi / 180)
            * earth_equator_radius
            * math.cos(math.pi / 180 * max_lat)
        ) * margin
        y_diff = ((max_lat - min_lat) * (math.pi / 180) * earth_equator_radius) * margin

        # map width in pixels / x_diff in kilometers
        zoom_x = math.log2((23800 / x_diff)) + zoom_offset
        # map height in pixels / y_diff in kilometers
        zoom_y = math.log2((11900 / y_diff)) + zoom_offset
        return min(zoom_x, zoom_y)

    def mtr_data_table(raw_output):
        lines = raw_output.split("\n")
        pretty_output = (
            "<table><tr><th>HOST</th><th>Loss%</th>"
            "<th>Snt</th><th>Last</th><th>Avg</th>"
            "<th>Best</th><th>Wrst</th><th>StDev</th></tr>"
        )
        # Assuming the first is the header
        for line in lines[2:]:
            parts = line.split()
            # Making sure it's not an empty line or a line with insufficient data
            if parts and len(parts) > 1:
                pretty_output += "<tr><td>" + "</td><td>".join(parts[1:]) + "</td></tr>"

        pretty_output += "</table>"
        return pretty_output

    def perform_traceroute(target, radius):
        if target:
            try:
                user_ip = requests.get("https://httpbin.org/ip", timeout=5).json()[
                    "origin"
                ]
                output = subprocess.run(
                    ["mtr", "--report", "--report-cycles=1", target],
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout.decode()

                # Always display the MTR table
                st.markdown("## Raw MTR Output")
                st.markdown(mtr_data_table(output), unsafe_allow_html=True)

                regex_pattern = r"\d+\.\|\-\- ([\w\.\-]+)"
                hops = re.findall(regex_pattern, output)
                if not hops:
                    st.error(
                        "No hops found. Please try again with a different IP or domain."
                    )
                    # Indicate failure in the traceroute operation
                    st.markdown('<p id="traceroute-status">Traceroute failed</p>',\
                                unsafe_allow_html=True)
                    return

                hops.insert(0, user_ip)

                arcs_data = []
                scatter_data = []

                max_lat = -90
                min_lat = 90
                max_lon = -180
                min_lon = 180

                for i in range(len(hops) - 1):
                    try:
                        src = hops[i]
                        dst = hops[i + 1]
                        if not re.match(r"[\d\.]+", src):
                            src = socket.gethostbyname(src)
                        if not re.match(r"[\d\.]+", dst):
                            dst = socket.gethostbyname(dst)

                        response_src = DbIpCity.get(src, api_key="free")
                        response_dst = DbIpCity.get(dst, api_key="free")

                        max_lat = max(
                            max_lat, response_src.latitude, response_dst.latitude
                        )
                        min_lat = min(
                            min_lat, response_src.latitude, response_dst.latitude
                        )
                        max_lon = max(
                            max_lon, response_src.longitude, response_dst.longitude
                        )
                        min_lon = min(
                            min_lon, response_src.longitude, response_dst.longitude
                        )

                        arcs_data.append(
                            {
                                "sourcePosition": [
                                    response_src.longitude,
                                    response_src.latitude,
                                ],
                                "targetPosition": [
                                    response_dst.longitude,
                                    response_dst.latitude,
                                ],
                            }
                        )

                        scatter_data.append(
                            {
                                "position": [
                                    response_dst.longitude,
                                    response_dst.latitude,
                                ],
                                "color": [200, 30, 0, 160],
                            }
                        )

                    except (InvalidRequestError, LimitExceededError) as ip2geo_err:
                        st.error(
                            f"An error occurred while fetching geolocation data: {ip2geo_err}"
                        )
                        continue

                arc_layer = pdk.Layer(
                    "ArcLayer",
                    data=arcs_data,
                    get_source_position="sourcePosition",
                    get_target_position="targetPosition",
                    get_width=2,
                    get_height=0.5,
                    get_tilt=15,
                    get_source_color=[200, 30, 0],
                    get_target_color=[200, 30, 0],
                )

                scatter_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=scatter_data,
                    get_position="position",
                    get_radius=radius,
                    get_fill_color="color",
                )

                zoom_level = calculate_initial_zoom(max_lat, min_lat, max_lon, min_lon)

                st.pydeck_chart(
                    pdk.Deck(
                        layers=[arc_layer, scatter_layer],
                        initial_view_state={
                            "latitude": (max_lat + min_lat) / 2,
                            "longitude": (max_lon + min_lon) / 2,
                            "zoom": zoom_level,
                            "pitch": 50,
                        },
                        tooltip=True,
                    )
                )
            except requests.exceptions.RequestException as req_err:
                st.error(f"An error occurred while fetching the user IP: {req_err}")
                st.markdown('<p id="traceroute-status">Traceroute failed</p>',\
                            unsafe_allow_html=True)
            except subprocess.CalledProcessError as subp_err:
                st.error(
                    f"An error occurred while executing the traceroute command: {subp_err}"
                )
                st.markdown('<p id="traceroute-status">Traceroute failed</p>',\
                            unsafe_allow_html=True)
            except (InvalidRequestError, LimitExceededError) as ip2geo_err:
                st.error(
                    f"An error occurred while fetching geolocation data: {ip2geo_err}"
                )
                st.markdown('<p id="traceroute-status">Traceroute failed</p>',\
                            unsafe_allow_html=True)

    st.markdown("# Traceroute Map")

    # Simple input section for target IP or Domain
    target = st.text_input("Target IP or Domain", "")

    # Other UI elements
    #show_raw_output = st.checkbox("Show Raw Output", True)
    radius = st.slider(
        "Adjust Scatter Radius", min_value=0, max_value=30000, value=30000, step=1000
    )

    if target:
        perform_traceroute(target, radius)


# Expect IPs to be 4 ints separated by periods
# Moved this to top level so I can use it in other functions
def is_ip(address):
    split_ip = address.split(".")
    if len(split_ip) != 4:
        return False
    for segment in split_ip:
        try:
            int(segment)
        except ValueError:
            return False
    return True


def http_header_tool():
    st.markdown("# HTTP Header Tool")
    address = st.text_input("Enter URL or IP address", "")
    send = st.button("Send Request")

    if send and address:
        if is_ip(address):
            address = "http://" + address

        try:
            response = requests.get(address, timeout=5)
            st.subheader("Headers")
            for key in response.headers:
                st.markdown(f"```{key}: {response.headers[key]}```")

        except requests.exceptions.MissingSchema:
            st.error(
                "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, \
                    and enter IPs in the form x.x.x.x using only numbers."
            )
        except requests.exceptions.InvalidSchema:
            st.error("Invalid URL. Please use http:// or https://")
        except requests.exceptions.ReadTimeout:
            st.error("Request timed out. Please try again later.")
        except requests.exceptions.RequestException:
            st.error("Site doesn't exist or connection cannot be made at this time.")


def online_curl_tool():
    st.markdown("# Online Curl Tool")

    # Input field for the user to enter a URL
    url = st.text_input("Enter a URL (e.g., https://www.google.com)", "https://www.example.com")

    # Button to send the curl request
    if st.button("Send Curl Request"):
        if url:
            try:
                # Use subprocess to run a curl command and capture the output
                result = subprocess.check_output(
                    ["curl", url],
                    stderr=subprocess.STDOUT,
                    text=True,  # use curl instad of wget
                )
                if "<!" in result:
                    result = result[
                        result.find("<!") :
                    ]  # getting send/recv stats out of there
                st.write("Curl Response:")
                st.code(
                    result, "cshtml"
                )  # display a code block with cshtml syntax-highlighting
            except subprocess.CalledProcessError as e:
                # we receive all stdout and it looks bad, so just check if we couldn't resolve it
                if "Could not resolve host" in e.output:
                    st.error("Could not resolve host. Please try again.")
                else:  # we don't know what happened.
                    st.error("An unknown error has occured. Please try again.")


def validate_ip_address(ip_string):
    try:
        ip_object = ipaddress.ip_address(ip_string)
        return ip_object
    except ValueError:
        return False


def whois_lookup():
    st.markdown("# Whois Lookup Tool")
    request = st.text_input("Enter URL or IP address", "")

    if request:
        if is_ip(request):
            request = validate_ip_address(request)
        # Another check to make sure request is not false from IP validation
        if request:
            whois_result = whois.whois(str(request))  # if it's an IP it needs the str()
            st.subheader("Results")
            for key in whois_result:
                st.markdown(f"```{key}: {whois_result[key]}```")
        else:
            st.error("Please enter a valid URL or IP address")


def website_ping():
    st.markdown("# Website Ping")
    address = st.text_input("Enter domain name or IP address", "")

    if address:
        try:
            response = ping(address)
            if response.success(option=3):
                st.write(":heavy_check_mark: :green[Success. Website is up.]")
            elif response.success(option=1):
                st.write(
                    ":heavy_exclamation_mark: :orange[Partial Success. Website is up but \
                        experiencing difficulties.]"
                )
            else:
                st.write(":heavy_multiplication_x: :red[Failure. Website is down.]")

            with st.expander("See individual replies"):
                for line in response:
                    if line.success:
                        st.write(f":green[{line}]")
                    else:
                        st.write(f":red[{line}]")

        except RuntimeError:
            st.error("Invalid domain name or IP address.")


def regex_tester(regex_pattern="", input_data=""):
    st.title("Regex Tester")

    st.write("Enter a regex pattern and input data to test:")
    regex_pattern = st.text_area("Regex Pattern", regex_pattern)
    input_data = st.text_area("Input Data", input_data)

    if st.button("Test Regex"):
        try:
            matches = re.finditer(regex_pattern, input_data)
            match_list = [match.group() for match in matches]
            if match_list:
                st.write("Matches:", match_list)
            else:
                st.error("No matches found.")
        except re.error as e:
            st.error(f"Regex Error: {e}")
            
            
def url_encoder_decoder():
    # This is to make the colums as wide as the buttons so they aren't spread far apart
    st.markdown(
        """
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """,
        unsafe_allow_html=True,
    )
    st.markdown("# URL Encoder/Decoder")
    user_input = st.text_input("Enter the string you would like to encode/decode:")
    output = ""
    col1, col2 = st.columns([1, 1])
    with col1:
        encode = st.button("Encode")
    with col2:
        decode = st.button("Decode")

    if encode:
        output = urllib.parse.quote(user_input)
    elif decode:
        output = urllib.parse.unquote(user_input)

    if output != "":
        st.subheader("Results:")
        st.write(output)


# Dictionary of subpage functions
page1_funcs = {
    "IP Geolocation": ip_geolocation,
    "Traceroute Visualizer": traceroute_visualizer,
    "Network Analysis": network_analysis,
    "Subnet Calculator": subnet_calculator,
    "Certificate Lookup": certificate_lookup,
    "NS Lookup": ns_lookup,
    "Subnet Scanner": subnet_scanner,
    "Online Curl Tool": online_curl_tool,
    "HTTP Header Tool": http_header_tool,
    "Whois Lookup": whois_lookup,
    "Website Ping": website_ping,
    "Regex Tester": regex_tester,
    "URL Encoder and Decoder": url_encoder_decoder,
}
