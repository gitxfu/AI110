from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Extreme") == (1, 100)


# --- parse_guess ---

def test_parse_valid_int():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_decimal_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_guess_boundary_low():
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"

def test_guess_boundary_high():
    outcome, _ = check_guess(100, 100)
    assert outcome == "Win"


# --- update_score ---

def test_win_on_attempt_1():
    # points = 100 - 10 * (1 + 1) = 80
    result = update_score(0, "Win", 1)
    assert result == 80

def test_win_score_floor():
    # attempt 9: points = 100 - 10 * (9 + 1) = 0 → clamped to 10
    result = update_score(0, "Win", 9)
    assert result == 10

def test_too_high_deducts_five():
    result = update_score(50, "Too High", 1)
    assert result == 45

def test_too_low_deducts_five():
    result = update_score(50, "Too Low", 1)
    assert result == 45

def test_unknown_outcome_unchanged():
    result = update_score(50, "Invalid", 1)
    assert result == 50
