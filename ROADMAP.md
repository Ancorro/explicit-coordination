# Roadmap

- Fix the noisy-reward misses: keep c across plays but apply the complement only when the two best-action sets disagree (Algorithm 1, lines 17-20), never to all actions (lines 21-23).
- Noise sweep: vary reward variance and find where EXCEL and HYQ (hysteretic Q-learning) each stop coordinating.
- Scale: more agents (6-10) and actions (50+); measure how coordination falls off.
- Add the paper's other baselines (RFMQ, LMRL2) and its tabular grid worlds.
- Deep EXCEL on a predator-prey task, comparing the paper's three ways of using negative TD (temporal-difference) errors.
- Cross-play: pair agents trained in separate runs and test whether they still coordinate.
- Language-model agents playing the same coordination games, with or without EXCEL-style optimistic and average value summaries in their prompts.
