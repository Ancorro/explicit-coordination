import concurrent.futures, json, subprocess, sys
from pathlib import Path
jobs=[(method,n,noise) for method in ('excel','hyq') for n in (3,4,5) for noise in (False,True)]
def execute(job):
    method,n,noise=job
    cmd=[sys.executable,'experiment.py','--method',method,'--agents',str(n),'--trials','512','--steps','10000','--seed','42']
    if noise: cmd.append('--stochastic')
    return json.loads(subprocess.check_output(cmd,text=True))
if __name__=='__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as pool: results=list(pool.map(execute,jobs))
    Path('results.json').write_text(json.dumps(results,indent=2)+'\n')
