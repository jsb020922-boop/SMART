import numpy as np, json, sys
from PIL import Image, ImageDraw
import cal

UP=(220,2,2); DN=(0,1,200)
def near(A,c,tol=12):
    return (np.abs(A-np.array(c)).max(axis=2)<=tol)

def rows_of(A,color,x0,x1,thr,tol=3):
    m=(np.abs(A[:,x0:x1,:].astype(int)-np.array(color)).max(axis=2)<=tol).mean(axis=1)
    return [y for y,v in enumerate(m) if v>thr]

def cluster(v,gap=1):
    out=[];cur=[]
    for x in v:
        if cur and x-cur[-1]>gap: out.append(cur);cur=[]
        cur.append(x)
    if cur: out.append(cur)
    return out

def segs(col_mask, bridge_ok, maxgap=4):
    """vertical segments of True in col_mask, bridging gaps where bridge_ok (non-white non-candle) up to maxgap"""
    ys=np.where(col_mask)[0]
    if len(ys)==0: return []
    out=[[ys[0],ys[0]]]
    for y in ys[1:]:
        if y-out[-1][1]<=1: out[-1][1]=y; continue
        g=range(out[-1][1]+1,y)
        if y-out[-1][1]-1<=maxgap and all(bridge_ok[k] for k in g): out[-1][1]=y
        else: out.append([y,y])
    return out

def digitize(cfg):
    A=np.array(Image.open(cfg['img']).convert('RGB')).astype(int)
    H,W,_=A.shape
    sep=rows_of(A,(204,204,204),10,840,0.9)
    # panel boundaries: price panel between first two separators, volume between 2nd and 3rd
    sep=[s for s in sep]
    p_top,p_bot=sep[0]+1,sep[1]-1
    v_top=sep[1]+1; v_bot=[s for s in sep if s>v_top+20][0]-1
    xr=cfg.get('xrange',(8,850))
    up=near(A,UP); dn=near(A,DN)
    white=(A.min(axis=2)>=245)
    cand=up|dn
    bridge=~white & ~cand
    for (x0,y0,x1,y1) in cfg.get('mask',[]):
        cand[y0:y1,x0:x1]=False; up[y0:y1,x0:x1]=False; dn[y0:y1,x0:x1]=False; bridge[y0:y1,x0:x1]=True
    # price-panel column profile
    prof=cand[p_top:p_bot+1, :].sum(axis=0)
    prof[:xr[0]]=0; prof[xr[1]:]=0
    # calendar
    days=cal.days(cfg['start_search'],cfg['last'],cfg['cal'],cfg.get('extra_hol',()))
    # grid from month-start vertical gridlines
    vg=[x for x in range(xr[0],xr[1]) if ((np.abs(A[p_top:p_bot,x,:]-np.array((233,233,233))).max(axis=1)<=3).mean()>0.3)]
    vg=[c[0] for c in cluster(vg)]
    return A,dict(p_top=p_top,p_bot=p_bot,v_top=v_top,v_bot=v_bot,vg=vg,prof=prof,up=up,dn=dn,bridge=bridge,cand=cand,days=days)

def nice_step(raw):
    import math
    e=10**math.floor(math.log10(raw)); 
    for m in [1,2,2.5,5,10]:
        if abs(raw/(m*e)-1)<0.2: return m*e
    return None

def extract(cfg, verbose=True):
    A,r=digitize(cfg)
    p_top,p_bot,v_top,v_bot=r['p_top'],r['p_bot'],r['v_top'],r['v_bot']
    up,dn,cand,bridge=r['up'],r['dn'],r['cand'],r['bridge']
    days=r['days']; idx={d.isoformat():i for i,d in enumerate(days)}
    # month-first gridlines -> calendar index
    firsts={}
    for i,d in enumerate(days): firsts.setdefault((d.year,d.month),i)
    vg=[x for x in r['vg'] if x>cfg.get('xrange',(8,850))[0]+3]
    # assign each gridline to month-first by order: last gridline = month of last day
    fi=sorted(firsts.values())
    fi=fi[-len(vg):] if cfg.get('vg_months') is None else [firsts[m] for m in cfg['vg_months']]
    X=np.array(vg,float); I=np.array(fi,float)
    p,x0=np.polyfit(I,X,1)
    res=X-(x0+p*I)
    bw=cfg.get('bw',5); off=(bw-1)//2
    if verbose: print('pitch',round(p,3),'resid',np.round(res,2))
    out=[]
    for i,d in enumerate(days):
        L=int(round(x0+p*i)); c=L+off
        if L<cfg.get('xrange',(8,850))[0] or c>=cfg.get('xrange',(8,850))[1]: continue
        sub=slice(p_top,p_bot+1)
        body_cols=[c+k for k in range(-off,bw-off) if k!=0]
        bm=np.zeros(p_bot-p_top+1,bool)
        cols=[cand[sub,x] for x in body_cols]
        if cols:
            both=np.logical_and.reduce([cols[0],cols[-1]]) if len(cols)>=2 else cols[0]
            bm=both
        bseg=segs(bm, bridge[sub,c], maxgap=4)
        wseg=segs(cand[sub,c], bridge[sub,c], maxgap=4)
        if bseg:
            bs=max(bseg,key=lambda s:s[1]-s[0])
        elif wseg:
            bs=None
        else:
            out.append(dict(date=d.isoformat(),missing=True)); continue
        if bs is not None:
            ws=[s for s in wseg if not (s[1]<bs[0]-1 or s[0]>bs[1]+1)]
            hi=min([bs[0]]+[s[0] for s in ws]); lo=max([bs[1]]+[s[1] for s in ws])
            ys=slice(p_top+bs[0],p_top+bs[1]+1)
            nu=up[ys,body_cols].sum(); nd=dn[ys,body_cols].sum()
            color='up' if nu>=nd else 'dn'
            b0,b1=bs
        else:
            s=max(wseg,key=lambda s:s[1]-s[0]); hi,lo=s
            ys=slice(p_top+hi,p_top+lo+1); color='up' if up[ys,c].sum()>=dn[ys,c].sum() else 'dn'
            b0=b1=(hi+lo)//2
        # volume bar
        vsub=slice(v_top,v_bot+1)
        vcols=[x for x in range(c-off,c-off+bw)]
        vm=cand[vsub][:,vcols].any(axis=1)
        vys=np.where(vm)[0]
        vtop=(v_top+vys.min()) if len(vys) else None
        out.append(dict(date=d.isoformat(),x=c,color=color,hi=p_top+hi,lo=p_top+lo,b0=p_top+b0,b1=p_top+b1,vtop=vtop))
    # price calibration via gridlines
    hg=rows_of(A[p_top:p_bot+1],(233,233,233),10,840,0.5)
    hg=[c[0]+p_top for c in cluster(hg)]
    ok=[o for o in out if not o.get('missing')]
    ymin=min(o['hi'] for o in ok); ymax=max(o['lo'] for o in ok)
    a=(cfg['high']-cfg['low'])/(ymin-ymax); b=cfg['high']-a*ymin
    est=[a*y+b for y in hg]
    step=nice_step(abs(est[1]-est[0])) if len(est)>1 else None
    if step and len(hg)>=2:
        vals=[round(e/step)*step for e in est]
        a2,b2=np.polyfit(hg,vals,1)
    else:
        a2,b2=a,b; vals=est
    if verbose:
        print('gridrows',hg,'vals',vals,'step',step)
        print('anchor fit a,b',round(a,2),round(b,1),' grid fit',round(a2,2),round(b2,1))
    P=lambda y: a2*y+b2
    # volume calibration
    vgr=rows_of(A[v_top:v_bot+1],(233,233,233),10,840,0.4)
    vgr=[c[0]+v_top for c in cluster(vgr)]
    vstep=cfg['vstep']
    if len(vgr)>=2:
        sp=np.mean(np.diff(vgr)); zero=vgr[-1]+sp
    else:
        sp=None; zero=v_bot
    vpp=vstep/sp if sp else None
    if verbose: print('vol grid',vgr,'zero',round(zero,1),'per px',vpp)
    recs=[]
    for o in out:
        if o.get('missing'): recs.append(dict(date=o['date'],missing=True)); continue
        top,bot=P(o['b0']),P(o['b1'])
        if o['color']=='up': op,cl=bot,top
        else: op,cl=top,bot
        vol=(zero-o['vtop'])*vpp if (o['vtop'] is not None and vpp) else 0
        recs.append(dict(date=o['date'],o=op,h=P(o['hi']),l=P(o['lo']),c=cl,v=max(vol,0),x=o['x'],color=o['color']))
    ok=[q for q in recs if not q.get('missing')]
    H=max(ok,key=lambda q:q['h']); Lw=min(ok,key=lambda q:q['l'])
    if verbose:
        print('N',len(ok),'first',ok[0]['date'],'last',ok[-1]['date'],'missing',[q['date'] for q in recs if q.get('missing')])
        print('HIGH',H['date'],round(H['h']),'vs',cfg['high'],cfg.get('high_date'))
        print('LOW ',Lw['date'],round(Lw['l']),'vs',cfg['low'],cfg.get('low_date'))
        print('LAST close',round(ok[-1]['c']),'vs',cfg.get('cur'))
    return A,r,recs,dict(P=(a2,b2),zero=zero,vpp=vpp)

def auto_masks(cfg):
    """mask the candle-colored 최고/최저 annotation text next to the extreme candles"""
    A,r=digitize(cfg)
    p_top,p_bot=r['p_top'],r['p_bot']
    cand=r['cand']; days=r['days']
    firsts={}
    for i,d in enumerate(days): firsts.setdefault((d.year,d.month),i)
    vg=[x for x in r['vg'] if x>cfg.get('xrange',(8,850))[0]+3]
    fi=sorted(firsts.values())[-len(vg):]
    p,x0=np.polyfit(np.array(fi,float),np.array(vg,float),1)
    bw=cfg.get('bw',5); off=(bw-1)//2
    hg=rows_of(A[p_top:p_bot+1],(233,233,233),10,840,0.5)
    hg=[c[0]+p_top for c in cluster(hg)]
    vals=cfg['gridvals']
    a,b=np.polyfit(hg[:len(vals)],vals,1)
    idx={d.isoformat():i for i,d in enumerate(days)}
    masks=[]
    for key in ['high','low']:
        y=int(round((cfg[key]-b)/a)); i=idx[cfg[key+'_date']]
        xc=int(round(x0+p*i))+off
        y0,y1=y-8,y+8
        band=cand[max(y0,p_top):y1,:]
        dens=band.any(axis=0)
        best=None
        for side in (+1,-1):
            x=xc+side*(off+2); last=x; empty=0; n=0
            while 0<=x<cfg.get('xrange',(8,850))[1]+60 and x<A.shape[1]-60 and empty<22:
                if dens[x]: last=x; empty=0; n+=1
                else: empty+=1
                x+=side
            if n>40 and (best is None or n>best[0]): best=(n,side,last)
        if best:
            n,side,last=best
            xa=xc+side*(off+1)
            x_lo,x_hi=(xa,last+1) if side>0 else (last,xa+1)
            masks.append((x_lo,max(y0,p_top),x_hi,y1))
    return masks

def overlay(A,recs,cal,fn,scale=3,crop=None):
    from PIL import Image,ImageDraw
    im=Image.fromarray(A.astype('uint8')).resize((A.shape[1]*scale,A.shape[0]*scale),Image.NEAREST)
    d=ImageDraw.Draw(im)
    a,b=cal['P']
    Y=lambda p:(p-b)/a*scale
    for q in recs:
        if q.get('missing'): continue
        x=(q['x']+0.5)*scale+ (3*scale)
        col=(0,170,0) if q['color']=='up' else (255,140,0)
        d.line([(x,Y(q['h'])),(x,Y(q['l']))],fill=col,width=1)
        d.rectangle([x-2,Y(max(q['o'],q['c'])),x+2,Y(min(q['o'],q['c']))],outline=col)
        if cal['vpp']:
            vy=(cal['zero']-q['v']/cal['vpp'])*scale
            d.line([(x-2,vy),(x+2,vy)],fill=(0,170,0),width=2)
    if crop: im=im.crop([c*scale for c in crop])
    im.save(fn)

def compare(A,recs,cal,fn,scale=2,crop=None):
    from PIL import Image,ImageDraw
    H,W=A.shape[:2]
    rec=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(rec)
    a,b=cal['P']; Y=lambda p:(p-b)/a
    for q in recs:
        if q.get('missing'): continue
        x=q['x']; col=(220,2,2) if q['color']=='up' else (0,1,200)
        d.line([(x,Y(q['h'])),(x,Y(q['l']))],fill=col)
        d.rectangle([x-2,Y(max(q['o'],q['c'])),x+2,Y(min(q['o'],q['c']))],fill=col)
        if cal['vpp']:
            d.rectangle([x-2,cal['zero']-q['v']/cal['vpp'],x+2,cal['zero']],fill=col)
    orig=Image.fromarray(A.astype('uint8'))
    if crop: orig=orig.crop(crop); rec=rec.crop(crop)
    w,h=orig.size
    out=Image.new('RGB',(w,h*2+4),'black'); out.paste(orig,(0,0)); out.paste(rec,(0,h+4))
    out=out.resize((w*scale,(h*2+4)*scale),Image.NEAREST)
    out.save(fn)
