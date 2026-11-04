# Explicitly Coordinated Policy Iteration: independent reproduction

*AI-sourced: written by an AI agent.*

Independent reproduction of Yujing Hu, Yingfeng Chen, Changjie Fan and Jianye Hao, [Explicitly Coordinated Policy Iteration](https://www.ijcai.org/proceedings/2019/51) (IJCAI 2019).

## Scope

We implement the paper's tabular EXCEL algorithm and hysteretic Q-learning (HYQ) on its coordination matrix games. We omit RFMQ, LMRL2, the grid worlds and neural-network experiments. Unlike the paper's 20,000 training periods per setting, this experiment uses 512, so uncertainty is larger. Each period is treated as a 10,000-step episode, with EXCEL's complementary factor reset once at its start. At each of five checkpoints we measure deterministic greedy play; the paper measures after every play. Ties are randomly broken. These choices and any implementation differences may contribute to discrepancies.

Run `bash setup.sh`, `python run_all.py`, and `python -m pytest -q`. Results are saved to `results.json`.

## Results

Final coordination fraction, 512 independent trials per setting, 10,000 steps per trial, 20 actions, seed 42, CPU on a desktop PC. Learning rate: EXCEL 0.2; HYQ positive 0.05 and negative 0.02. Exploration decays as max(0.1, 0.99977^step), starting at 1. EXCEL complement starts at 0, increments by 0.001 and is capped at 1. Stochastic reward standard deviations are derived from the paper's stated 90% and 95% normal intervals. A matrix game is modeled as one continuing episode with discount 0. All settings use the same seed independently.

| Agents | Reward | EXCEL ours / paper | HYQ ours / paper |
|---|---|---|---|
| 3 | deterministic | 0.232 / 0.999 | 0.965 / 0.960 |
| 3 | stochastic | 0.086 / 0.999 | 0.803 / 0.793 |
| 4 | deterministic | 0.074 / 0.995 | 0.756 / 0.766 |
| 4 | stochastic | 0.008 / 0.993 | 0.553 / 0.440 |
| 5 | deterministic | 0.023 / 0.975 | 0.393 / 0.547 |
| 5 | stochastic | 0.002 / 0.983 | 0.404 / 0.205 |

The EXCEL result does not reproduce the paper: its coordination is much lower in every setting. HYQ is broadly similar in the three-agent case but diverges at five agents. The cause of the EXCEL discrepancy is unresolved; episode boundaries, value complement behavior, and tie handling warrant investigation. These are hypotheses, not established explanations. The results do not establish the paper's claimed advantage. The complete checkpoint measurements and hyperparameters are in `results.json`.
