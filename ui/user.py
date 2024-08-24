import time

from controller.state import get_state_code_from_name, states_list, state_names
from controller.user import get_user, modify_user, create_user, User
import streamlit as st

SLEEP_SECONDS = 1.5

@st.dialog('Modifying My Info')
def modify_user_screen():
    me = st.session_state.me
    my_state_name = next(s.name for s in states_list() if s.code == me.home_state_code)
    home_state_idx = state_names().index(my_state_name)
    with st.form('My Info'):
        st.text_input('My Email (cannot be changed)', disabled=True, value=me.email)
        name = st.text_input('My First & Last Name', value=me.name)
        home_state_name = st.selectbox('My Home State', state_names(), index=home_state_idx)
        home_state_code = get_state_code_from_name(home_state_name)
        submit = st.form_submit_button('Modify Me')
        if submit:
            modify_user(me.email, name, home_state_code)
            st.success('You have been modified')
            updated_user = get_user(me.email)
            st.session_state.me = updated_user
            time.sleep(SLEEP_SECONDS)
            st.rerun()

@st.dialog('Creating My Profile')
def create_user_screen():
    with st.form('My Info'):
        email = st.text_input('My Email (will not be visible to anyone)')
        name = st.text_input('My First & Last Name')
        home_state_name = st.selectbox('My Home State', state_names())
        home_state_code = get_state_code_from_name(home_state_name)
        submit = st.form_submit_button('Create Me')
        if submit:
            new_user = create_user(email, name, home_state_code)
            if not new_user:
                st.error('You already exist! Please login.')
            else:
                st.success('You have been created')
                st.session_state.me = new_user
                time.sleep(SLEEP_SECONDS)
                st.rerun()

@st.dialog('Logging In')
def login_screen():
    with st.form('My Email'):
        email = st.text_input('Enter Your Email')
        submit = st.form_submit_button('Login')
        if submit:
            user = get_user(email)
            if not user:
                st.error('You weren\'t found. Please create yourself by clicking "Create Me".')
            else:
                st.session_state.me = user
                st.session_state['viewing'] = f'{user.name} ({user.home_state_code}) ({user.state_cnt})'
                st.success("Logging you in ...")
                time.sleep(SLEEP_SECONDS)
                st.rerun()
