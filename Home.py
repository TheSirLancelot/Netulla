import streamlit_antd_components as sac
import streamlit as st
from functions.n1_Network_Tool import page1_funcs
from functions.n2_Password_Tools import page2_funcs

st.set_page_config(page_title="Netulla", page_icon="./images/favicon.png")

# Define the menu
menu_items = [
    # Icons are from: https://icons.getbootstrap.com/
    sac.MenuItem('Home', icon='house-fill'),
    sac.MenuItem('Network Tool', icon='binoculars', children=[
        # Icon is the default for the children
        sac.MenuItem(subpage, icon='arrow-right') for subpage in page1_funcs.keys()
    ]),
    sac.MenuItem('Password Tools', icon='key', children=[
        sac.MenuItem(subpage, icon='arrow-right') for subpage in page2_funcs.keys()
    ]),
]

# Display the menu in the sidebar and get the selected item
with st.sidebar:
    # Size options are small, middle, largex
    selected_item = sac.menu(menu_items, format_func='title', size='small', open_all=True)

# Function to display the main page
def show_main_page():
    logo, title = st.columns([.1, .9])
    with logo:
        st.image('./images/Netulla.png')
    with title:
        st.title('Netulla')
    st.write("A web-based suite of multi-functional network tools. See the sidebar on the left to access the tools.")
    st.write("This application is written in Python using the [Streamlit](https://docs.streamlit.io) framework.")

# Display the selected page
if selected_item == 'Home':
    show_main_page()
elif selected_item in page1_funcs:
    page1_funcs[selected_item]()
elif selected_item in page2_funcs:
    page2_funcs[selected_item]()
# We can add more pages as needed
