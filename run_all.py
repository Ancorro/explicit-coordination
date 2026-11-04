"""Paper-scale matrix runs: 20,000 trials per setting, split into seeded chunks run in parallel."""
import concurrent.futures, json, os, subprocess, sys
from pathlib import Path
TRIALS, CHUNKS, STEPS, SEED = 20000, 8, 10000, 42
settings = [(method, reset, n, noise) for method, reset in (('excel', 'play'), ('excel', 'period'), ('hyq', None))
            for n in (3, 4, 5) for noise in (False, True)]
def execute(job):
    (method, reset, n, noise), k = job
    cmd = [sys.executable, 'experiment.py', '--method', method, '--agents', str(n), '--trials', str(TRIALS // CHUNKS),
           '--steps', str(STEPS), '--seed', str(SEED + k)]
    if reset: cmd += ['--c-reset', reset]
    if noise: cmd.append('--stochastic')
    return json.loads(subprocess.check_output(cmd, text=True, env={**os.environ, 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1'}))
if __name__ == '__main__':
    jobs = [(s, k) for s in settings for k in range(CHUNKS)]
    workers = int(os.environ.get('WORKERS', 10))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool: parts = list(pool.map(execute, jobs))
    results = []
    for i, s in enumerate(settings):
        chunk = parts[i * CHUNKS:(i + 1) * CHUNKS]; first = dict(chunk[0])
        first.update(trials=TRIALS, seed=[SEED + k for k in range(CHUNKS)])
        first['curve'] = [{key: (pt['step'] if key == 'step' else sum(c['curve'][j][key] for c in chunk) / CHUNKS)
                           for key in pt} for j, pt in enumerate(chunk[0]['curve'])]
        results.append(first)
    Path('results.json').write_text(json.dumps(results, indent=2) + '\n')
