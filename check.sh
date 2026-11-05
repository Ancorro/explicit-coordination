#!/usr/bin/env bash
# Runs the tests, EXCEL with a noise-adaptive complementary factor on all six matrix games, and language-model agents on the same game.
set -euo pipefail
python -m pytest -q
for n in 3 4 5; do
  for noise in "" "--stochastic"; do
    python experiment.py --method excel-adaptive --agents "$n" --trials 512 $noise \
      | python -c "import json,sys; r=json.load(sys.stdin); print(r['method'], r['agents'], 'stochastic' if r['stochastic'] else 'deterministic', r['curve'][-1]['coordination'])"
  done
done
python llm_game.py --agents 3 --actions 20 --trials 20
