import sys, json, numpy as np
import digit2
from digit import cluster, near
from configs import CFGS
MAC={'ma5':(255,0,0),'ma20':(50,205,50),'ma60':(0,128,255),'ma120':(102,102,102)}
def trace(A,info,recs,color,legend=(0,0,300,16)):
    p_top,p_bot=info['p_top'],info['p_bot']
    m=near(A,color,tol=10)
    m[:p_top,:]=False; m[p_bot+1:,:]=False
    lx0,ly0,lx1,ly1=legend; m[p_top+ly0:p_top+ly1,lx0:lx1]=False
    xs=[q['x'] for q in recs if not q.get('missing')]
    cands=[]
    for x in xs:
        xi=int(round(x)); rows=np.where(m[:,max(xi-1,0):xi+2].any(axis=1))[0]
        cl=cluster(list(rows),gap=1)
        cands.append([float(np.mean(c)) for c in cl])
    # viterbi smoothest path with missing state
    MISS=8.0
    n=len(xs); INF=1e18
    prev_cost={None:0.0}; back=[]
    for t in range(n):
        cur={}; bk={}
        states=cands[t]+[None]
        for s in states:
            best=INF;arg=None
            for ps,pc in prev_cost.items():
                if s is None: c=pc+MISS
                elif ps is None: c=pc+(0 if t==0 else 2.0)
                else: c=pc+abs(s-ps)
                if c<best: best,arg=c,ps
            cur[s]=best; bk[s]=arg
        # keep for backtrack
        back.append(bk); prev_cost=cur
    s=min(prev_cost,key=prev_cost.get); path=[]
    for t in range(n-1,-1,-1):
        path.append(s); s=back[t][s]
    path=path[::-1]
    a,b=info['P']
    vals=np.array([a*y+b if y is not None else np.nan for y in path])
    idx=np.arange(n); ok=~np.isnan(vals)
    if ok.sum()>=2: vals=np.interp(idx,idx[ok],vals[ok])
    return vals,ok
def run(name,verbose=True):
    cfg=CFGS[name]
    A,recs,info=digit2.extract2(cfg,verbose=verbose)
    # fill occluded candles (hidden under MA lines) as doji at neighbour-average close
    for k,q in enumerate(recs):
        if q.get('missing'):
            prv=next(r for r in recs[k-1::-1] if not r.get('missing'))
            nxt=next((r for r in recs[k+1:] if not r.get('missing')),prv)
            px=(prv['c']+nxt['o'])/2
            recs[k]=dict(date=q['date'],o=px,h=px,l=px,c=px,v=0.0,x=(prv['x']+nxt['x'])/2,w=prv['w'],color='up',filled=True)
            print('  filled occluded candle',q['date'],round(px,2))
    ok=[q for q in recs if not q.get('missing')]
    # anchors
    for q in ok:
        if q['date']==cfg['high_date']: q['h']=cfg['high']; q['o']=min(q['o'],cfg['high']); q['c']=min(q['c'],cfg['high'])
        if q['date']==cfg['low_date']: q['l']=cfg['low']; q['o']=max(q['o'],cfg['low']); q['c']=max(q['c'],cfg['low'])
    o,h,l,c=cfg['last_ohlc']; ok[-1].update(o=o,h=h,l=l,c=c)
    # clip others inside [low,high]
    for q in ok:
        for k in 'ohlc': q[k]=min(max(q[k],cfg['low']),cfg['high'])
        q['h']=max(q['h'],q['o'],q['c']); q['l']=min(q['l'],q['o'],q['c'])
    half=abs(info['P'][0])*0.5
    for q in ok:
        if q['date']!=cfg['low_date'] and q['l']<=cfg['low']+1e-9: q['l']=cfg['low']+half; q['o']=max(q['o'],q['l']); q['c']=max(q['c'],q['l'])
        if q['date']!=cfg['high_date'] and q['h']>=cfg['high']-1e-9: q['h']=cfg['high']-half; q['o']=min(q['o'],q['h']); q['c']=min(q['c'],q['h'])
    mas={}
    for k,col in MAC.items():
        v,okm=trace(A,info,ok,col); mas[k]=v.tolist(); mas[k+'_cov']=float(okm.mean())
    closes=np.array([q['c'] for q in ok])
    for k,n in (('ma5',5),('ma20',20)):
        comp=np.array([closes[i-n+1:i+1].mean() if i>=n-1 else np.nan for i in range(len(closes))])
        dv=np.array(mas[k]); msk=~np.isnan(comp)
        err=np.nanmean(abs(dv[msk]-comp[msk])/comp[msk])*100
        if verbose: print(f'  {k} coverage {mas[k+"_cov"]:.2f}  mean |digitized-computed| {err:.2f}%')
    if verbose: print('  ma60 cov',round(mas['ma60_cov'],2),'ma120 cov',round(mas['ma120_cov'],2),' last MA',[round(mas[k][-1],2) for k in MAC])
    out=dict(name=name,cfg={k:v for k,v in cfg.items() if k!='img'},bars=[{k:q[k] for k in ('date','o','h','l','c','v')} for q in ok],**{k:mas[k] for k in MAC})
    out['filled']=[q['date'] for q in ok if q.get('filled')]
    json.dump(out,open(f'data_{name}.json','w'),ensure_ascii=False)
    digit2.compare(A,recs,info,f'cmp_{name}.png',scale=1)
    return out
if __name__=='__main__':
    for n in (sys.argv[1:] or CFGS):
        print('=====',n); run(n)
