from datetime import date

from controller.data import get_all_data
from controller.user import create_user, get_user, modify_user
from controller.user_state import add_user_state, delete_user_state
import streamlit as st
from ui.board import Board, states_list

if 'my_states' not in st.session_state:
    st.session_state['my_states'] = {}
if 'selected_state' not in st.session_state:
    st.session_state['selected_state'] = None
if 'user' not in st.session_state:
    st.session_state['me'] = get_user(6)

@st.cache_data
def get_data():
    return get_all_data()


all_data = get_data()

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

def display_user_states():
    if my_states := st.session_state['me'].state_data:
        table = [{'State': code, 'Year': data['visited_on']} for code, data in my_states.items()]
        st.dataframe(table, column_config={'Year': st.column_config.NumberColumn('Year Visited', format='%d')})

@st.dialog('Add a State')
def dialog_add_user_state():
    s = st.session_state.get('selected_state')
    st.subheader(s.name)
    years = sorted(range(date.today().year - 100, date.today().year + 1), reverse=True)
    year = st.selectbox('Year Visited (Optional)', years, index=None)
    btn_text = 'Submit With Year' if year else 'Submit Without Year'
    submit = st.button(btn_text, on_click=add_user_state, args=[st.session_state['me'], s, year])
    if submit:
        st.session_state['selected_state'] = None
        st.rerun()

@st.dialog('Are you sure you want to delete this state from your list?')
def confirm_delete_state():
    s = st.session_state.get('selected_state')
    st.subheader(s.name)
    submit = st.button(f"Yes, I definitely want to remove {s.name}")
    if submit:
        delete_user_state(st.session_state['me'], s)
        st.session_state['selected_state'] = None
        st.rerun()

def add_delete_state_btn():
    if not st.session_state['selected_state']:
        return
    if st.session_state['selected_state'].code not in st.session_state['me'].state_data:
        st.button(f"Add {st.session_state['selected_state'].name} to My States", on_click=dialog_add_user_state)
    else:
        st.button(f"Remove {st.session_state['selected_state'].name} from My States", on_click=confirm_delete_state)


c1, c2, c3 = st.columns([4, 4, 2])
with c1:
    add_delete_state_btn()
with c2:
    if st.session_state.get('me'):
        c2.write(st.session_state.me.name)
with c3:
    if not st.session_state.get('me'):
        c3.button('Create Me', on_click=create_user_screen)
    else:
        c3.button('Modify Me', on_click=modify_user_screen)

items = [f'{r.name} ({r.home_state_code}) ({r.state_cnt})' for r in all_data.data]
viewing = st.multiselect('Viewing:', items)
# TODO: Viewing index should default to the person's own map upon load/login

st.divider()
board = Board(len(viewing))
board.display_board()
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader('My States')
    display_user_states()
with col2:
    st.subheader('All Users')
    st.dataframe(all_data.users_and_state_counts)
