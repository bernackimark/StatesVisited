from controller.user import get_all_users, get_user, User
import streamlit as st
from ui.board import Board
from ui.user import login_screen, modify_user_screen, create_user_screen

EDIT_LABEL = ':pencil: Edit My States'
VIEW_LABEL = ':eye: View'
TEST_USER_EMAIL = 'bernackimark@gmail.com'

if 'selected_state' not in st.session_state:
    st.session_state['selected_state'] = None
if 'board_mode' not in st.session_state:
    st.session_state.board_mode = VIEW_LABEL  # Default to the View Board
# if 'user' not in st.session_state:
#     st.session_state['me'] = get_user(TEST_USER_EMAIL)


# TODO: Viewing index should default to the person's own map upon load/login
# TODO: handle the log-in process better

@st.cache_data
def get_data() -> list[User]:
    return get_all_users()


if st.session_state.get('refresh_data') is True:
    st.cache_data.clear()
    get_data()
    print('Refreshing data')
    del st.session_state.refresh_data


all_data: list[User] = get_data()

def legend(board_mode: str):
    if board_mode == 'view':
        co1, co2, co3, co4, co5, co6 = st.columns([2, 6, 2, 6, 2, 6])
        co1.button('ST')
        co2.write('no one has visited')
        co3.button(':gray-background[ST]')
        co4.write('some have visited')
        co5.button('ST', type='primary')
        co6.write('everyone has visited')
    else:
        co1, co2, co3, co4 = st.columns([2, 6, 2, 6])
        co1.button('ST')
        co2.write("not visited")
        co3.button('ST', type='primary')
        co4.write("visited")


c1, c2, c3 = st.columns([8, 2, 2])
with c2:
    if not st.session_state.get('me'):
        c2.button('Login', on_click=login_screen)
        c3.button('Create Me', on_click=create_user_screen)
    else:
        c3.button('Modify Me', on_click=modify_user_screen)

st.divider()

col_radio, col_viewing = st.columns([1, 2])
if st.session_state.get('me'):
    st.session_state.board_mode = col_radio.radio('Interactive Mode', (EDIT_LABEL, VIEW_LABEL), horizontal=True,
                                                  index=0 if st.session_state.board_mode == EDIT_LABEL else 1)
else:
    st.session_state.board_mode = col_radio.radio('Interactive Mode (Create Yourself to Make a Map)', (VIEW_LABEL,))
if st.session_state.board_mode == EDIT_LABEL:
    st.info("Click a state to add or delete it from your list.")
else:
    st.info("Select people from the dropdown to see their map(s).")

legend(st.session_state.board_mode)

st.divider()

if st.session_state.board_mode == EDIT_LABEL:
    st.session_state['user_maps']: list[User] = [r for r in all_data if r.email == st.session_state.me.email]
else:
    name_items = [f'{r.name} ({r.home_state_code}) ({r.state_cnt})' for r in all_data]
    st.session_state['viewing']: list[str] = col_viewing.multiselect('Viewing:', name_items,
                                                                     placeholder='Select a user to view their map.')
    viewer_names: list[str] = [name[:name.find('(') - 1] for name in st.session_state.get('viewing', default='')]
    st.session_state['user_maps']: list[User] = [r for r in all_data if r.name in viewer_names]


board = Board('edit' if st.session_state.board_mode == EDIT_LABEL else 'view',
              st.session_state.get('user_maps', default=[]))
board.display_board()

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader('Most States Visited')
    st.dataframe([{'name': r.name, 'home_state': r.home_state_code, 'state_cnt': r.state_cnt}
                  for r in sorted(all_data, key=lambda x: x.state_cnt, reverse=True)])
with col2:
    if sel_state := st.session_state.selected_state:
        st.subheader(f'{sel_state.name} Visitors')
        st.dataframe([{'name': r.name} for r in all_data if r.has_visited(sel_state.code)])
