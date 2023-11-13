import streamlit as st
from functions.n1_Network_Tool import (
    page1_funcs,
)  # Import the dictionary of subpage functions
from functions.n2_Password_Tools import (
    page2_funcs,
)  # Import the dictionary of subpage functions
from functions.n3_Plotting_Demo import page3
from functions.n4_Mapping_Demo import page4
from functions.n5_DataFrame_Demo import page5

st.set_page_config(page_title="Netulla", page_icon="./images/favicon.png")

page_names_to_funcs = {
    "Main Page": "main_page",
    "Network Tool": page1_funcs,  # Use the dictionary as the value for 'Network Tool'
    "Password Tools": page2_funcs,  # Use the dictionary as the value for 'Password Tools'
    "Page 2": page3,
    "Page 3": page4,
    "Page 4": page5,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())

if selected_page == "Main Page":
    logo, title = st.columns([.1, .9])
    with logo:
        st.image('./images/Netulla.png')
    with title:
        st.title('Netulla')

    st.write("A web-based suite of multi-functional network tools. See the sidebar on the left to access the tools.")
    st.write("This application is written in Python using the [Streamlit](https://docs.streamlit.io) framework.")
elif isinstance(page_names_to_funcs[selected_page], dict):
    # If the selected page has subpages
    selected_subpage = st.sidebar.selectbox(
        "Select a function", page_names_to_funcs[selected_page].keys()
    )
    page_names_to_funcs[selected_page][
        selected_subpage
    ]()  # Run the selected subpage function
else:
    # If the selected page doesn't have subpages, just run the function
    page_names_to_funcs[selected_page]()
