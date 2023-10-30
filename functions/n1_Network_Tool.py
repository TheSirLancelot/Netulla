import socket
import ipaddress
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import nmap
import plotly.express as px


def ip_geolocation():
    # st.set_page_config(page_title="IP Geolocation", page_icon="🕸")

    st.markdown("# IP Geolocation")
    # st.sidebar.header("IP Geolocation")

    ip_address = st.sidebar.text_input(
        "Enter an IP Address", value="8.8.8.8", max_chars=None, key=None, type="default"
    )

    @st.cache_data
    def get_geolocation(ip_address):
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        response.raise_for_status()  # Ensure we got a valid response
        return response.json()

    if ip_address:
        location = get_geolocation(ip_address)
        latitude = location["lat"]
        longitude = location["lon"]

        st.sidebar.markdown(f"### Geolocation of IP: {ip_address}")
        st.sidebar.markdown(f"**Latitude:** {latitude}")
        st.sidebar.markdown(f"**Longitude:** {longitude}")

        # Display IP location on a map
        map_data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})
        layer = pdk.Layer(
            "ScatterplotLayer",
            map_data,
            get_position=["lon", "lat"],
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
    st.markdown("# Network Analysis")

    # Add separator
    st.sidebar.markdown("---")

    # Move the ip_input to the sidebar
    ip_input = st.sidebar.text_input("Enter IP address (e.g., 8.8.8.8, 45.33.32.156)")

    well_known_ports = st.sidebar.checkbox("Scan only well-known ports")

    # Add separator
    st.sidebar.markdown("---")

    # Add Execute button
    execute = st.sidebar.button("Execute")

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
            ports_filter = st.sidebar.checkbox("Show only open ports")

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
            network = ipaddress.IPv4Network(f"{ip_input}/{cidr_input}")
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


# Dictionary of subpage functions
page1_funcs = {
    "IP Geolocation": ip_geolocation,
    "Network Analysis": network_analysis,
    "Subnet Calculator": subnet_calculator,
}
