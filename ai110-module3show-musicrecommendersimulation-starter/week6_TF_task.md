# Week 6 - Music Recommender Simulation

---

## Phase 1: Understanding Recommenders (Assigned)

### TFs should:

- [X] Understand content-based vs collaborative filtering
- [X] Review `songs.csv` structure
- [X] Identify key features used
- [X] Determine your "Algorithm Recipe"

I am familiar with content-based vs collaborative filtering and have reviewed the data and it's 9 features.

Collaborative filtering doesn't need to know anything about the items, it only looks at the pattern of who liked what. If someone has the same taste as you, their favorites become your recommendations. The downside is the cold start problem: new users with no ratings and new items with no ratings can't participate.

Content-based filtering doesn't need other users at all, it analyzes the features of items you've already enjoyed, builds a preference profile, and scores new items against it. The tradeoff is that it can only recommend things similar to what you've already liked, so it tends to lack serendipity.

### TFs may skip:

- Long research summaries (Step 4)

**New concept:** Feature-driven recommendation logic

---

## Phase 2: Designing Scoring Logic (Assigned)

### TFs should:

- [X] Understand the weight formula
- [X] Manually compute one song score
- [X] Predict which song should rank first
- [X] Identify weight imbalance risks
- [X] Make a mental map of the flow: Input (User Preferences) → Process (Score each song) → Output (Top K)

Added my notes in README.md

### TFs may skip:

- Dataset expansion
- Flowchart polishing with Mermaid.js
- Documentation

**Why this matters:** This is the single biggest confusion point for students.

---

## Phase 3: Implementation (Assigned)

### TFs should:

- [X] Implement `load_songs()`
- [X] Trace `score_song()`
- [X] Verify numeric conversions (energy, tempo_bpm cast to float/int)
- [X] Confirm sorting correctness
- [X] Implement `recommend_songs()`

```
AI110/ai110-module3show-musicrecommendersimulation-starter/src/main.py
Loaded songs: 20

Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy proximity (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0), energy proximity (+0.87)

Rooftop Lights - Score: 1.96
Because: mood match (+1.0), energy proximity (+0.96)

Club Infinite - Score: 1.95
Because: mood match (+1.0), energy proximity (+0.95)

Golden Hour Drive - Score: 1.90
Because: mood match (+1.0), energy proximity (+0.90)
```

### TFs may skip:

- Advanced CLI formatting
- Documentation

---

## Phase 4: Evaluation and Bias (Assigned)

### TFs should:

- [X] Run at least two user profiles
- [X] Explain why a specific song ranked first
- [X] Run a small data experiment (e.g., weight shift or feature removal)
- [X] Identify one bias or limitation
- [X] Interpret surprising output

I ran two user profiles below:

run_profile(songs, "High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.8})
run_profile(songs, "Chill Lofi",      {"genre": "lofi", "mood": "chill", "energy": 0.35})
For the experiment, I set mood to "NONE"

Here is the results

```
Profile: High-Energy Pop, {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
  Sunrise City - Score: 3.98 | genre match (+2.0), mood match (+1.0), energy proximity (+0.98)
  Gym Hero - Score: 2.87 | genre match (+2.0), energy proximity (+0.87)
  Rooftop Lights - Score: 1.96 | mood match (+1.0), energy proximity (+0.96)
  Club Infinite - Score: 1.95 | mood match (+1.0), energy proximity (+0.95)
  Golden Hour Drive - Score: 1.90 | mood match (+1.0), energy proximity (+0.90)

Profile: Chill Lofi, {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
  Library Rain - Score: 4.00 | genre match (+2.0), mood match (+1.0), energy proximity (+1.00)
  Midnight Coding - Score: 3.93 | genre match (+2.0), mood match (+1.0), energy proximity (+0.93)
  Rainy Seoul - Score: 2.98 | genre match (+2.0), energy proximity (+0.98)
  Focus Flow - Score: 2.95 | genre match (+2.0), energy proximity (+0.95)
  Spacewalk Thoughts - Score: 1.93 | mood match (+1.0), energy proximity (+0.93)

Experiment: mood removed from scoring (pop/happy/0.8)

Profile: No Mood Weight, {'genre': 'pop', 'mood': 'NONE', 'energy': 0.8}
  Sunrise City - Score: 2.98 | genre match (+2.0), energy proximity (+0.98)
  Gym Hero - Score: 2.87 | genre match (+2.0), energy proximity (+0.87)
  Ember and Ash - Score: 0.98 | energy proximity (+0.98)
  Rooftop Lights - Score: 0.96 | energy proximity (+0.96)
  Club Infinite - Score: 0.95 | energy proximity (+0.95)
```
One bias is that genre is the dominant signal. One surprise is "Spacewalk Thoughts" has good match for mood and energy but ranks lower due to genre mismatch.

For the experiment, removing mood changed the rank of some songs, which creates some biases. 


### TFs may skip:

- None - should do all.

**New concept:** Algorithmic bias reasoning

---

## Phase 5: Model Card (Review)

### TFs should:

- [X] Skim required sections
- [X] Understand grading expectations

### TFs may skip:

- Writing full Model Cards
- Personal Reflection
