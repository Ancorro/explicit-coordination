# Explicitly Coordinated Policy Iteration: independent reproduction

*AI-sourced: assisted by AI agents.*

Independent reproduction of Yujing Hu, Yingfeng Chen, Changjie Fan and Jianye Hao, [Explicitly Coordinated Policy Iteration](https://www.ijcai.org/proceedings/2019/51) (IJCAI 2019).

## Scope

We implement the paper's tabular EXCEL algorithm and hysteretic Q-learning (HYQ) on its coordination matrix games. We omit RFMQ, LMRL2, the grid worlds and the neural-network experiments. Each training period is 10,000 game plays. At five checkpoints we measure deterministic greedy play; the paper measures after every play. Ties are broken at random.

Algorithm 1 resets EXCEL's complementary factor c at the start of each episode. A matrix game has no states, so the paper leaves open whether an episode is one game play or a whole training period. `experiment.py --c-reset play` (the default) resets c before every play; `--c-reset period` resets it once per period.

## How to run

```
bash setup.sh
python -m pytest -q
python experiment.py --method excel --agents 3 --trials 128 --stochastic
python run_all.py   # all 18 settings at 20,000 trials each; writes results.json
```

## Results

Final coordination fraction after 10,000 plays, 20 actions. Learning rate: EXCEL 0.2; HYQ positive 0.05 and negative 0.02. Exploration: epsilon-greedy, max(0.1, 0.99977^step) from 1. EXCEL complement: starts at 0, increment 0.001, cap 1. Stochastic reward standard deviations come from the paper's 90% (optimal) and 95% (other) normal intervals. Discount 0. CPU only.

**First run** (512 trials per setting, seed 42, c reset once per period; `results_512_period_reset.json`):

| Agents | Reward | EXCEL ours / paper | HYQ ours / paper |
|---|---|---|---|
| 3 | deterministic | 0.232 / 0.999 | 0.965 / 0.960 |
| 3 | stochastic | 0.086 / 0.999 | 0.803 / 0.793 |
| 4 | deterministic | 0.074 / 0.995 | 0.756 / 0.766 |
| 4 | stochastic | 0.008 / 0.993 | 0.553 / 0.440 |
| 5 | deterministic | 0.023 / 0.975 | 0.393 / 0.547 |
| 5 | stochastic | 0.002 / 0.983 | 0.404 / 0.205 |

**Probe of the reset rule** (128 trials per setting, seed 1):

| Agents | Reward | c reset per period | c reset per play | Paper |
|---|---|---|---|---|
| 3 | deterministic | 0.22 | 1.00 | 0.999 |
| 3 | stochastic | 0.09 | 1.00 | 0.999 |
| 5 | deterministic | 0.02 | 1.00 | 0.975 |
| 5 | stochastic | 0.00 | 0.49 | 0.983 |

When c carries over between plays, it grows, and the complement step (Algorithm 1, lines 21-23) keeps pulling the optimistic values toward the average values. The optimal joint action is sampled rarely, so its optimistic value decays between samples, and EXCEL behaves like an average learner. In a sweep of the cap on c with c carried over, coordination fell as the cap rose (five agents, deterministic: 0.61 at cap 0.001, 0.008 at cap 1). Resetting c every play matches the paper in three of the four probed settings. The five-agent stochastic setting still misses: under this reading c never exceeds 0.001, so the complement does little against noise. The paper's statement that c "increases from 0 to 1" does not fit a per-play reset, so neither reading reproduces every number. The 20,000-trial run of all settings has not been completed yet; `results.json` will hold it.

## Sources and attribution

- Yujing Hu, Yingfeng Chen, Changjie Fan, Jianye Hao. [Explicitly Coordinated Policy Iteration](https://www.ijcai.org/proceedings/2019/51). IJCAI 2019. The EXCEL algorithm, matrix games, hyperparameters and the "paper" numbers in the tables come from this paper. No code from the authors was used.
- Laëtitia Matignon, Guillaume J. Laurent, Nadine Le Fort-Piat. Hysteretic Q-learning: an algorithm for decentralized reinforcement learning in cooperative multi-agent teams. IEEE/RSJ IROS 2007. The HYQ baseline.
- [NumPy](https://numpy.org) (BSD-3-Clause) and [pytest](https://pytest.org) (MIT).

## Plans

See [ROADMAP.md](ROADMAP.md).

## Repo rules

This repo can be made public at any time, history included.

- No secrets: keys go in `.env` (untracked); `.env.example` lists the names only.
- No private information: cluster paths, host names, run logs, costs and personal notes go in `private/`, which is untracked and backed up outside git.
- Large data stays out of git; a script downloads it.
- Sources: add each new source to "Sources and attribution" in the commit that starts using it.
- Keep the real history: no squashing or force-pushing published commits.
