import numpy as np
from PIL import Image, ImageDraw
import cal
from digit import near, rows_of, cluster, segs

def load(cfg):
    A=np.array(Image.open(cfg['img']).convert('RGB')).astype(int)
    return A

def extract2(cfg, verbose=True):
    A=load(cfg); Hh,Ww,_=A.shape
    UPc=cfg.get('upc',(220,2,2)); DNc=cfg.get('dnc',(0,1,200))
    sep=rows_of(A,cfg.get('sepc',(204,204,204)),10,840,0.9)
    p_top,p_bot=sep[0]+1,sep[1]-1
    v_top=sep[1]+1; v_bot=[s for s in sep if s>v_top+20][0]-1
    X0,X1=cfg.get('xrange',(8,850))
    up=near(A,UPc); dn=near(A,DNc); white=(A.min(axis=2)>=245)|near(A,(233,233,233),4)|near(A,(238,238,238),3)
    cand=up|dn; bridge=~white & ~cand
    # calendar & month-start gridlines
    days=cal.days(cfg['start_search'],cfg['last'],cfg['cal'],cfg.get('extra_hol',()))
    vg=[x for x in range(X0,X1) if ((np.abs(A[p_top:p_bot,x,:]-np.array((233,233,233))).max(axis=1)<=3).mean()>0.3)]
    vg=[c[0] for c in cluster(vg)]
    vg=[x for x in vg if x>X0+3]
    if cfg.get('vg_drop'): vg=[x for x in vg if x not in cfg['vg_drop']]
    firsts={}
    for i,d in enumerate(days): firsts.setdefault((d.year,d.month),i)
    fi=sorted(firsts.values())[-len(vg):]
    p,x0=np.polyfit(np.array(fi,float),np.array(vg,float),1)
    res=np.array(vg)-(x0+p*np.array(fi))
    idxd={d.isoformat():i for i,d in enumerate(days)}
    goff0=cfg.get('goff',None); goff0=(p-1.75)/2 if goff0 is None else goff0
    anc={}
    for key in ('high','low'):
        c_=x0+p*idxd[cfg[key+'_date']]+goff0
        anc[key]=(c_,list(range(int(np.floor(c_-2.5)),int(np.ceil(c_+2.5))+1)))
    # price calibration from horizontal gridlines
    hg=rows_of(A[p_top:p_bot+1],(233,233,233),10,840,0.5)
    hg=[c[0]+p_top for c in cluster(hg)]
    gv=cfg['gridvals']
    if cfg.get('gridrows'): hg=cfg['gridrows']
    assert len(hg)==len(gv), (hg,gv)
    a,b=np.polyfit(hg,gv,1)
    Pinv=lambda v:(v-b)/a
    yH=Pinv(cfg['high']); yL=Pinv(cfg['low'])
    # clamp: remove candle pixels outside [yH-1.5, yL+1.5] in price panel
    lim_top=int(np.floor(yH-1.0)); lim_bot=int(np.ceil(yL+1.0))
    # text-label band masking: candle-colored pixels beyond the extremes can only be label text
    for side in ('top','bot'):
        if side=='top': rr=np.arange(p_top,max(lim_top,p_top))
        else: rr=np.arange(lim_bot+1,p_bot+1)
        if len(rr)==0: continue
        sub=cand[rr][:,X0:X1+60].copy()
        ys,xs=np.where(sub)
        ys=rr[ys]; xs=xs+X0
        keep=~((ys<p_top+15)&(xs<330))
        ys,xs=ys[keep],xs[keep]
        if len(ys)<15: continue
        ac=anc['high' if side=='top' else 'low']
        cl=cluster(sorted(set(xs.tolist())),gap=25)
        best=min(cl,key=lambda c:min(abs(c[0]-ac[0]),abs(c[-1]-ac[0])))
        sel=(xs>=best[0])&(xs<=best[-1]); ys,xs=ys[sel],xs[sel]
        if len(ys)<15: continue
        cfg['_anchor_cols']=ac[1]
        if side=='top': t1=ys.max(); t0=min(ys.min(), t1-13); t1=max(t1, ys.min()+13)
        else: t0=ys.min(); t1=max(ys.max(), t0+13); t0=min(t0, ys.max()-13)
        xa,xb=xs.min()-3,xs.max()+4
        t0=max(t0,p_top); t1=min(t1,p_bot)
        cfg.setdefault('_autotext',[]).append((int(xa),int(t0),int(xb),int(t1+1)))
    for (x0_,y0_,x1_,y1_) in cfg.get('_autotext',[]):
        keep=cfg.get('_anchor_cols',[])
        for M in (up,dn,cand):
            saved=M[y0_:y1_,keep].copy() if keep else None
            M[y0_:y1_,x0_:x1_]=False
            if keep: M[y0_:y1_,keep]=saved
    for M in (up,dn,cand):
        M[p_top:max(lim_top,p_top),:]=False; M[lim_bot+1:p_bot+1,:]=False
    for (x0,y0,x1,y1) in cfg.get('mask',[]):
        for M in (up,dn,cand): M[y0:y1,x0:x1]=False
        bridge[y0:y1,x0:x1]=True
    if verbose: print('pitch',round(p,3),'max resid',round(abs(res).max(),2), 'gridrows',hg)
    goff=cfg.get('goff',None)  # offset from gridline to candle center
    colhas=cand[p_top:p_bot+1,:].any(axis=0); colhas[:X0]=False; colhas[X1:]=False
    runs=cluster([x for x in range(Ww) if colhas[x]])
    # predicted centers
    if goff is None: goff=(p-1.75)/2
    pc=np.array([x0+p*i+goff for i in range(len(days))])
    assign={}
    for ru in runs:
        # split long runs
        pieces=[ru]
        if len(ru)>6:
            pieces=[]
            for i in range(len(days)):
                lo=pc[i]-p/2; hi=pc[i]+p/2
                sub=[x for x in ru if lo<=x<hi]
                if sub: pieces.append(sub)
        for pc_ in pieces:
            c=np.mean(pc_); i=int(np.argmin(abs(pc-c)))
            if abs(pc[i]-c)<=p/2: assign.setdefault(i,[]).extend(pc_)
    recs=[]
    sub=slice(p_top,p_bot+1)
    for i,d in enumerate(days):
        if i not in assign:
            if pc[i]>=X0 and pc[i]<X1 and i>=min(assign) and i<=max(assign):
                recs.append(dict(date=d.isoformat(),missing=True))
            continue
        cols=sorted(set(assign[i])); w=len(cols)
        cm=cand[sub][:,cols]; cnt=cm.sum(axis=1)
        full=cnt>=max(w-1,1) if w>=3 else cnt>=w
        nonwhite=(~white[sub][:,cols]).sum(axis=1)>=max(w-1,1)
        bseg=segs(full, nonwhite, maxgap=3)
        # wick column = column with max pixel count
        wc=cols[int(np.argmax(cm.sum(axis=0)))] if w<3 else cols[int(np.argmax(cm[:, :].sum(axis=0)))]
        wseg=segs(cand[sub,wc], bridge[sub,wc], maxgap=3)
        if not bseg and not wseg: recs.append(dict(date=d.isoformat(),missing=True)); continue
        if bseg:
            bs=max(bseg,key=lambda s:(cm[s[0]:s[1]+1].sum()))
        else:
            s=max(wseg,key=lambda s:s[1]-s[0]); m=(s[0]+s[1])//2; bs=[m,m]
        ws=[s for s in wseg if not (s[1]<bs[0]-1 or s[0]>bs[1]+1)]
        hi=min([bs[0]]+[s[0] for s in ws]); lo=max([bs[1]]+[s[1] for s in ws])
        ys=slice(p_top+bs[0],p_top+bs[1]+1)
        nu=up[ys][:,cols].sum(); nd=dn[ys][:,cols].sum()
        color='up' if nu>=nd else 'dn'
        # volume
        vtop=None
        cc=cols[len(cols)//2]
        colc=[c_ for c_ in cols if 0<=c_<Ww]
        y=v_bot
        # skip baseline/non-candle rows at the very bottom
        while y>v_top and not cand[y,colc].any() and (v_bot-y)<4: y-=1
        top=None
        while y>v_top:
            if cand[y,colc].any(): top=y; y-=1; continue
            if (~white[y,colc]).all(): y-=1; continue
            # allow 1-2 px bridge of partially non-white (MA lines)
            if (~white[y,colc]).any() and (~white[y-1,colc]).any(): y-=1; continue
            break
        vtop=top
        recs.append(dict(date=d.isoformat(),x=float(np.mean(cols)),w=w,color=color,
                         hi=p_top+hi,lo=p_top+lo,b0=p_top+bs[0],b1=p_top+bs[1],vtop=vtop))
    # volume calibration
    vgr=rows_of(A[v_top:v_bot+1],(233,233,233),10,840,0.4)
    vgr=[c[0]+v_top for c in cluster(vgr)]
    if cfg.get('vgridrows'): vgr=cfg['vgridrows']
    va,vb=np.polyfit(vgr[:len(cfg['vgridvals'])],cfg['vgridvals'],1); vpp=-va; zero=vb/vpp
    P=lambda y:a*y+b
    out=[]
    for q in recs:
        if q.get('missing'): out.append(q); continue
        top,bot=P(q['b0']),P(q['b1'])
        op,cl=(bot,top) if q['color']=='up' else (top,bot)
        v=(zero-q['vtop']+0.5)*vpp if q['vtop'] is not None else 0
        out.append(dict(date=q['date'],o=op,h=P(q['hi']),l=P(q['lo']),c=cl,v=max(v,0),x=q['x'],w=q['w'],color=q['color']))
    ok=[q for q in out if not q.get('missing')]
    info=dict(P=(a,b),zero=zero,vpp=vpp,p_top=p_top,p_bot=p_bot,v_top=v_top,v_bot=v_bot,pitch=p)
    if verbose:
        H=max(ok,key=lambda q:q['h']); L=min(ok,key=lambda q:q['l'])
        print('N',len(ok),ok[0]['date'],'→',ok[-1]['date'],'missing',[q['date'] for q in out if q.get('missing')])
        print(' HIGH',H['date'],round(H['h'],2),'| text',cfg['high'],cfg['high_date'])
        print(' LOW ',L['date'],round(L['l'],2),'| text',cfg['low'],cfg['low_date'])
        print(' LAST',ok[-1]['date'],'o',round(ok[-1]['o'],2),'h',round(ok[-1]['h'],2),'l',round(ok[-1]['l'],2),'c',round(ok[-1]['c'],2),'| text cur',cfg['cur'])
        print(' px/price',round(a,4),' vol/px',round(vpp,1))
    return A,out,info

def compare(A,recs,info,fn,scale=2,crop=None):
    H,W=A.shape[:2]
    rec=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(rec)
    a,b=info['P']; Y=lambda p:(p-b)/a
    for q in recs:
        if q.get('missing'): continue
        x=q['x']; col=(220,2,2) if q['color']=='up' else (0,1,200); hw=(q['w']-1)/2
        d.line([(x,Y(q['h'])),(x,Y(q['l']))],fill=col)
        d.rectangle([x-hw,Y(max(q['o'],q['c'])),x+hw,Y(min(q['o'],q['c']))],fill=col)
        d.rectangle([x-hw,info['zero']-q['v']/info['vpp'],x+hw,info['zero']],fill=col)
    orig=Image.fromarray(A.astype('uint8'))
    if crop: orig=orig.crop(crop); rec=rec.crop(crop)
    w,h=orig.size
    out=Image.new('RGB',(w,h*2+4),'black'); out.paste(orig,(0,0)); out.paste(rec,(0,h+4))
    out.resize((w*scale,(h*2+4)*scale),Image.NEAREST).save(fn)
