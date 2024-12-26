from enum import StrEnum

from controller.user import get_all_users, get_user, User
import streamlit as st
from ui.board import Board, BoardMode
from ui.user import login_screen, modify_user_screen, create_user_screen

# WHAT IF THE BUTTONS WERE VERTICAL STRIPES, INDICATING WHICH PEOPLE HAVE VISITED

class Mode(StrEnum):
    NO_USER = 'No User'
    EDIT = 'Edit'
    VIEW = 'View'


if 'selected_state' not in st.session_state:
    st.session_state['selected_state'] = None
if 'mode' not in st.session_state:
    st.session_state.mode = Mode.NO_USER  # Default to the View Board
if 'selected_user_maps' not in st.session_state:
    st.session_state.selected_user_maps = []


@st.cache_data
def get_data() -> list[User]:
    return get_all_users()


if st.session_state.get('refresh_data') is True:
    st.cache_data.clear()
    get_data()
    print('Refreshing data')
    del st.session_state.refresh_data


all_data: list[User] = get_data()


def legend():
    if st.session_state.mode == Mode.NO_USER:
        return

    if st.session_state.mode == Mode.VIEW:
        co1, co2, co3 = st.columns([2, 2, 2])
        co1.button('No one has visited', type='tertiary')
        co2.button('Some have visited', type='secondary')
        co3.button('All have visited!', type='primary')
    else:
        co1, co2, co3, co4, co5 = st.columns([2, 2, 2, 2, 2])
        co2.button('Unvisited', type='tertiary')
        co4.button('Visited', type='primary')
    st.divider()

def user_header():
    c1, c2, c3 = st.columns([8, 2, 2])
    with c1:
        if not st.session_state.get('me'):
            st.info("""
            click Create Me to:
            - Create your map of states you've visited
            - View your friends' maps
            - Check who has been to the most and fewest states
            - See where all, some, or none of you have been!
            """)
        else:
            mode = c1.radio('Mode', ('Edit', 'View'), horizontal=True, index=1)
            st.session_state.mode = Mode(mode)

            if st.session_state.mode == Mode.EDIT:
                st.info("Click a state to add or delete it from your list.")

    with c2:
        if not st.session_state.get('me'):
            c2.button('Login', on_click=login_screen)
            c3.button('Create Me', on_click=create_user_screen)
        else:
            c3.button('Modify Me', on_click=modify_user_screen)
    st.divider()

def user_map_dd() -> list[User]:
    """Creates the UI dropdown of users & returns the selected users"""
    def encode_to_list_item_str(u: User) -> str:
        return f'{u.name} ({u.home_state_code}) ({u.state_cnt})'

    def decode_to_user_name(dd_name: str) -> str:
        return dd_name[:dd_name.find('(') - 1]

    all_users = sorted(all_data, key=lambda user: (user.email != st.session_state.me.email, user.name))
    maps_to_view: list[str] = st.multiselect('Viewing:', [encode_to_list_item_str(u) for u in all_users],
                                             placeholder='Select people from the dropdown to see their map(s)')
    selected_map_names: list[str] = [decode_to_user_name(name) for name in maps_to_view]
    st.session_state.selected_user_maps = [r for r in all_data if r.name in selected_map_names]
    st.divider()
    return st.session_state.selected_user_maps

def board_display():
    board_dict = {'Edit': lambda: Board([r for r in all_data if r.email == st.session_state.me.email], BoardMode.EDIT),
                  'View': lambda: Board(user_map_dd(), BoardMode.VIEW),
                  'No User': lambda: Board([], BoardMode.VIEW)}

    board: Board = board_dict[st.session_state.mode]()
    board.display_board()
    st.divider()

def leaderboard():
    if st.session_state.mode == Mode.NO_USER:
        return

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Most States Visited')
        st.dataframe([{'name': r.name, 'home_state': r.home_state_code, 'state_cnt': r.state_cnt}
                      for r in sorted(all_data, key=lambda x: x.state_cnt, reverse=True)])
    with col2:
        if sel_state := st.session_state.selected_state:
            st.subheader(f'{sel_state.name} Visitors')
            st.dataframe([{'name': r.name} for r in st.session_state.selected_user_maps if r.has_visited(sel_state.code)])


user_header()
legend()
board_display()
leaderboard()
