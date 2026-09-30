import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
for w in ['Regular','Medium','SemiBold','Bold','Light']:
    fm.fontManager.addfont(f'/root/.fonts/Pretendard-{w}.ttf')
plt.rcParams['font.family']='Pretendard'
NAVY='#0b1f5c'; UPC='#c0392b'; DNC='#12457d'; GRID='#ececec'; GRAY='#6f6f6f'; AX='#b5b5b5'
MAC={'ma5':'#e05a50','ma20':'#a855c8','ma60':'#4a90d9','ma120':'#8c8c8c','ma7':'#e05a50','ma25':'#a855c8','ma99':'#4a90d9'}
W_PT,H_PT=400,172
def fmt_price(v,dec): return f'{v:,.0f}' if dec==0 else f'{v:,.{dec}f}'
def fmt_vol(v):
    if v>=1e8: return f'{v/1e8:,.1f}억'.replace('.0억','억')
    if v>=1e4: return f'{v/1e4:,.0f}만'
    return f'{v:,.0f}'
def place_label(ax,fig,lab,y,va,color,h,l,n,prefer='right',fs=5.7):
    t=ax.text(0,y,lab,color=color,fontsize=fs,fontweight='bold',ha='left',va=va,zorder=9,
              bbox=dict(boxstyle='square,pad=0.12',fc='white',ec='none',alpha=0.88))
    fig.canvas.draw(); r=fig.canvas.get_renderer()
    bb=t.get_window_extent(r).transformed(ax.transData.inverted())
    w=bb.x1-bb.x0; y0,y1=bb.y0,bb.y1
    cands=[n*0.93-w-k*(n/60) for k in range(60)] if prefer!='left' else [1+k*(n/60) for k in range(60)]
    best=None
    for x0 in cands:
        if x0<0.5 or x0+w>n*0.935: continue
        i0=max(int(np.floor(x0-0.5)),0); i1=min(int(np.ceil(x0+w+0.5)),n-1)
        ov=int(((h[i0:i1+1]>=y0)&(l[i0:i1+1]<=y1)).sum())
        if best is None or ov<best[0]: best=(ov,x0)
        if ov==0: break
    t.set_x(best[1] if best else n*0.985-w); return t
def render(name,title,code,out,dec=0,mas=('ma5','ma20','ma60','ma120'),ma_labels=('5','20','60','120'),
           bands=(),lines=(),chg=None,band_side='right',h_pt=H_PT,partial_last_vol=True,cur_label=None):
    d=json.load(open(f'd930/data_{name}.json')); bars=d['bars']; p930=d.get('p930')
    n=len(bars); x=np.arange(n)
    o,h,l,c,v=(np.array([b[k] for b in bars]) for k in 'ohlcv')
    dates=[b['date'] for b in bars]
    fig=plt.figure(figsize=(W_PT/72,h_pt/72),dpi=450)
    top=1-12.5/h_pt; volh=31/h_pt; xlab=9.5/h_pt
    vb=xlab; sep=vb+volh+4/h_pt; pb=sep+3/h_pt
    R=1-(33 if dec<4 else (40 if dec<6 else 47))/W_PT
    axp=fig.add_axes([0.003,pb,R-0.003,top-pb]); axv=fig.add_axes([0.003,vb,R-0.003,volh],sharex=axp)
    for ax in (axp,axv):
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.tick_right(); ax.tick_params(axis='y',length=0,labelsize=5.4,labelcolor=GRAY,pad=3)
        ax.grid(axis='y',color=GRID,lw=0.45); ax.set_axisbelow(True)
    axp.tick_params(axis='x',length=0,labelbottom=False)
    up=c>=o; bw=0.66 if n<200 else 0.72; lw=0.42 if n<200 else 0.36
    rng=h.max()-l.min()
    for i in range(n):
        col=UPC if up[i] else DNC
        axp.vlines(i,l[i],h[i],color=col,lw=lw,zorder=3)
        bot=min(o[i],c[i]); ht=max(abs(c[i]-o[i]),rng*0.0015)
        axp.add_patch(Rectangle((i-bw/2,bot),bw,ht,facecolor=col,edgecolor=col,lw=0.1,zorder=3))
    xe=x.tolist()
    for k in mas:
        if k in d:
            arr=[np.nan if q is None else q for q in (d.get(k+'_traced') or d[k])]
            xs=list(x); ys=list(arr)
            if p930: xs.append(n); ys.append(p930['ma'][k])
            axp.plot(xs,ys,color=MAC[k],lw=0.7 if k!='ma120' else 0.8,zorder=4,alpha=0.95)
    lo_,hi_=l.min(),h.max()
    axp.set_ylim(lo_-rng*0.12,hi_+rng*0.13)
    last_x=n if p930 else n-1
    axp.set_xlim(-1,last_x+max(n*0.155,20))
    axp.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda val,pos: fmt_price(val,dec)))
    axp.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    for (b0,b1,lab) in bands:
        axp.axhspan(b0,b1,color='#fbeaea',zorder=1,lw=0)
        for yy in (b0,b1): axp.axhline(yy,color=UPC,lw=0.45,ls=(0,(3,2)),zorder=2)
        place_label(axp,fig,lab,b1,'bottom',UPC,h,l,n,prefer=band_side)
    for (val,lab,side) in lines:
        axp.axhline(val,color=NAVY,lw=0.5,ls=(0,(1,1.3)),zorder=2)
        place_label(axp,fig,lab,val,'top',NAVY,h,l,n,prefer=side)
    iH=int(np.argmax(h)); iL=int(np.argmin(l)); dd=lambda s: s.replace('-','.')
    def ha(i): return 'center' if 0.12<i/n<0.85 else ('left' if i/n<=0.12 else 'right')
    axp.plot(iH,h[iH]+rng*0.012,'o',ms=2.3,color=UPC,zorder=7)
    axp.text(iH,h[iH]+rng*0.04,f'{fmt_price(h[iH],dec)}  {dd(dates[iH])}',color=UPC,fontsize=5.8,fontweight='bold',ha=ha(iH),va='bottom',zorder=7)
    axp.plot(iL,l[iL]-rng*0.012,'o',ms=2.3,color=NAVY,zorder=7)
    axp.text(iL,l[iL]-rng*0.04,f'{fmt_price(l[iL],dec)}  {dd(dates[iL])}',color=NAVY,fontsize=5.8,fontweight='bold',ha=ha(iL),va='top',zorder=7)
    if p930:
        cc=UPC if not p930['chg'].startswith('-') else DNC
        if p930['chg'].startswith('0.00'): cc=GRAY
        axp.plot([n-0.45,n+0.45],[p930['c']]*2,color=cc,lw=1.3,zorder=8,solid_capstyle='butt')
        axp.plot(n,p930['c'],'o',ms=2.8,mfc='white',mec=cc,mew=0.8,zorder=9)
        axp.text(n+1.0,p930['c'],f"{fmt_price(p930['c'],dec)}\n9/30 {p930['chg']}",color=cc,fontsize=6.0,fontweight='bold',ha='left',va='center',zorder=9,linespacing=1.05,bbox=dict(boxstyle='square,pad=0.1',fc='white',ec='none',alpha=0.8))
    else:
        isup=(not chg.startswith('-')) if chg else c[-1]>=c[-2]
        cc=UPC if isup else DNC
        axp.plot(n-1,c[-1],'o',ms=2.6,color=cc,zorder=8)
        axp.text(n+0.6,c[-1],(cur_label or fmt_price(c[-1],dec))+(f'\n{chg}' if chg else ''),color=cc,fontsize=6.0,fontweight='bold',ha='left',va='center',zorder=8,linespacing=1.05,bbox=dict(boxstyle='square,pad=0.1',fc='white',ec='none',alpha=0.8))
    cols=[UPC if u else DNC for u in up]
    axv.bar(x[:-1],v[:-1],width=bw,color=cols[:-1],lw=0,zorder=3)
    if partial_last_vol: axv.bar([x[-1]],[v[-1]],width=bw,color='white',edgecolor=cols[-1],lw=0.35,hatch='//////',zorder=3)
    else: axv.bar([x[-1]],[v[-1]],width=bw,color=cols[-1],lw=0,zorder=3)
    vm=np.array([v[max(0,i-19):i+1].mean() if i>=19 else np.nan for i in range(n)])
    axv.plot(x[:-1],vm[:-1],color='#a855c8',lw=0.55,zorder=4)
    axv.set_ylim(0,v.max()*1.1)
    axv.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(3))
    axv.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda val,pos: fmt_vol(val) if val>0 else '0'))
    axv.text(0.003,0.97,'거래량',transform=axv.transAxes,fontsize=5.2,color=GRAY,va='top')
    fig.add_artist(Line2D([0.003,R],[sep-1.5/h_pt]*2,color=AX,lw=0.45))
    ticks=np.linspace(0,n-1,6).round().astype(int)
    axv.set_xticks(ticks); lb=axv.set_xticklabels([dates[t][2:].replace('-','/') for t in ticks],fontsize=5.3,color=GRAY)
    lb[0].set_ha('left'); lb[-1].set_ha('right'); axv.tick_params(axis='x',length=0,pad=2)
    yT=1-6/h_pt
    t0=fig.text(0.004,yT,title,fontsize=7.6,fontweight='bold',color=NAVY,va='center')
    fig.canvas.draw(); bb=t0.get_window_extent(fig.canvas.get_renderer())
    fig.text(bb.x1/fig.bbox.width+0.008,yT,code,fontsize=5.8,color=GRAY,va='center')
    lx=R-0.33
    fig.text(lx,yT,'이동평균',fontsize=5.4,color=GRAY,va='center'); lx+=0.052
    for k,lab_ in zip(mas,ma_labels):
        fig.add_artist(Line2D([lx,lx+0.028],[yT]*2,color=MAC[k],lw=0.9)); fig.text(lx+0.033,yT,lab_,fontsize=5.4,color=GRAY,va='center'); lx+=0.066
    fig.savefig(out,dpi=450,facecolor='white'); plt.close(fig)
