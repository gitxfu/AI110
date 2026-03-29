"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def run_profile(songs, label, user_prefs, k=5):
    print(f"\nProfile: {label}, {user_prefs}")
    for song, score, explanation in recommend_songs(user_prefs, songs, k=k):
        print(f"  {song['title']} - Score: {score:.2f} | {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Two user profiles
    run_profile(songs, "High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.8})
    run_profile(songs, "Chill Lofi",      {"genre": "lofi", "mood": "chill", "energy": 0.35})

    # Experiment: remove mood from scoring to see ranking shift
    print("\nExperiment: mood removed from scoring (pop/happy/0.8)")
    no_mood_prefs = {"genre": "pop", "mood": "NONE", "energy": 0.8}
    run_profile(songs, "No Mood Weight", no_mood_prefs)


if __name__ == "__main__":
    main()
