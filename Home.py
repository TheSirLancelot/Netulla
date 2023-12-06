import streamlit_antd_components as sac
import streamlit as st
from functions.n1_Network_Tool import page1_funcs
from functions.n2_Password_Tools import page2_funcs


st.set_page_config(page_title="Netulla", page_icon="./images/favicon.png")

# Link icon to function name.
# Icons are from: https://icons.getbootstrap.com/
icons = {
    "IP Geolocation": "globe2",
    "Traceroute Visualizer": "graph-up",
    "Network Analysis": "diagram-3",
    "Subnet Calculator": "calculator-fill",
    "Certificate Lookup": "certificate-fill",
    "NS Lookup": "search",
    "Subnet Scanner": "broadcast",
    "Online Curl Tool": "cloud-arrow-down",
    "HTTP Header Tool": "file-earmark-text",
    "Whois Lookup": "question-square",
    "Website Ping": "wifi",
    "URL Encoder and Decoder": "file-earmark-code",
    "Password Complexity": "shield-lock-fill",  # Example icon for Password Complexity
    "Password Generator": "key-fill" 
    
}

# Define the menu
menu_items = [
    sac.MenuItem("Home", icon="house-fill"),
    sac.MenuItem(
        "Network Tool",
        icon="binoculars",
        children=[
            # Icon is the default for the children
            sac.MenuItem(subpage, icon=icons.get(subpage, "default-icon"))
            for subpage in page1_funcs.keys()
        ],
    ),
    sac.MenuItem(
        "Password Tools",
        icon="key",
        children=[
            sac.MenuItem(subpage, icon=icons.get(subpage, "default-icon")) for subpage in page2_funcs.keys()
        ],
    ),
]

# Display the menu in the sidebar and get the selected item
with st.sidebar:
    # Size options are small, middle, largex
    selected_item = sac.menu(
        menu_items, format_func=lambda x: x, size="small", open_all=True
    )


# Function to display the main page
def show_main_page():
    logo, title = st.columns([0.1, 0.9])
    with logo:
        st.image("./images/Netulla.png")
    with title:
        st.title("Netulla")
    st.write(
        "A web-based suite of multi-functional network tools. See the sidebar on the left to access the tools."
    )
    st.write(
        "This application is written in Python using the [Streamlit](https://docs.streamlit.io) framework."
    )


# Display the selected page
if selected_item == "Home":
    show_main_page()
elif selected_item in page1_funcs:
    page1_funcs[selected_item]()
elif selected_item in page2_funcs:
    page2_funcs[selected_item]()
# We can add more pages as needed
