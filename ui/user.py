import streamlit as st

from controller.state import states_list
from controller.user import modify_user, create_user

@st.dialog('Modifying My Info')
def modify_user_screen():
    me = st.session_state.me
    my_state_name = next(s.name for s in states_list() if s.code == me.home_state_code)
    sorted_state_names = sorted([s.name for s in states_list()])
    home_state_idx = sorted_state_names.index(my_state_name)
    with st.form('My Info'):
        st.text_input('My Email (cannot be changed)', disabled=True, value=me.email)
        name = st.text_input('My First & Last Name', value=me.name)
        home_state_code = st.selectbox('My Home State', sorted_state_names, index=home_state_idx)
        submit = st.form_submit_button('Modify Me')
        if submit:
            modify_user(me.id, name, home_state_code)
            st.success('You have been modified')

@st.dialog('Creating My Profile')
def create_user_screen():
    with st.form('My Info'):
        email = st.text_input('My Email')
        name = st.text_input('My First & Last Name')
        home_state_code = st.selectbox('My Home State', sorted([s.name for s in states_list()]))
        submit = st.form_submit_button('Create Me')
        if submit:
            users_created = create_user(email, name, home_state_code)
            st.success('You have been created') if users_created else st.error('You already exist! Please login.')
