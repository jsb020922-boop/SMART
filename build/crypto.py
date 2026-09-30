import numpy as np, json, datetime as dt, colorsys, sys
from PIL import Image
from digit import cluster, segs
C={
 'eth':dict(img='../img/v3_p35_x444_1141x442.png',start='2025-11-25',grid={'2025-12-01':4.5,'2026-01-01':108.5,'2026-02-01':212.5,'2026-03-01':306.5,'2026-04-01':410.5,'2026-05-01':511,'2026-06-01':615,'2026-07-01':715.5,'2026-08-01':819.5,'2026-09-01':923.5},
          prow=[69,121,173,225],pval=[3500,3000,2500,2000],vrow=[316,356],vval=[2e6,1e6],ptop=48,pbot=301,vtop=304,vbot=403,
          high=3447.44,low=1505.68,last=(2688.71,2735.00,2652.20,2719.33),ma=(2693.91,2578.10,2117.88),quote='USDT'),
 'stx':dict(img='../img/v3_p36_x447_1140x436.png',start='2025-10-20',grid={'2025-11-01':40.5,'2025-12-01':127,'2026-01-01':216,'2026-02-01':305,'2026-03-01':386,'2026-04-01':475,'2026-05-01':561.5,'2026-06-01':650.5,'2026-07-01':737,'2026-08-01':826,'2026-09-01':915.5},
          prow=[44.5,77,109.5,142,174,207,239,271.5],pval=[5.5e-6,5.0e-6,4.5e-6,4.0e-6,3.5e-6,3.0e-6,2.5e-6,2.0e-6],vrow=[338],vval=[5e6],vzero=402,ptop=48,pbot=308,vtop=311,vbot=410,
          high=0.00000462,low=0.00000181,last=(0.00000376,0.00000380,0.00000366,0.00000380),ma=(0.00000383,0.00000359,0.00000280),quote='BTC'),
 'zec':dict(img='../img/v3_p37_x450_1124x449.png',start='2025-10-20',grid={'2025-11-01':28.5,'2025-12-01':115,'2026-01-01':204,'2026-02-01':293.5,'2026-03-01':374,'2026-04-01':463,'2026-05-01':549.5,'2026-06-01':639,'2026-07-01':725,'2026-08-01':814,'2026-09-01':903.5},
          prow=[38.5,80.5,122.5,164.5,206.5,248.5],pval=[0.6,0.5,0.4,0.3,0.2,0.1],vrow=[320,347,374],vval=[6000,4000,2000],ptop=48,pbot=307,vtop=310,vbot=409,
          high=0.63134,low=0.05442,last=(0.55190,0.55299,0.51000,0.52372),ma=(0.57001,0.52147,0.34122),quote='ETH'),
}
def hsv(A):
    B=A/255.0; mx=B.max(2); mn=B.min(2); d=mx-mn+1e-9
    r,g,b=B[...,0],B[...,1],B[...,2]
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))/6
    s=np.where(mx>0,(mx-mn)/(mx+1e-9),0)
    return h,s,mx
def run(name):
    c=C[name]; A=np.array(Image.open(c['img']).convert('RGB')).astype(float)
    h,s,v=hsv(A)
    colored=(s>0.4)&(v>0.28)
    up=colored&(h>=0.40)&(h<=0.47)
    dn=colored&((h>=0.962)|(h<=0.02))
    cand=up|dn
    # x-grid
    ds=[dt.date.fromisoformat(k) for k in c['grid']]; xs=np.array(list(c['grid'].values()))
    d0=ds[0]; n=np.array([(d-d0).days for d in ds])
    p,x0=np.polyfit(n,xs,1)
    res=xs-(x0+p*n); print(name,'pitch',round(p,4),'max resid',round(abs(res).max(),2))
    a,b=np.polyfit(c['prow'],c['pval'],1); P=lambda y:a*y+b
    if len(c['vrow'])>=2: va,vb=np.polyfit(c['vrow'],c['vval'],1); vzero=-vb/va
    else: vzero=c['vzero']; va=-c['vval'][0]/(vzero-c['vrow'][0]); vb=-va*vzero
    V=lambda y:va*y+vb
    yH=(c['high']-b)/a; yL=(c['low']-b)/a
    lim0=int(np.floor(yH-1)); lim1=int(np.ceil(yL+1))
    day=dt.date.fromisoformat(c['start']); end=dt.date(2026,9,29); recs=[]
    while day<=end:
        k=(day-d0).days; xc=x0+p*k
        cl=int(np.floor(xc)); cols=[cl,cl+1]   # 2px candle, gridline-aligned
        if cl<0: day+=dt.timedelta(1); continue
        sub=cand[c['ptop']:c['pbot']+1][:,cols].copy()
        sub[:max(lim0-c['ptop'],0)]=False; sub[lim1-c['ptop']+1:]=False
        both=sub.all(axis=1); anyc=sub.any(axis=1)
        nonbg=(s[c['ptop']:c['pbot']+1][:,cols]>0.25).any(axis=1)
        bseg=segs(both,nonbg,maxgap=3); wseg=segs(anyc,nonbg,maxgap=3)
        if not wseg: recs.append(dict(date=day.isoformat(),missing=True)); day+=dt.timedelta(1); continue
        if bseg: bs=max(bseg,key=lambda q:q[1]-q[0])
        else:
            q=max(wseg,key=lambda q:q[1]-q[0]); m=(q[0]+q[1])//2; bs=[m,m]
        ws=[q for q in wseg if not (q[1]<bs[0]-1 or q[0]>bs[1]+1)]
        hi=min([bs[0]]+[q[0] for q in ws]); lo=max([bs[1]]+[q[1] for q in ws])
        ys=slice(c['ptop']+bs[0],c['ptop']+bs[1]+1)
        color='up' if up[ys][:,cols].sum()>=dn[ys][:,cols].sum() else 'dn'
        top,bot=P(c['ptop']+bs[0]-0.5),P(c['ptop']+bs[1]+0.5)
        if bs[0]==bs[1]: top=bot=P(c['ptop']+bs[0])
        o,cl_=(bot,top) if color=='up' else (top,bot)
        # volume: scan up from vbot
        vm=cand[c['vtop']:c['vbot']+1][:,cols].any(axis=1); vy=np.where(vm)[0]
        vol=max(V(c['vtop']+vy.min()-0.5),0) if len(vy) else 0.0
        recs.append(dict(date=day.isoformat(),o=o,h=P(c['ptop']+hi-0.5),l=P(c['ptop']+lo+0.5),c=cl_,v=vol,color=color))
        day+=dt.timedelta(1)
    miss=[r['date'] for r in recs if r.get('missing')]
    # fill missing by neighbour
    for i,r in enumerate(recs):
        if r.get('missing'):
            pv=next((q for q in recs[i-1::-1] if not q.get('missing')),None); nx=next((q for q in recs[i+1:] if not q.get('missing')),pv)
            px=((pv or nx)['c']+nx['o'])/2; recs[i]=dict(date=r['date'],o=px,h=px,l=px,c=px,v=0,color='up',filled=True)
    o,hh,ll,cc=c['last']; recs[-1].update(o=o,h=hh,l=ll,c=cc)
    iH=int(np.argmax([r['h'] for r in recs])); iL=int(np.argmin([r['l'] for r in recs]))
    recs[iH]['h']=c['high']; recs[iL]['l']=c['low']
    for i,r in enumerate(recs):
        for k in 'ohlc': r[k]=min(max(r[k],c['low']),c['high'])
        r['h']=max(r['h'],r['o'],r['c']); r['l']=min(r['l'],r['o'],r['c'])
    closes=np.array([r['c'] for r in recs])
    mas={f'ma{n}':[float(closes[max(0,i-n+1):i+1].mean()) if i>=n-1 else None for i in range(len(closes))] for n in (7,25,99)}
    print('  N',len(recs),recs[0]['date'],'→',recs[-1]['date'],'missing',len(miss),miss[:6])
    print('  HIGH',recs[iH]['date'],c['high'],' LOW',recs[iL]['date'],c['low'])
    print('  MA check (digitized vs Binance):',[ (round(mas[k][-1],8),t) for k,t in zip(['ma7','ma25','ma99'],c['ma'])])
    json.dump(dict(name=name,quote=c['quote'],bars=recs,**mas,binance_ma=c['ma'],filled=miss),open(f'data_{name}.json','w'))
    return recs
for nm in (sys.argv[1:] or C): run(nm)

def trace_ma(name):
    import extract_all  # reuse viterbi logic by duplicating minimal code
    c=C[name]; A=np.array(Image.open(c['img']).convert('RGB')).astype(float)
    h,s,v=hsv(A); colored=(s>0.4)&(v>0.28)
    d=json.load(open(f'data_{name}.json')); bars=d['bars']
    ds=[dt.date.fromisoformat(k) for k in c['grid']]; xs=np.array(list(c['grid'].values()))
    d0=ds[0]; n=np.array([(q-d0).days for q in ds]); p,x0=np.polyfit(n,xs,1)
    a,b=np.polyfit(c['prow'],c['pval'],1)
    win={'ma7':(0.09,0.16),'ma25':(0.86,0.925),'ma99':(0.70,0.77)}
    out={}
    for k,(h0,h1) in win.items():
        m=colored&(h>=h0)&(h<=h1); m[:c['ptop']+4]=False; m[c['pbot']+1:]=False
        cands=[]
        for q in bars:
            xc=x0+p*(dt.date.fromisoformat(q['date'])-d0).days; xi=int(np.floor(xc))
            rows=np.where(m[:,max(xi-1,0):xi+3].any(axis=1))[0]
            cands.append([float(np.mean(g)) for g in cluster(list(rows),gap=1)])
        MISS=6.0; prev={None:0.0}; back=[]
        for t in range(len(bars)):
            cur={};bk={}
            for st in cands[t]+[None]:
                best=1e18;arg=None
                for ps,pc in prev.items():
                    cc=pc+(MISS if st is None else (2.0 if ps is None else abs(st-ps)+(40 if abs(st-ps)>9 else 0)))
                    if cc<best: best,arg=cc,ps
                cur[st]=best;bk[st]=arg
            back.append(bk);prev=cur
        st=min(prev,key=prev.get);path=[]
        for t in range(len(bars)-1,-1,-1): path.append(st); st=back[t][st]
        path=path[::-1]
        vals=np.array([a*y+b if y is not None else np.nan for y in path]); ok=~np.isnan(vals); idx=np.arange(len(vals))
        exact=c['ma'][['ma7','ma25','ma99'].index(k)]
        vals[-1]=exact; ok[-1]=True
        first=idx[ok][0]
        vals=np.interp(idx,idx[ok],vals[ok]); vals[:first]=np.nan; out[k]=[None if np.isnan(q) else float(q) for q in vals]
        print(name,k,'coverage',round(ok.mean(),2),'last traced',vals[-1],'binance',c['ma'][['ma7','ma25','ma99'].index(k)])
    d.update({k+'_traced':v for k,v in out.items()}); json.dump(d,open(f'data_{name}.json','w'))
