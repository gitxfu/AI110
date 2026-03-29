# Week 6 - Music Recommender Simulation

---

## Phase 1: Understanding Recommenders (Assigned)

### TFs should:

- [ ] Understand content-based vs collaborative filtering
- [ ] Review `songs.csv` structure
- [ ] Identify key features used
- [ ] Determine your "Algorithm Recipe"

I am familiar with content-based vs collaborative filtering and have reviewed the data and it's 9 features.

### TFs may skip:

- Long research summaries (Step 4)

**New concept:** Feature-driven recommendation logic

---

## Phase 2: Designing Scoring Logic (Assigned)

### TFs should:

- [ ] Understand the weight formula
- [ ] Manually compute one song score
- [ ] Predict which song should rank first
- [ ] Identify weight imbalance risks
- [ ] Make a mental map of the flow: Input (User Preferences) → Process (Score each song) → Output (Top K)

### TFs may skip:

- Dataset expansion
- Flowchart polishing with Mermaid.js
- Documentation

**Why this matters:** This is the single biggest confusion point for students.

---

## Phase 3: Implementation (Assigned)

### TFs should:

- [ ] Implement `load_songs()`
- [ ] Trace `score_song()`
- [ ] Verify numeric conversions (energy, tempo_bpm cast to float/int)
- [ ] Confirm sorting correctness
- [ ] Implement `recommend_songs()`

### TFs may skip:

- Advanced CLI formatting
- Documentation

---

## Phase 4: Evaluation and Bias (Assigned)

### TFs should:

- [ ] Run at least two user profiles
- [ ] Explain why a specific song ranked first
- [ ] Run a small data experiment (e.g., weight shift or feature removal)
- [ ] Identify one bias or limitation
- [ ] Interpret surprising output

### TFs may skip:

- None - should do all.

**New concept:** Algorithmic bias reasoning

---

## Phase 5: Model Card (Review)

### TFs should:

- [ ] Skim required sections
- [ ] Understand grading expectations

### TFs may skip:

- Writing full Model Cards
- Personal Reflection
