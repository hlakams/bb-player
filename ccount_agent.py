"""
A collection of card-counting strategies
Names are suffixed by their level (we pick 2 per level)
"""

# card value dictionaries
# level 1
hi_lo_dict = dict([
    (0, -1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 0),
    (7, 0),
    (8, 0),
    (9, -1),
    (10, -1),
    (11, -1),
    (12, -1)
])
# level 1
ko_dict = dict([
    (0, -1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 0),
    (8, 0),
    (9, -1),
    (10, -1),
    (11, -1),
    (12, -1)
])

# level 2
zen_dict = dict([
    (0, -1),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 1),
    (7, 0),
    (8, 0),
    (9, -2),
    (10, -2),
    (11, -2),
    (12, -2)
])
ten_dict = dict([
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (9, -2),
    (10, -2),
    (11, -2),
    (12, -2)
])

# level 3
halves_dict = dict([
    (0, -1),
    (1, 0.5),
    (2, 1),
    (3, 1),
    (4, 1.5),
    (5, 1),
    (6, 0.5),
    (7, 0),
    (8, -0.5),
    (9, -1),
    (10, -1),
    (11, -1),
    (12, -1)
])
uston_dict = dict([
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 2),
    (4, 3),
    (5, 2),
    (6, 2),
    (7, 1),
    (8, -1),
    (9, 3),
    (10, 3),
    (11, 3),
    (12, -3)
])

# return current count value
def ccount(name: str, value: int) -> float:
    # level 1
    if name == "hi_lo":
        return hi_lo_dict.get(value)
    elif name == "ko":
        return ko_dict.get(value)
    # level 2
    elif name == "zen":
        return zen_dict.get(value)
    elif name == "ten":
        return ten_dict.get(value)
    # level 3
    elif name == "halves":
        return halves_dict.get(value)
    elif name == "uston":
        return uston_dict.get(value)

def ccount_action(state: int, count: float):
    if state == 1 and count > (26/4):
        return 9
    elif count > 0:
        return 7
    else:
        return 8