from snake_main import subtract_one_from_all_positives
from snake_main import add_apple_at_random_location
from snake_main import is_legal_move



def test_subtract_one_from_all_positives():
    print('Tester subtract_one_from_all_positives...', end='')
    a = [[2, 3, 0], [1, -1, 2]]
    subtract_one_from_all_positives(a)
    assert [[1, 2, 0], [0, -1, 1]] == a

    b = [[2, 0], [0, -1]]
    subtract_one_from_all_positives(b)
    assert [[1, 0], [0, -1]] == b
    print('OK')


test_subtract_one_from_all_positives()


def test_add_apple_at_random_location():
    print('Tester add_apple_at_random_location...', end='')
    NUMBER_OF_RUNS = 1000
    legal_states = [
        [[2, 3, -1, -1], [1, 0, 0, 0]],
        [[2, 3, -1, 0], [1, -1, 0, 0]],
        [[2, 3, -1, 0], [1, 0, -1, 0]],
        [[2, 3, -1, 0], [1, 0, 0, -1]],
    ]
    counters = [0] * len(legal_states)
    for _ in range(NUMBER_OF_RUNS):
        a = [[2, 3, -1, 0], [1, 0, 0, 0]]
        add_apple_at_random_location(a)
        assert a in legal_states
    print('OK')


test_add_apple_at_random_location()


def test_is_legal_move():
    print('Tester is_legal_move...', end='')
    board = [
        [0, 3, 4],
        [0, 2, 5],
        [0, 1, 0],
        [-1, 0, 0],
    ]
    assert is_legal_move((2, 2), board) is True
    assert is_legal_move((1, 3), board) is False # Utenfor brettet
    assert is_legal_move((1, 1), board) is False # Krasjer med seg selv
    assert is_legal_move((0, 2), board) is False # Krasjer med seg selv

    assert is_legal_move((0, 0), board) is True
    assert is_legal_move((3, 0), board) is True # Eplets posisjon er lovlig
    assert is_legal_move((3, 2), board) is True
    assert is_legal_move((-1, 0), board) is False # Utenfor brettet
    assert is_legal_move((0, -1), board) is False # Utenfor brettet
    assert is_legal_move((3, -1), board) is False # Utenfor brettet
    assert is_legal_move((3, 3), board) is False # Utenfor brettet
    assert is_legal_move((4, 2), board) is False # Utenfor brettet
    print('OK')

test_is_legal_move()




