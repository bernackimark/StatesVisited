from datetime import date

from controller.data import DataRow, get_all_data
from controller.user import get_user
from controller.user_state import add_user_state, delete_user_state
import streamlit as st
from ui.board import Board
from ui.user import modify_user_screen, create_user_screen

if 'my_states' not in st.session_state:
    st.session_state['my_states'] = {}
if 'selected_state' not in st.session_state:
    st.session_state['selected_state'] = None
if 'user' not in st.session_state:
    st.session_state['me'] = get_user(4)

# TODO: Viewing index should default to the person's own map upon load/login
# TODO: handle the log-in process better

@st.cache_data
def get_data() -> list[DataRow]:
    return get_all_data()

def refresh_data() -> None:
    st.cache_data.clear()
    get_data()


all_data: list[DataRow] = get_data()


def display_user_states():
    if my_states := st.session_state['me'].state_data:
        table = [{'State': code, 'Year': data['visited_on']} for code, data in my_states.items()]
        st.dataframe(table, column_config={'Year': st.column_config.NumberColumn('Year Visited', format='%d')})

@st.dialog('Add a State')
def dialog_add_user_state():
    s = st.session_state.get('selected_state')
    st.subheader(s.name)
    years = sorted(range(date.today().year - 100, date.today().year + 1), reverse=True)
    year = st.selectbox('Year First Visited (Optional)', years, index=None)
    btn_text = 'Submit With Year' if year else 'Submit Without Year'
    submit = st.button(btn_text, on_click=add_user_state, args=[st.session_state['me'], s, year])
    if submit:
        st.session_state['selected_state'] = None
        refresh_data()

@st.dialog('Are you sure you want to delete this state from your list?')
def confirm_delete_state():
    s = st.session_state.get('selected_state')
    st.subheader(s.name)
    submit = st.button(f"Yes, I definitely want to remove {s.name}")
    if submit:
        delete_user_state(st.session_state['me'], s)
        st.session_state['selected_state'] = None
        refresh_data()

def add_delete_state_btn():
    if not st.session_state['selected_state']:
        return
    if st.session_state['selected_state'].code not in st.session_state['me'].state_data:
        st.button(f"Add {st.session_state['selected_state'].name} to My States", on_click=dialog_add_user_state)
    else:
        st.button(f"Remove {st.session_state['selected_state'].name} from My States", on_click=confirm_delete_state)


c1, c2, c3 = st.columns([6, 4, 2])
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

name_items = [f'{r.name} ({r.home_state_code}) ({r.state_cnt})' for r in all_data]
st.session_state['viewing']: list[str] = st.multiselect('Viewing:', name_items,
                                    placeholder='The generic map; select a user to view their map.')


st.divider()
# TODO: this legend is butt ugly
co1, co2, co3, co4, co5, co6 = st.columns([1, 3, 1, 3, 1, 3])
co1.button('ST', disabled=True)
co2.write('no one has visited')
co3.button(':gray-background[ST]', disabled=True, use_container_width=True)
co4.write('some have visited')
co5.button('ST', type='primary')
co6.write('everyone has visited')

viewer_names: list[str] = [name[:name.find('(')-1] for name in st.session_state['viewing']]
filtered_data: list[DataRow] = [r for r in all_data if r.name in viewer_names]
board = Board(filtered_data)
board.display_board()

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader('My States')
    display_user_states()
with col2:
    st.subheader('All Users')
    st.dataframe([{'name': r.name, 'home_state': r.home_state_code, 'state_cnt': r.state_cnt} for r in all_data])
