import streamlit as st

st.markdown("""
    <style>
    .btn_green {
        background-color: #4CAF50; /* Green */
        color: white;
    }

    .btn_green:hover {
        background-color: #45a049;
    }

    .btn_red {
        background-color: #f44336; /* Red */
        color: white;
    }

    .btn_red:hover {
        background-color: #da190b;
    }
    
    .btn_light_red {
        background-color: #ff6666; /* Light Red */
        color: white;
    }

    .btn_light_red:hover {
        background-color: #ffcccc; /* Very Light Red */
    }
    </style>
    """, unsafe_allow_html=True)
