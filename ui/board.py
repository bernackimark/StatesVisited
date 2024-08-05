from controller.state import State, states_list
import streamlit as st

class Board:
    def __init__(self, viewing_cnt: int = 0):
        self.states = states_list()
        self.viewing_cnt = viewing_cnt

    @property
    def _organized_states(self) -> list[list[State]]:
        board = [[None for _ in range(11)] for _ in range(8)]
        for s in self.states:
            board[s.row][s.col] = s
        return board

    def display_board(self):
        for row in self._organized_states:
            cols = st.columns(len(row))  # Create a column for each button in the row
            for i, (col, state) in enumerate(zip(cols, row)):
                if state:
                    if self.viewing_cnt == 1:
                        btn_type = 'primary' if state.code in st.session_state['me'].state_data else 'secondary'
                        col.button(state.code, key=state.code, on_click=self.user_state_click, args=[state],
                                   type=btn_type, use_container_width=True)
                    if self.viewing_cnt > 1:
                        st.markdown(f'<button class="btn_light_red">{state.code}</button>', unsafe_allow_html=True)
                    # TODO:
                    # if multiple users are selected, then the state coloring scheme should be different:
                    # if everyone has been there, red.  if some, [some other color].  if none: still default color

    @staticmethod
    def user_state_click(s: State):
        st.session_state['selected_state'] = s


# TODO: ensure user can only update their own map