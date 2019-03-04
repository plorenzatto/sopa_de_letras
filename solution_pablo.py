import numpy as np
from pathlib import Path
import string
import sys

VOID = ' '

def get_board(board_sz=(10, 10), alphabet=string.ascii_lowercase):
    board = np.random.choice(list(alphabet), size=board_sz)
    protected = np.random.choice([VOID], size=board_sz)
    return board, protected

orient_confs = {
    'horizonal': {
        'get_valid_square_max_offset': lambda board, word: (
            board.shape[0],
            board.shape[1] - len(word),
        ),
        'get_indices': lambda place_select, word: (
            [place_select[0]] * len(word),
            list(range(place_select[1], place_select[1]+len(word))),
        ),
    },
    'vertical': {
        'get_valid_square_max_offset': lambda board, word: (
            board.shape[0] - len(word),
            board.shape[1],
        ),
        'get_indices': lambda place_select, word: (
            list(range(place_select[0], place_select[0]+len(word))),
            [place_select[1]] * len(word),
        ),
    },
    'diagonal_from_lefttop': {
        'get_valid_square_max_offset': lambda board, word: (
            board.shape[0] - len(word),
            board.shape[1] - len(word),
        ),
        'get_indices': lambda place_select, word: (
            list(range(place_select[0], place_select[0]+len(word))),
            list(range(place_select[1], place_select[1]+len(word))),
        ),
    },
    'diagonal_from_leftbottom': {
        'get_valid_square_max_offset': lambda board, word: (
            board.shape[0] - len(word),
            board.shape[1] - len(word),
        ),
        'get_indices': lambda place_select, word: (
            list(range(place_select[0], place_select[0]+len(word)))[::-1],
            list(range(place_select[1], place_select[1]+len(word))),
        ),
    },
}

def insert_word(board, protected, word, orient='horizonal', start_upperleft=True, retries=100, mark_words=False):
    """Insert a word in the given orientation word.
    
    TODO: Word overlap logic.
    """
    word = list(word)
    if not start_upperleft:
        word = word[::-1]
    valid_square_max_offset = orient_confs[orient]['get_valid_square_max_offset'](board, word)
    for i in range(retries):
        place_select = (
            np.random.randint(0, valid_square_max_offset[0]),
            np.random.randint(0, valid_square_max_offset[1]),
        )
        indices = orient_confs[orient]['get_indices'](place_select, word)
        
        if all(cp == VOID or cw == cp for cw, cp in zip(word, protected[indices])):
            protected[indices] = word
            if mark_words:
                word = list(map(str.upper, word))
            board[indices] = word
            break
    else:
        return None
    
    return board, protected


def get_filled_board(board_sz, wordlist, num_words, mark_words=False):
    alphabet = list(set(''.join(wordlist)))
    board, protected = get_board(board_sz, alphabet)
    words = []
    for w in np.random.choice(wordlist, num_words):
        words.append(w)
        start_upperleft = np.random.choice([True, False])
        orient = np.random.choice(list(orient_confs.keys()))
        rv = insert_word(board, protected, w, start_upperleft=start_upperleft, orient=orient, mark_words=mark_words)
        if rv is None:
            print(f"Couldn't place {w}")
        else:
            board, protected = rv
    
    return board, protected, words


# fn = '"/etc/dictionaries-common/words"'
fn = 'spanish_dict.txt'

if not Path(fn).exists():
    print("Wordlist not found. Run the following command to get it:")
    print("wget -nc -O spanish_dict.txt https://raw.githubusercontent.com/tendermint/mintkey/master/wordlist/spanish.txt")
    sys.exit(1)

with open(fn) as f:
    wordlist = [w.strip().lower() for w in f.readlines()]
    alphabet = list(set(''.join(wordlist)))
    def word_filter(w):
        return len(w) <= 9 and all(c in alphabet for c in w)

    wordlist = list(filter(word_filter, wordlist))

board, protected, words = get_filled_board((20, 20), wordlist, num_words=20)

print('Word list:')
print('\n'.join(sorted(words)))
print()
print('Board only with words:')
print('\n'.join(' '.join(l) for l in protected))
print()
print('Complete board:')
print('\n'.join(' '.join(l) for l in board))

