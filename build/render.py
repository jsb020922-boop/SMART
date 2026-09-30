import json, numpy as np, datetime as dt
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
for w in ['Regular','Medium','SemiBold','Bold','Light']:
    fm.fontManager.addfont(f'/root/.fonts/Pretendard-{w}.ttf')
plt.rcParams['font.family']='Pretendard'
NAVY='#0b1f5c'; UPC='#c0392b'; DNC='#12457d'; GRID='#eeeeee'; GRAY='#7a7a7a'; AX='#aeaeae'
MAC={'ma5':'#e05a50','ma20':'#a855c8','ma60':'#4a90d9','ma120':'#8c8c8c','ma7':'#e05a50','ma25':'#a855c8','ma99':'#4a90d9'}

def fmt_price(v,dec):
    if dec==0: return f'{v:,.0f}'
    return f'{v:,.{dec}f}'
def fmt_vol(v):
    if v>=1e8: return f'{v/1e8:,.1f}억'.replace('.0억','억')
    if v>=1e4: return f'{v/1e4:,.0f}만'
    return f'{v:,.0f}'


def place_label(ax,fig,lab,y,va,color,h,l,n,prefer='right'):
    """place label next to a horizontal level where it overlaps the fewest candles"""
    t=ax.text(0,y,lab,color=color,fontsize=7.3,fontweight='bold',ha='left',va=va,zorder=9,
              bbox=dict(boxstyle='square,pad=0.15',fc='white',ec='none',alpha=0.85))
    fig.canvas.draw(); r=fig.canvas.get_renderer()
    bb=t.get_window_extent(r).transformed(ax.transData.inverted())
    w=bb.x1-bb.x0; y0,y1=bb.y0,bb.y1
    cands=[n*0.985-w - k*(n/60) for k in range(0,60)]
    if prefer=='left': cands=[1+k*(n/60) for k in range(0,60)]
    best=None
    for x0 in cands:
        if x0<0.5 or x0+w>n*0.99: continue
        i0=max(int(np.floor(x0-0.5)),0); i1=min(int(np.ceil(x0+w+0.5)),n-1)
        ov=int(((h[i0:i1+1]>=y0)&(l[i0:i1+1]<=y1)).sum())
        if best is None or ov<best[0]: best=(ov,x0)
        if ov==0: break
    t.set_x(best[1] if best else (n*0.985-w))
    return t

def render(name, title, code, out, dec=0, mas=('ma5','ma20','ma60','ma120'), ma_labels=('5','20','60','120'),
           bands=(), lines=(), chg=None, vol_unit='주', src_ma='traced', ylim=None, hi_label_side='auto', lo_label_side='auto',
           cur_up=None, extra_marks=(), band_side='right'):
    d=json.load(open(f'data_{name}.json')); bars=d['bars']
    n=len(bars); x=np.arange(n)
    o=np.array([b['o'] for b in bars]); h=np.array([b['h'] for b in bars]); l=np.array([b['l'] for b in bars]); c=np.array([b['c'] for b in bars]); v=np.array([b['v'] for b in bars])
    dates=[b['date'] for b in bars]
    fig=plt.figure(figsize=(8.55,4.35),dpi=200)
    axp=fig.add_axes([0.012,0.315,0.885,0.585]); axv=fig.add_axes([0.012,0.08,0.885,0.185],sharex=axp)
    for ax in (axp,axv):
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.tick_right(); ax.tick_params(axis='y',length=0,labelsize=7.2,labelcolor=GRAY,pad=4)
        ax.grid(axis='y',color=GRID,lw=0.7); ax.set_axisbelow(True)
    axp.tick_params(axis='x',length=0,labelbottom=False)
    up=c>=o
    bw=0.62 if n<200 else 0.7
    lw=0.55 if n<200 else 0.45
    for i in range(n):
        col=UPC if up[i] else DNC
        axp.vlines(i,l[i],h[i],color=col,lw=lw,zorder=3)
        bot=min(o[i],c[i]); ht=max(abs(c[i]-o[i]), (h.max()-l.min())*0.0012)
        axp.add_patch(Rectangle((i-bw/2,bot),bw,ht,facecolor=col,edgecolor=col,lw=0.2,zorder=3))
    for k in mas:
        if k in d:
            arr=np.array([np.nan if q is None else q for q in (d.get(k+'_traced') or d[k])],float) if src_ma=='traced' else np.array([np.nan if q is None else q for q in d[k]],float)
            axp.plot(x,arr,color=MAC[k],lw=1.0 if k!='ma120' else 1.1,zorder=4,alpha=0.95)
    lo_,hi_=l.min(),h.max(); rng=hi_-lo_
    if ylim: axp.set_ylim(*ylim)
    else: axp.set_ylim(lo_-rng*0.13, hi_+rng*0.14)
    axp.set_xlim(-1.5,n+ (n*0.075))
    axp.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda val,pos: fmt_price(val,dec)))
    axp.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    # bands / lines
    for (b0,b1,lab) in bands:
        axp.axhspan(b0,b1,color='#fbeaea',zorder=1,lw=0)
        axp.axhline(b0,color=UPC,lw=0.6,ls=(0,(3,2)),zorder=2); axp.axhline(b1,color=UPC,lw=0.6,ls=(0,(3,2)),zorder=2)
        place_label(axp,fig,lab,b1,'bottom',UPC,h,l,n,prefer=band_side)
    for (val,lab,side) in lines:
        axp.axhline(val,color=NAVY,lw=0.7,ls=(0,(1,1.4)),zorder=2)
        place_label(axp,fig,lab,val,'top',NAVY,h,l,n,prefer=side)
    # high / low
    iH=int(np.argmax(h)); iL=int(np.argmin(l))
    def dd(s): return s.replace('-','.')
    axp.plot(iH,h[iH]+rng*0.012,'o',ms=3.2,color=UPC,zorder=7)
    axp.text(iH,h[iH]+rng*0.045,f'{fmt_price(h[iH],dec)}  {dd(dates[iH])}',color=UPC,fontsize=7.6,fontweight='bold',ha='center' if 0.12<iH/n<0.85 else ('left' if iH/n<=0.12 else 'right'),va='bottom',zorder=7)
    axp.plot(iL,l[iL]-rng*0.012,'o',ms=3.2,color=NAVY,zorder=7)
    axp.text(iL,l[iL]-rng*0.045,f'{fmt_price(l[iL],dec)}  {dd(dates[iL])}',color=NAVY,fontsize=7.6,fontweight='bold',ha='center' if 0.12<iL/n<0.85 else ('left' if iL/n<=0.12 else 'right'),va='top',zorder=7)
    for (i_,val,lab,colr) in extra_marks:
        axp.annotate(lab,(i_,val),xytext=(0,-14),textcoords='offset points',ha='center',fontsize=6.6,color=colr,fontweight='bold',arrowprops=dict(arrowstyle='-',color=colr,lw=0.6))
    # current
    isup=cur_up if cur_up is not None else ((not chg.startswith('-')) if chg else c[-1]>=c[-2])
    cc=UPC if isup else DNC
    axp.plot(n-1,c[-1],'o',ms=3.4,color=cc,zorder=8)
    lab=fmt_price(c[-1],dec)+(f'\n{chg}' if chg else '')
    axp.text(n+0.8,c[-1],lab,color=cc,fontsize=8.2,fontweight='bold',ha='left',va='center',zorder=8,linespacing=1.05)
    # volume
    axv.bar(x,v,width=bw,color=[UPC if u else DNC for u in up],lw=0,zorder=3)
    vm=np.array([v[max(0,i-19):i+1].mean() if i>=19 else np.nan for i in range(n)])
    axv.plot(x,vm,color='#a855c8',lw=0.8,zorder=4)
    axv.set_ylim(0,v.max()*1.12)
    axv.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(3))
    axv.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda val,pos: fmt_vol(val) if val>0 else '0'))
    axv.text(0.004,0.97,'거래량',transform=axv.transAxes,fontsize=7,color=GRAY,va='top')
    # separator
    fig.add_artist(matplotlib.lines.Line2D([0.012,0.897],[0.295,0.295],color=AX,lw=0.6))
    # x labels
    ticks=np.linspace(0,n-1,5).round().astype(int)
    axv.set_xticks(ticks); lbls=axv.set_xticklabels([dates[t][2:].replace('-','/') for t in ticks],fontsize=7,color=GRAY)
    lbls[0].set_ha('left'); lbls[-1].set_ha('right')
    axv.tick_params(axis='x',length=0,pad=3)
    # title & legend
    fig.text(0.014,0.952,title,fontsize=11.5,fontweight='bold',color=NAVY,va='center')
    tw=fig.text(0,0,'');
    r=fig.canvas.get_renderer(); t0=fig.texts[0]; bb=t0.get_window_extent(r); xr=bb.x1/fig.bbox.width
    fig.text(xr+0.008,0.952,code,fontsize=8.5,color=GRAY,va='center')
    lx=0.60
    fig.text(lx,0.955,'이동평균',fontsize=7,color=GRAY,va='center'); lx+=0.055
    for k,lab_ in zip(mas,ma_labels):
        fig.add_artist(matplotlib.lines.Line2D([lx,lx+0.03],[0.955,0.955],color=MAC[k],lw=1.2)); fig.text(lx+0.035,0.955,lab_,fontsize=7,color=GRAY,va='center'); lx+=0.07
    fig.savefig(out,dpi=200,facecolor='white'); plt.close(fig)
    return dict(n=n,last=c[-1],hi=(dates[iH],h[iH]),lo=(dates[iL],l[iL]))
if __name__=='__main__':
    print(render('sksquare','SK스퀘어','402340','t_sk.png',chg='+1.55%',bands=[(1000000*0.99,1010000,'')],lines=[]))
