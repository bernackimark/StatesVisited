from collections import defaultdict

from controller.data import DataRow
from controller.state import State, states_by_coord
import streamlit as st

class Board:
    def __init__(self, user_data: list[DataRow]):
        self.states_by_coord: dict[tuple[int, int]: State] = states_by_coord()
        self._matrix: list[[list[State]]] = [[self.states_by_coord.get((r, c)) for c in range(11)] for r in range(8)]
        self.users_data: list[DataRow] = user_data

    @property
    def map_cnt(self) -> int:
        return len(self.users_data)

    @property
    def states(self) -> dict[str: list[DataRow]]:
        """Pivot the data by state.  The dict is {state: [DataRow, DatRow]}"""
        d = defaultdict(list)
        [d[state.state_code].append(user_map) for user_map in self.users_data for state in user_map.state_data]
        return dict(d)

    def state_visit_cnt(self, state_code: str) -> int:
        return len(self.states[state_code])

    def state_tooltip(self, state_code: str) -> str:
        users_and_years = {}
        for user_data in self.states[state_code]:
            yr = next((s.year for s in user_data.state_data if s.state_code == state_code), None)
            users_and_years[user_data.name] = yr
        return '\n'.join([f'{name}: {year}' for name, year in users_and_years.items()])

    def state_button_props(self, state_code: str):
        """No one has visited = label: normal, button: secondary, tooltip: none.
        Some have visited = label: special formatting, button: secondary, tooltip: yes.
        Everyone's visited = label: normal, button, primary, tooltip: yes"""
        if not self.states.get(state_code):
            return {'label': state_code, 'type': 'secondary', 'help': None}
        if self.state_visit_cnt(state_code) < self.map_cnt:
            return {'label': f':gray-background[{state_code}]', 'type': 'secondary', 'help': self.state_tooltip(state_code)}
        return {'label': state_code, 'type': 'primary', 'help': self.state_tooltip(state_code)}

    def display_board(self):
        for row in self._matrix:
            cols = st.columns(len(row))  # Create one st.column for each button in the row
            for i, (col, state) in enumerate(zip(cols, row)):
                if not state:
                    continue
                btn_props = self.state_button_props(state.code)
                col.button(btn_props['label'], key=state.code, on_click=lambda x: self.user_state_click(x),
                           args=[state], type=btn_props['type'], help=btn_props['help'], use_container_width=True)

    @staticmethod
    def user_state_click(s: State):
        st.session_state['selected_state'] = s
