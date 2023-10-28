def ip_geolocation():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk
    import requests
    #st.set_page_config(page_title="IP Geolocation", page_icon="🕸")

    st.markdown("# IP Geolocation")
    #st.sidebar.header("IP Geolocation")

    ip_address = st.sidebar.text_input("Enter an IP Address", value="8.8.8.8", max_chars=None, key=None, type='default')

    @st.cache_data
    def get_geolocation(ip_address):
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()  # Ensure we got a valid response
        return response.json()

    if ip_address:
        location = get_geolocation(ip_address)
        latitude = location['lat']
        longitude = location['lon']

        st.sidebar.markdown(f"### Geolocation of IP: {ip_address}")
        st.sidebar.markdown(f"**Latitude:** {latitude}")
        st.sidebar.markdown(f"**Longitude:** {longitude}")

        # Display IP location on a map
        map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
        layer = pdk.Layer(
            'ScatterplotLayer',
            map_data,
            get_position=['lon', 'lat'],
            get_color=[200, 30, 0, 160],
            get_radius=1000,
        )

        # Set the initial view, https://deckgl.readthedocs.io/en/latest/view_state.html
        view_state = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=12,
            pitch=50,
        )

        # Render the deck.gl map in the Streamlit app as a PyDeck chart 
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.error("Please enter an IP address.")

def network_analysis():
    import streamlit as st
    import socket
    import requests
    import ipaddress
    import nmap
    import pandas as pd

    st.markdown("# Network Analysis")

    # Add separator
    st.sidebar.markdown('---')

    # Move the ip_input to the sidebar
    ip_input = st.sidebar.text_input("Enter IP address (e.g., 8.8.8.8, 45.33.32.156)")

    well_known_ports = st.sidebar.checkbox("Scan only well-known ports")

    # Add separator
    st.sidebar.markdown('---')

    # Add Execute button
    execute = st.sidebar.button("Execute")

    # Set a boolean flag in the session state to indicate whether the "Execute" button has been clicked
    if execute:
        st.session_state['executed'] = True
    if not 'executed' in st.session_state:
        st.session_state['executed'] = False

    # Only show the description if the "Execute" button has not been clicked
    if not st.session_state['executed']:
        st.markdown("""This tool provides information about the network related to the provided IP address. 
            It scans for open ports, the corresponding service for well-known ports, and geographical information 
            related to the IP. Please input an IP address and click 'Execute' to start the analysis.
            """)

    # Read port descriptions from file
    well_known_ports_dict = {}
    with open('functions/port_descriptions.txt', 'r') as file:
        for line in file:
            port, description = line.strip().split(',')
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

            response = requests.get(f"http://ip-api.com/json/{ip_input}")
            response.raise_for_status()  # Ensure we got a valid response
            data = response.json()

            st.session_state['host_name'] = host_name
            st.session_state['ISP'] = data['isp']
            st.session_state['Region'] = data['regionName']
            st.session_state['City'] = data['city']
            st.session_state['ZIP'] = data['zip']

            # Use Nmap to get open ports
            scanner = nmap.PortScanner()
            ports_to_scan = ','.join(map(str, well_known_ports_dict.keys())) if well_known_ports else '1-1024'
            scanner.scan(ip_input, ports_to_scan)
            
            # Initialize ports DataFrame
            ports_data = []

            for port in scanner[ip_input]['tcp'].keys():
                status = scanner[ip_input]['tcp'][port]['state']
                description = well_known_ports_dict.get(port, 'N/A')
                ports_data.append({'Port': port, 'Status': status, 'Description': description})

            st.session_state['ports_data'] = ports_data  # Store ports data in session state

        except ValueError:
            st.error("Invalid IP address.")
        except requests.exceptions.RequestException:
            st.error("Request failed.")
    # Display information if scan has been executed
    if 'executed' in st.session_state and st.session_state['executed']:
        st.write(f"Hostname: {st.session_state['host_name']}")
        st.write(f"ISP: {st.session_state['ISP']}")
        st.write(f"Region: {st.session_state['Region']}")
        st.write(f"City: {st.session_state['City']}")
        st.write(f"ZIP: {st.session_state['ZIP']}")

        # If scan has finished, allow user to filter ports
        if 'ports_data' in st.session_state:
            ports_filter = st.sidebar.checkbox("Show only open ports")

            # Update the ports_data if filter is applied
            if ports_filter:
                ports_data = [data for data in st.session_state['ports_data'] if data['Status'] == 'open']
            else:
                ports_data = st.session_state['ports_data']

            ports_df = pd.DataFrame(ports_data)
            st.dataframe(ports_df.set_index('Port'))  # Display the data in a more interactive table

def subnet_calculator():
    import streamlit as st
    import ipaddress
    import pandas as pd
    import plotly.express as px

    st.markdown("# Subnet Calculator")

    ip_input = st.text_input("Enter IP address (e.g., 192.168.0.1)", '')
    cidr_input = st.number_input("Enter CIDR (e.g., 24)", min_value=0, max_value=32, value=24)

    if ip_input and cidr_input:
        try:
            # Create network object
            network = ipaddress.IPv4Network(f"{ip_input}/{cidr_input}")
            st.success("Valid IP address and CIDR")

            st.markdown("### Subnet Details")

            details = {
                "Total IPs": str(network.num_addresses),
                "Usable IPs": str(network.num_addresses - 2) if network.prefixlen != 32 else "1",
                "Network Address": str(network.network_address),
                "Broadcast Address": str(network.broadcast_address),
                "Subnet Mask": str(network.netmask),
                "Wildcard Mask": str(network.hostmask),
                "Binary Subnet Mask": bin(int(network.netmask))
            }
            
            # Converting the dictionary to a list of tuples
            details_list = list(details.items())
            # Creating the DataFrame
            df = pd.DataFrame(details_list, columns=['Information', 'Value'])
            st.table(df.set_index('Information'))

            # Pie chart for the IP address allocation
            if network.prefixlen < 32:
                allocation = {
                    "Usable IP Range": network.num_addresses - 2,
                    "Network and Broadcast": 2
                }

                df = pd.DataFrame(allocation.items(), columns=['Category', 'Count'])
                fig = px.pie(df, values='Count', names='Category', title='IP Allocation')
                st.plotly_chart(fig)

        except ValueError:
            st.error("Invalid IP address or CIDR.")

def traceroute_visualizer():
    import streamlit as st
    import pydeck as pdk
    import subprocess
    import re
    import requests
    import math
    from ip2geotools.databases.noncommercial import (DbIpCity,
                                                     InvalidRequestError,
                                                     LimitExceededError)

    def calculate_initial_zoom(max_lat, min_lat, max_lon, min_lon):
        earth_equator_radius = 6378.137  # in kilometers
        margin = 1.3  # to avoid cutting off arcs
        zoom_offset = 1  # adjust this value to get the desired zoom

        x_diff = ((max_lon - min_lon) * (math.pi / 180) * earth_equator_radius *
                  math.cos(math.pi / 180 * max_lat)) * margin
        y_diff = ((max_lat - min_lat) * (math.pi / 180) * earth_equator_radius) * margin

        # map width in pixels / x_diff in kilometers
        zoom_x = math.log2((23800 / x_diff)) + zoom_offset
        # map height in pixels / y_diff in kilometers
        zoom_y = math.log2((11900 / y_diff)) + zoom_offset

        return min(zoom_x, zoom_y)

    def mtr_data_table(raw_output):
        lines = raw_output.split('\n')
        pretty_output = "<table><tr><th>HOST</th><th>Loss%</th><th>Snt</th><th>Last</th><th>Avg\
        </th><th>Best</th><th>Wrst</th><th>StDev</th></tr>"
        # Add each line of mtr data as a row in the table
        for line in lines[2:]:
            parts = line.split()
            if parts:
                pretty_output += "<tr><td>" + "</td><td>".join(parts[1:]) + "</td></tr>"

        pretty_output += "</table>"

        return pretty_output

    try:
        st.markdown("# Traceroute Map")

        # Simple input section
        target = st.text_input("Target IP or Domain")
        # This shows the output for MTR, if checked
        show_raw_output = st.sidebar.checkbox('Show Raw Output', True)
        # Slider to adjust the radius of scatter points
        radius = st.sidebar.slider('Adjust Scatter Radius',
                                   min_value=0, max_value=30000, value=30000, step=1000)
        # Save radius so if slider is adjusted after scanning IP/DNS, the map regenerates
        last_radius = st.session_state.get('last_radius', None)
        # Save output so if user checks the box after a scan,
        # the map regenerates with/without the output
        last_show_raw_output = st.session_state.get('last_show_raw_output', None)

        if st.button("Run Traceroute") or (last_radius != radius) or \
            (last_show_raw_output != show_raw_output):
            # Save the current radius to the session state
            st.session_state.last_radius = radius
            # Save the current checkbox state to the session state
            st.session_state.last_show_raw_output = show_raw_output

            if target:  # Check if the target input is not empty
                try:
                    user_ip = requests.get('https://httpbin.org/ip').json()['origin']
                    output = subprocess.run(["mtr", "--report", "--report-cycles=1", target],
                                            stdout=subprocess.PIPE, check=True).stdout.decode()

                    if show_raw_output:
                        st.markdown("## Raw MTR Output")
                        st.markdown(mtr_data_table(output), unsafe_allow_html=True)

                    hops = re.findall(r"\d+\.\|\-\- ([\d\.]+|[\?\?\?]+)", output)
                    if not hops:
                        st.error("No hops found. Please try again with a different IP or domain.")
                        return

                    hops.insert(0, user_ip)
                    hops = [hop for hop in hops if hop != "???"]

                    arcs_data = []
                    scatter_data = []

                    max_lat = -90
                    min_lat = 90
                    max_lon = -180
                    min_lon = 180

                    for i in range(len(hops) - 1):
                        response_src = DbIpCity.get(hops[i], api_key='free')
                        response_dst = DbIpCity.get(hops[i+1], api_key='free')

                        max_lat = max(max_lat, response_src.latitude, response_dst.latitude)
                        min_lat = min(min_lat, response_src.latitude, response_dst.latitude)
                        max_lon = max(max_lon, response_src.longitude, response_dst.longitude)
                        min_lon = min(min_lon, response_src.longitude, response_dst.longitude)

                        arcs_data.append({
                            "sourcePosition": [response_src.longitude, response_src.latitude],
                            "targetPosition": [response_dst.longitude, response_dst.latitude],
                        })

                        scatter_data.append({
                            "position": [response_dst.longitude, response_dst.latitude],
                            "color": [200, 30, 0, 160],
                        })

                    arc_layer = pdk.Layer(
                        'ArcLayer',
                        data=arcs_data,
                        get_source_position='sourcePosition',
                        get_target_position='targetPosition',
                        get_width=2,
                        get_tilt=15,
                        get_source_color=[200, 30, 0],
                        get_target_color=[200, 30, 0],
                    )

                    scatter_layer = pdk.Layer(
                        'ScatterplotLayer',
                        data=scatter_data,
                        get_position='position',
                        get_radius=radius,
                        get_fill_color='color',
                    )

                    zoom_level = calculate_initial_zoom(max_lat, min_lat, max_lon, min_lon)

                    st.pydeck_chart(pdk.Deck(
                        layers=[arc_layer, scatter_layer],
                        initial_view_state={
                            "latitude": (max_lat + min_lat) / 2,
                            "longitude": (max_lon + min_lon) / 2,
                            "zoom": zoom_level,
                            "pitch": 50,
                        },
                        tooltip=True,
                    ))
                except requests.exceptions.RequestException as req_err:
                    st.error(f"An error occurred while fetching the user IP: {req_err}")
                except subprocess.CalledProcessError as subp_err:
                    st.error(f"An error occurred while executing the traceroute\
                             command: {subp_err}")
                except (InvalidRequestError, LimitExceededError) as ip2geo_err:
                    st.error(f"An error occurred while fetching geolocation data: {ip2geo_err}")

    # Having pylint ignore as the point of this is to catch any errors the prior exceptions did not
    except Exception as e: # pylint: disable=broad-except
        st.error(f"An error occurred: {e}")

# Dictionary of subpage functions
page1_funcs = {
    "IP Geolocation": ip_geolocation,
    "Network Analysis": network_analysis,
    "Subnet Calculator": subnet_calculator,
    "Traceroute Visualizer": traceroute_visualizer
}
