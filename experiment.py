import argparse, json
import numpy as np

def run(method, n, m, trials, steps, stochastic, seed, c_reset='play', cmax=1.0):
    rng = np.random.default_rng(seed)
    avg = np.zeros((trials,n,m)); opt = avg.copy(); c = np.zeros((trials,n))
    row = np.arange(trials)[:,None]; agent = np.arange(n)[None,:]
    curve = []
    def greedy(v):
        return np.argmax(v + rng.random(v.shape)*1e-10, axis=2)
    for t in range(steps):
        if method == 'excel':
            mask = opt == opt.max(axis=2,keepdims=True)
            policy = greedy(np.where(mask,avg,-np.inf))
        else: policy = greedy(avg)
        eps = max(.1, .99977**t)
        actions = np.where(rng.random((trials,n)) < eps, rng.integers(m,size=(trials,n)),policy)
        s = actions.sum(axis=1); best = np.all(actions == actions[:, :1],axis=1)
        reward = np.where(best,n*(m-1),np.maximum(s,n*(m-1)-s)).astype(float)
        if stochastic:
            sigma = np.where(best,.3/1.6448536269514722,.2/1.959963984540054)*reward
            reward = rng.normal(reward,sigma)
        prev = avg[row,agent,actions]; delta = reward[:,None]-prev
        rate = .2 if method == 'excel' else np.where(delta>=0,.05,.02)
        avg[row,agent,actions] = prev + rate*delta
        if method == 'excel':
            prev = opt[row,agent,actions]; opt[row,agent,actions] = prev + .2*np.maximum(0,reward[:,None]-prev)
            om = opt == opt.max(axis=2,keepdims=True); am = avg == avg.max(axis=2,keepdims=True)
            disjoint = ~(om & am).any(axis=2)
            if c_reset == 'play': c = np.zeros_like(c)  # one game play is one episode (Algorithm 1, line 4)
            c = np.where(disjoint,np.minimum(c+.001,cmax),c)
            select = np.where(disjoint[:,:,None],om,True)
            opt += select*c[:,:,None]*(avg-opt)
        if t in {0,99,999,4999,steps-1}:
            if method=='excel':
                mask = opt == opt.max(axis=2,keepdims=True); test = greedy(np.where(mask,avg,-np.inf))
            else: test = greedy(avg)
            total=test.sum(axis=1); coord=np.all(test==test[:,:1],axis=1)
            curve.append({'step':t+1,'coordination':float(coord.mean()),'reward':float(np.where(coord,n*(m-1),np.maximum(total,n*(m-1)-total)).mean())})
    return {'method':method,'agents':n,'actions':m,'trials':trials,'steps':steps,'stochastic':stochastic,'seed':seed,'c_reset':c_reset if method=='excel' else None,'cmax':cmax if method=='excel' else None,'curve':curve}
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--agents',type=int,default=3); p.add_argument('--actions',type=int,default=20); p.add_argument('--trials',type=int,default=128); p.add_argument('--steps',type=int,default=10000); p.add_argument('--seed',type=int,default=42); p.add_argument('--method',choices=['excel','hyq'],default='excel'); p.add_argument('--stochastic',action='store_true'); p.add_argument('--c-reset',choices=['play','period'],default='play'); p.add_argument('--cmax',type=float,default=1.0); a=p.parse_args()
    print(json.dumps(run(a.method,a.agents,a.actions,a.trials,a.steps,a.stochastic,a.seed,a.c_reset,a.cmax)))
