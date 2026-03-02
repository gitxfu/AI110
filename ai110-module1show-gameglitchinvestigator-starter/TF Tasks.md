# TF Tasks for Week 2 -  Game Glitch Investigator


## Phase 1: Glitch Hunt (Spot Check)

I have ran the app, tried the game and identify 9 bugs. 

## Phase 2: Investigate and Repair (Assigned)

- I fixed 9 bugs end‑to‑end. For less straightforward bugs, I reviewed and accepted the AI-generated edit.

- For refactoring, I used this prompt:
```
I need to refactor app.py by moving the four game logic functions into logic_utils.py. The functions to move are already defined and working in app.py.

Rules:
Copy each function exactly as-is into logic_utils.py, replacing the raise NotImplementedError stubs.
Do not change any logic inside the functions.
After moving them, delete the function definitions from app.py and add from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score at the top of app.py.
```

- My prompts to write pytest cases: 
```
For each of the four functions (get_range_for_difficulty, parse_guess, check_guess, update_score), generate pytest test cases in tests/test_game_logic.py.

Rules:
Test both the happy path and edge cases for each function.
check_guess returns a tuple (outcome, message), unpack it and assert only on outcome.
For parse_guess, test: valid int, valid decimal (should truncate), empty string, None, and non-numeric input.
For update_score, test: Win on attempt 1, Win on a late attempt (score floor of 10), Too High, Too Low.
Do not import streamlit. Tests must run with plain pytest and no UI dependencies.
Keep each test function focused on one behavior.
```

- I ran pytest successfully

```
(.venv) ai110-module1show-gameglitchinvestigator-starter (main) $ python -m pytest tests/test_game_logic.py -v
```

```
tests/test_game_logic.py::test_easy_range PASSED                                                                      [  5%]
tests/test_game_logic.py::test_normal_range PASSED                                                                    [ 10%]
tests/test_game_logic.py::test_hard_range PASSED                                                                      [ 15%]
tests/test_game_logic.py::test_unknown_difficulty_defaults_to_normal PASSED                                           [ 21%]
tests/test_game_logic.py::test_parse_valid_int PASSED                                                                 [ 26%]
tests/test_game_logic.py::test_parse_decimal_truncates PASSED                                                         [ 31%]
tests/test_game_logic.py::test_parse_empty_string PASSED                                                              [ 36%]
tests/test_game_logic.py::test_parse_none PASSED                                                                      [ 42%]
tests/test_game_logic.py::test_parse_non_numeric PASSED                                                               [ 47%]
tests/test_game_logic.py::test_winning_guess PASSED                                                                   [ 52%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                                  [ 57%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                                   [ 63%]
tests/test_game_logic.py::test_guess_boundary_low PASSED                                                              [ 68%]
tests/test_game_logic.py::test_guess_boundary_high PASSED                                                             [ 73%]
tests/test_game_logic.py::test_win_on_attempt_1 PASSED                                                                [ 78%]
tests/test_game_logic.py::test_win_score_floor PASSED                                                                 [ 84%]
tests/test_game_logic.py::test_too_high_deducts_five PASSED                                                           [ 89%]
tests/test_game_logic.py::test_too_low_deducts_five PASSED                                                            [ 94%]
tests/test_game_logic.py::test_unknown_outcome_unchanged PASSED                                                       [100%]
```

- Here are the hints I prepared to guide students to find the bugs I fixed without giving them the answers.

```
1. You're on Easy mode. The sidebar says 1–20 but the info box says 1–100. Is this expected?

2. You guessed 80 and the secret is 30. Your guess is too high. What should the game tell you to do? 

3. Before you guess anything on a new fresh game, how many attempts does it say you have left? 

4. Type space and press Submit three times.  Should a typo cost you a turn? 

5. Start an Easy game, click New Game, check Debug expander, is the secret between 1 and 20?

6. You Win a game, then click New Game. What happens?

7. Switch from Normal to Easy in the sidebar, check if the secret change.

8. Do you always lose points for wrong answers? 

9. Try to guess the correct number on your 2nd attempt specifically. What happens?

```


## Phase 3: Reflection and README (Review)
- I reviewed reflection prompts and will focus the group discussion to compare approaches, prompts, and insights.
