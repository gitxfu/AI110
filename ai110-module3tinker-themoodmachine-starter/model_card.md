# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**
Both models were used and compared — a rule-based classifier in `mood_analyzer.py` and a logistic regression ML model in `ml_experiments.py`.

**Intended purpose:**
Classify short social media-style posts into one of four mood labels: positive, negative, neutral, or mixed.

**How it works (brief):**
The rule-based model tokenizes text, scores each token against positive/negative word lists (with negation handling and emoji signals), then maps the score to a label. The ML model converts posts into word-count vectors (bag of words) and learns which word patterns correlate with each label from the labeled examples.



## 2. Data

**Dataset description:**
Started with 6 posts, expanded to 20 total. New posts were intentionally varied: slang ("lowkey", "fire", "vibing"), emojis (🔥💀😩💪✨), sarcasm, and ambiguous mixed-emotion sentences.

**Labeling process:**
Labels were assigned by human judgment. Hard cases included "I'm fine 🙂" (labeled neutral, but could be sarcasm → negative) and "it is what it is" (resignation, labeled neutral). "sick beats bro" required cultural context — "sick" means impressive here, not bad.

**Important characteristics of your dataset:**
- Small (25 examples) and English-only
- Includes sarcasm, slang, emojis, and mixed feelings
- Skewed toward mixed/negative posts; fewer purely positive examples

**Possible issues with the dataset:**
Labels reflect one person's interpretation. Sarcastic posts especially could be labeled differently by different people. The dataset lacks any formal language, longer sentences, or non-English expressions.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**
- Each positive word token adds +1; each negative word subtracts -1
- Negation words ("not", "don't", "never", etc.) flip the sign of the next sentiment word
- Positive emojis (🔥😂💪✨) add +1; negative emojis (😩😢💀) subtract -1; 🙂 is unscored (too ambiguous)
- Short function words ("a", "so", "the") don't cancel the negation window
- Label thresholds: if both positive and negative signals exist → mixed; else score > 0 → positive, score < 0 → negative, 0 → neutral

**Strengths of this approach:**
Works reliably for clear single-sentiment posts and handles negation well ("I am not happy" → negative, "not bad at all" → positive). Fully transparent — every decision can be traced to a rule.

**Weaknesses of this approach:**
Cannot detect sarcasm ("I love getting stuck in traffic" → positive). Words outside the vocabulary are invisible ("hopeful", "proud", "accomplished" all score 0). Slang meaning depends on context ("sick" = bad in the word list, but cool in practice).

## 4. How the ML Model Works (if used)

**Features used:**
Bag of words using `CountVectorizer` — each post becomes a vector of word counts.

**Training data:**
Trained on all 25 posts in `SAMPLE_POSTS` with labels from `TRUE_LABELS`.

**Training behavior:**
Adding more diverse posts improved the ML model's ability to distinguish mixed vs. negative cases. It correctly labeled “sick beats bro” as positive and detected sarcasm in “I love getting stuck in traffic” — both of which the rule-based model failed on. However, it trains and tests on the same data, so its 100% accuracy is overfitting, not generalization.

**Strengths and weaknesses:**
Strength: learns patterns from examples without needing explicit rules — slang and context are implicitly captured if labeled correctly. Weakness: with only 25 examples, it memorizes rather than generalizes. Any mislabeled post directly corrupts what it learns.

## 5. Evaluation

**How you evaluated the model:**
Both models were evaluated against `TRUE_LABELS` on all 25 posts. Rule-based accuracy: **60%**. ML accuracy: **100%** (overfitted — trained and tested on same data).

**Examples of correct predictions:**
- "Today was a terrible day" → negative (rule-based: "terrible" hits; ML: learned from label)
- "not bad at all" → positive (rule-based: negation of "bad" flips sign correctly)
- "Ugh so tired of being tired 😩" → negative (rule-based: emoji + "tired" both score negative)

**Examples of incorrect predictions (rule-based):**
- "I love getting stuck in traffic" → predicted positive, true negative — sarcasm; "love" dominates
- "everything is falling apart and I can't stop it" → predicted neutral, true negative — no words from the negative list matched
- "Feeling tired but kind of hopeful" → predicted negative, true mixed — "hopeful" is not in the word list, so only "tired" scores

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only
