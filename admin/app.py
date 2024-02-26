import streamlit as st
from mock_data import create_df_ranking

# Define the sidebar
sidebar = st.sidebar

# Define the sidebar menu
menu = ["Tableau de bord"]
choice = sidebar.selectbox("Menu", menu)

# Set "Tableau de bord" as the default menu
if choice == "Tableau de bord":
    df = create_df_ranking()
    st.dataframe(df, width=1000, height=500)