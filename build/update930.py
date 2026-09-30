import json, numpy as np
# final 9/29 close (prev close implied by 9/30 reports) and 9/30 close / change
KR={'sksquare':(1118000,1139000,'+1.88%'),'hdhyundai':(201500,202500,'+0.50%'),'hdksoe':(323500,323500,'0.00%'),
    'lselectric':(205000,205000,'0.00%'),'hanwhaaero':(1012000,1007000,'-0.49%'),'dbins':(191600,185900,'-2.97%'),
    'eotech':(495500,520000,'+4.94%'),'rfmat':(48800,49250,'+0.92%'),'isc':(209500,214000,'+2.15%'),
    'lseco':(62100,62400,'+0.48%'),'samsungsdi':(511000,515000,'+0.78%'),'skinno':(145900,148800,'+1.99%')}
US={'gev':dict(c=962.49),'msft':dict(c=509.70),'anet':dict(c=203.71,h=207.60,l=201.35)}
def upd(name,c929,extra=None):
    d=json.load(open(f'data_{name}.json')); b=d['bars'][-1]
    b['c']=c929; b['h']=max(b['h'],c929); b['l']=min(b['l'],c929)
    if extra:
        if 'h' in extra: b['h']=max(extra['h'],b['h'])
        if 'l' in extra: b['l']=min(extra['l'],b['l'])
    return d
for k,(c929,c930,chg) in KR.items():
    d=upd(k,c929)
    closes=np.array([q['c'] for q in d['bars']])
    ext={}
    for m,n in (('ma5',5),('ma20',20),('ma60',60),('ma120',120)):
        arr=d.get(m+'_traced') or d[m]
        last=arr[-1]; drop=closes[-n] if len(closes)>=n else closes[0]
        ext[m]=last+(c930-drop)/n
    d['p930']=dict(c=c930,chg=chg,ma=ext)
    json.dump(d,open(f'd930/data_{k}.json','w'))
    print(k,'9/29',c929,'9/30',c930,{m:round(v) for m,v in ext.items()})
for k,e in US.items():
    d=upd(k,e['c'],e); json.dump(d,open(f'd930/data_{k}.json','w')); print(k,d['bars'][-1])
for k in ('eth','stx','zec'):
    d=json.load(open(f'data_{k}.json')); json.dump(d,open(f'd930/data_{k}.json','w'))
