from collections import defaultdict

from controller.state import State, states_by_coord
from controller.user import User
from controller.user_state import add_user_state, delete_user_state
import streamlit as st

# this reduces the gap between states, which caused the gray background to spill the state code text onto two lines
st.markdown(
    """
    <style>
        div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

class Board:
    def __init__(self, mode: str, user_data: list[User]):
        self.mode = mode
        self.states_by_coord: dict[tuple[int, int]: State] = states_by_coord()
        self._matrix: list[[list[State]]] = [[self.states_by_coord.get((r, c)) for c in range(11)] for r in range(8)]
        self.users_data: list[User] = user_data

    @property
    def map_cnt(self) -> int:
        return len(self.users_data)

    @property
    def states(self) -> dict[str: list[User]]:
        """Pivot the data by state.  The dict is {state: [User, User]}"""
        d = defaultdict(list)
        [d[state].append(user) for user in self.users_data for state in user.states]
        return dict(d)

    def state_visit_cnt(self, state_code: str) -> int:
        return len(self.states[state_code])

    def state_button_props(self, state_code: str):
        """No one has visited = label: normal, button: secondary.
        Some have visited = label: special formatting, button: secondary.
        Everyone's visited = label: normal, button, primary."""
        if not self.states.get(state_code):
            return {'label': state_code, 'type': 'secondary'}
        if self.state_visit_cnt(state_code) < self.map_cnt:
            return {'label': f':gray-background[{state_code}]', 'type': 'secondary'}
        return {'label': state_code, 'type': 'primary'}

    def display_board(self):
        for row in self._matrix:
            cols = st.columns(len(row))  # Create one st.column for each button in the row
            for i, (col, state) in enumerate(zip(cols, row)):
                if not state:
                    continue
                btn_props = self.state_button_props(state.code)
                if col.button(btn_props['label'], key=state.code, args=[state], type=btn_props['type'],
                              use_container_width=True):
                    self.user_state_click(state)

    def user_state_click(self, s: State):
        st.session_state['selected_state'] = s
        if self.mode != 'edit':
            return
        if not st.session_state.me.states or st.session_state.selected_state.code not in st.session_state.me.states:
            add_user_state(st.session_state.me, st.session_state.selected_state)
        else:
            delete_user_state(st.session_state.me, st.session_state.selected_state)
        st.session_state.selected_state = None
        st.session_state.refresh_data = True
