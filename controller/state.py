from dataclasses import dataclass
import json


@dataclass
class State:
    code: str
    name: str
    coord: tuple[int, int]

    @property
    def row(self) -> int:
        return self.coord[0]

    @property
    def col(self) -> int:
        return self.coord[1]


STATES = {'AL': State(code='AL', name='Alabama', coord=(6, 6)), 'AK': State(code='AK', name='Alaska', coord=(7, 1)),
          'AZ': State(code='AZ', name='Arizona', coord=(5, 1)), 'AR': State(code='AR', name='Arkansas', coord=(5, 4)),
          'CA': State(code='CA', name='California', coord=(4, 0)), 'CO': State(code='CO', name='Colorado', coord=(4, 2)),
          'CT': State(code='CT', name='Connecticut', coord=(3, 9)), 'DE': State(code='DE', name='Delaware', coord=(4, 9)),
          'FL': State(code='FL', name='Florida', coord=(7, 8)), 'GA': State(code='GA', name='Georgia', coord=(6, 7)),
          'HI': State(code='HI', name='Hawaii', coord=(7, 0)), 'ID': State(code='ID', name='Idaho', coord=(2, 1)),
          'IL': State(code='IL', name='Illinois', coord=(2, 5)), 'IN': State(code='IN', name='Indiana', coord=(3, 5)),
          'IA': State(code='IA', name='Iowa', coord=(3, 4)), 'KS': State(code='KS', name='Kansas', coord=(5, 3)),
          'KY': State(code='KY', name='Kentucky', coord=(4, 5)), 'LA': State(code='LA', name='Louisiana', coord=(6, 4)),
          'ME': State(code='ME', name='Maine', coord=(0, 10)), 'MD': State(code='MD', name='Maryland', coord=(4, 8)),
          'MA': State(code='MA', name='Massachusetts', coord=(2, 9)), 'MI': State(code='MI', name='Michigan', coord=(2, 6)),
          'MN': State(code='MN', name='Minnesota', coord=(2, 4)), 'MS': State(code='MS', name='Mississippi', coord=(6, 5)),
          'MO': State(code='MO', name='Missouri', coord=(4, 4)), 'MT': State(code='MT', name='Montana', coord=(2, 2)),
          'NE': State(code='NE', name='Nebraska', coord=(4, 3)), 'NV': State(code='NV', name='Nevada', coord=(3, 1)),
          'NH': State(code='NH', name='New Hampshire', coord=(1, 10)), 'NJ': State(code='NJ', name='New Jersey', coord=(3, 8)),
          'NM': State(code='NM', name='New Mexico', coord=(5, 2)), 'NY': State(code='NY', name='New York', coord=(2, 8)),
          'NC': State(code='NC', name='North Carolina', coord=(5, 6)), 'ND': State(code='ND', name='North Dakota', coord=(2, 3)),
          'OH': State(code='OH', name='Ohio', coord=(3, 6)), 'OK': State(code='OK', name='Oklahoma', coord=(6, 3)),
          'OR': State(code='OR', name='Oregon', coord=(3, 0)), 'PA': State(code='PA', name='Pennsylvania', coord=(3, 7)),
          'RI': State(code='RI', name='Rhode Island', coord=(3, 10)), 'SC': State(code='SC', name='South Carolina', coord=(5, 7)),
          'SD': State(code='SD', name='South Dakota', coord=(3, 3)), 'TN': State(code='TN', name='Tennessee', coord=(5, 5)),
          'TX': State(code='TX', name='Texas', coord=(7, 3)), 'UT': State(code='UT', name='Utah', coord=(4, 1)),
          'VT': State(code='VT', name='Vermont', coord=(1, 9)), 'VA': State(code='VA', name='Virginia', coord=(4, 7)),
          'WA': State(code='WA', name='Washington', coord=(2, 0)), 'WV': State(code='WV', name='West Virginia', coord=(4, 6)),
          'WI': State(code='WI', name='Wisconsin', coord=(1, 5)), 'WY': State(code='WY', name='Wyoming', coord=(3, 2))}

def states_list() -> list[State]:
    with open('states.json', 'r') as f:
        d: dict = json.load(f)
    return [State(code, name, coord) for code, (name, coord) in d.items()]
