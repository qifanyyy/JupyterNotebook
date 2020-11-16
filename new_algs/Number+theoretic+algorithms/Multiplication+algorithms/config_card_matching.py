RANK_CODE = {
    'A': 1,
    'K': 13,
    'Q': 12,
    'J': 11
}

SUIT_CODE = {
    'hearts': 1,
    'spades': 2,
    'clubs': 3,
    'diamonds': 4
   }

CARD_SUITS = [ 'diamonds', 'clubs', 'spades', 'hearts' ]
CARD_RANKS = [ 'A' ] + list(map(str, range(2, 10)))

PROGRAM_SET = [
    ("MOVE_PTR", 4, 2),       # Moves Pointer card1/car2/out (3 options) either left or right (2 options)
    ("WRITE", 2, 10),          # writes digit (10 options) on Out Pointer
    ("CMP", ),                # Top-Level Compare Program (calls children routines)
    ("USUB1",),               # Subtract operation (single digit; ignores sign)
    ("LSHIFT",)               # Shifts all Pointers Left (after Sub)
]

PROGRAM_ID = {x[0]: i for i, x in enumerate(PROGRAM_SET)}

PROGRAM_NUM = len(PROGRAM_SET) # MOVE_PTR, WRITE, CMP, LSHIFT


CONFIG = {
    "ENVIRONMENT_ROW": 3,         # Input 1, Input 2, Carry, Output
    "ENVIRONMENT_COL": 3,         # 3-Digit Maximum for Compare Task
    "ENVIRONMENT_DEPTH": 10,      # Size of each element vector => One-Hot, Options: 0-9

    "ARGUMENT_NUM": 3,            # Maximum Number of Program Arguments
    "ARGUMENT_DEPTH": 11,         # Size of Argument Vector => One-Hot, Options 0-9, Default (10)
    "DEFAULT_ARG_VALUE": 9,      # Default Argument Value

    "PROGRAM_NUM": PROGRAM_NUM,             # Maximum Number of Subroutines
    "PROGRAM_KEY_SIZE": PROGRAM_NUM - 1,    # Size of the Program Keys
    "PROGRAM_EMBEDDING_SIZE": 10            # Size of the Program Embeddings
}