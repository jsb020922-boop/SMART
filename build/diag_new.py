import json, numpy as np, datetime as dt
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
for w in ['Regular','Medium','SemiBold','Bold','Light']: fm.fontManager.addfont(f'/root/.fonts/Pretendard-{w}.ttf')
plt.rcParams.update({'font.family':'Pretendard','axes.linewidth':0.45,'axes.edgecolor':'#9a9a9a','xtick.color':'#6f6f6f','ytick.color':'#8a8a8a',
                     'xtick.labelsize':5.4,'ytick.labelsize':5.2,'hatch.linewidth':0.5})
NAVY='#0b1f5c'; MID='#12457d'; SLATE='#8fa3c9'; LS='#c9d3e3'; RED='#c0392b'; GRAY='#6f6f6f'; LG='#9a9a9a'; GRID='#ececec'
def fig(wpt,hpt): return plt.figure(figsize=(wpt/72,hpt/72),dpi=450)
def clean(ax,left=False):
    for s in ['top','right']+([] if left else ['left']): ax.spines[s].set_visible(False)
    ax.tick_params(length=0,pad=2); ax.grid(axis='y',color=GRID,lw=0.45); ax.set_axisbelow(True)
def ttl(f,x,y,t,u=None):
    f.text(x,y,t,fontsize=7.4,fontweight='bold',color=NAVY,va='top')
    if u: f.text(x,y-10.5/f.bbox.height*f.dpi/72*0+0,'',fontsize=1)
def load(k):
    d=json.load(open(f'd930/data_{k}.json')); dates=[dt.date.fromisoformat(b['date']) for b in d['bars']]; c=np.array([b['c'] for b in d['bars']])
    if d.get('p930'): dates.append(dt.date(2026,9,30)); c=np.append(c,d['p930']['c'])
    return dates,c
# ---------------- HD현대: 주가와 이익 추정치 괴리 (indexed line)
def hdhyundai(wpt=196,hpt=150):
    dates,c=load('hdhyundai'); base_i=dates.index(dt.date(2026,4,10)); idx=c/c[base_i]*100
    f=fig(wpt,hpt); H=hpt
    f.text(0.0,1-2/H,'주가와 2026년 이익 추정치',fontsize=7.4,fontweight='bold',color=NAVY,va='top')
    f.text(0.0,1-12.5/H,'(4월 10일 = 100, 주가는 일봉 종가)',fontsize=5.4,color=LG,va='top')
    ax=f.add_axes([0.01,22/H,0.80,1-60/H]); clean(ax)
    ax.yaxis.tick_right()
    x=np.array([(d-dates[0]).days for d in dates])
    ax.plot(x,idx,color=NAVY,lw=0.9,zorder=3)
    e_x=[(dt.date(2026,4,10)-dates[0]).days,(dt.date(2026,9,9)-dates[0]).days]; e_y=[100,137.78/81.42*100]
    ax.plot(e_x,e_y,color=RED,lw=0.9,ls=(0,(2.2,1.6)),zorder=4)
    ax.plot(e_x,e_y,'o',ms=3.2,color=RED,zorder=5)
    ax.text(e_x[0]+1,e_y[0]-9,'4/10 8.14조',fontsize=5.4,color=RED,fontweight='bold',va='top',ha='left')
    ax.text(e_x[1]-2,e_y[1]+4,'9/9  13.78조\n추정치 +69%',fontsize=5.6,color=RED,fontweight='bold',va='bottom',ha='right',linespacing=1.05)
    pk=int(np.argmax(c)); ax.plot(x[pk],idx[pk],'o',ms=2.4,color=NAVY,zorder=5)
    ax.text(x[pk]+3,idx[pk]+2,'5/4 고점',fontsize=5.2,color=NAVY,va='bottom')
    ax.plot(x[-1],idx[-1],'o',ms=2.8,mfc='white',mec=NAVY,mew=0.8,zorder=6)
    ax.text(x[-1]+3,idx[-1],f'9/30\n{idx[-1]:.0f}',fontsize=5.6,color=NAVY,fontweight='bold',va='center',ha='left',linespacing=1.0)
    ax.axhline(100,color=LG,lw=0.4,ls=(0,(1,1.3)))
    ax.set_ylim(60,190); ax.set_xlim(-3,x[-1]+28); ax.set_yticks([60,100,140,180])
    months=[dt.date(2026,m,1) for m in (4,5,6,7,8,9)]
    ax.set_xticks([(m-dates[0]).days for m in months]); ax.set_xticklabels([f'{m.month}월' for m in months])
    f.text(0.0,4/H,'이익 추정치 +69% 동안 주가는 고점 대비 -39.7%',fontsize=5.8,fontweight='bold',color=RED,va='bottom')
    f.savefig('diag2/hdhyundai_line.png',dpi=450,facecolor='white'); plt.close(f)
# ---------------- 이오테크닉스: 가격과 이익의 증가 속도 (slope chart)
def eotech(wpt=176,hpt=178):
    f=fig(wpt,hpt); H=hpt
    f.text(0.0,1-2/H,'가격과 이익의 증가 속도',fontsize=7.4,fontweight='bold',color=NAVY,va='top')
    f.text(0.0,1-12.5/H,'(각 기준 = 100)',fontsize=5.4,color=LG,va='top')
    ax=f.add_axes([0.02,40/H,0.60,1-66/H]); clean(ax); ax.grid(False); ax.spines['bottom'].set_visible(False)
    items=[('주가','7/29 저점 → 9/30',520000/230000*100,RED),('영업이익','',135,NAVY),('매출','',117,SLATE)]
    ax.set_xlim(-0.15,1.15); ax.set_ylim(80,240)
    ax.plot([0,0],[80,240],color='#d8dbe4',lw=0.6); ax.plot([1,1],[80,240],color='#d8dbe4',lw=0.6)
    for lab,sub,v,colr in items:
        ax.plot([0,1],[100,v],color=colr,lw=1.2 if colr!=SLATE else 1.0,zorder=3)
        ax.plot(1,v,'o',ms=3.3,color=colr,zorder=4)
        f.text(0.02+0.60*(1.15/1.3)+0.03, (40+(v-80)/160*(H-66))/H, f'{lab} {v:.0f}',fontsize=6.2,fontweight='bold',color=colr,va='center')
        if sub: f.text(0.02+0.60*(1.15/1.3)+0.03, (40+(v-80)/160*(H-66)-8)/H, sub,fontsize=5.0,color=GRAY,va='center')
    ax.plot(0,100,'o',ms=3.3,color=GRAY,zorder=4); ax.text(-0.05,100,'100',fontsize=5.6,color=GRAY,ha='right',va='center')
    f.text(0.02+0.60*(1.15/1.3)+0.03,(40+(117-80)/160*(H-66)-10)/H,'영업이익·매출:\n2025 → 최근 4개 분기',fontsize=5.0,color=GRAY,va='top',linespacing=1.1)
    ax.set_xticks([]); ax.set_yticks([])
    f.text(0.0,20/H,'영업이익률 21.2% → 24.6%',fontsize=6.0,fontweight='bold',color=NAVY,va='bottom')
    f.text(0.0,6/H,'가격 상승(+126%)이 이익 증가(+35%)보다 빠르다',fontsize=5.7,fontweight='bold',color=RED,va='bottom')
    f.savefig('diag2/eotech_slope.png',dpi=450,facecolor='white'); plt.close(f)
# ---------------- LS에코에너지: 성장 속도와 증분 이익률
def lseco(wpt=386,hpt=150):
    f=fig(wpt,hpt); H=hpt; Wd=wpt
    f.text(0.0,1-2/H,'① 성장 속도 비교',fontsize=7.4,fontweight='bold',color=NAVY,va='top')
    f.text(0.0,1-12.5/H,'(%, 괄호는 비교 기간)',fontsize=5.4,color=LG,va='top')
    ax=f.add_axes([88/Wd,26/H,(215-88)/Wd,1-54/H]); clean(ax); ax.grid(axis='x',color=GRID,lw=0.45); ax.grid(axis='y',visible=False)
    ax.spines['left'].set_visible(True); ax.spines['bottom'].set_visible(False)
    rows=[('주가','7/30 저점 → 9/30',62400/32000*100-100,RED),('매출','2026 상반기, 전년 대비',32.8,SLATE),('영업이익','2026 상반기, 전년 대비',16.5,MID),('영업이익','2026 2분기, 전년 대비',7.0,NAVY)]
    y=np.arange(len(rows))[::-1]
    for yy,(a,b,v,colr) in zip(y,rows):
        ax.barh(yy,v,height=0.58,color=colr,zorder=3)
        ax.text(v+2,yy,f'+{v:.1f}' if v<90 else f'+{v:.0f}',fontsize=6.0,fontweight='bold',color=colr,va='center')
        f.text(0.0,(26+(yy+0.5)/len(rows)*(H-54))/H+0.0,a,fontsize=6.2,fontweight='bold',color='#1a1a1a',va='bottom')
        f.text(0.0,(26+(yy+0.5)/len(rows)*(H-54)-1)/H,b,fontsize=5.0,color=GRAY,va='top')
    ax.set_xlim(0,115); ax.set_ylim(-0.6,len(rows)-0.4); ax.set_yticks([]); ax.set_xticks([0,50,100]); ax.tick_params(axis='x',labelsize=5.0)
    # right panel: incremental margin
    x0=240/Wd
    f.text(x0,1-2/H,'② 증분 이익률',fontsize=7.4,fontweight='bold',color=NAVY,va='top')
    f.text(x0,1-12.5/H,'(상반기 영업이익률과 늘어난 매출의 이익률, %)',fontsize=5.4,color=LG,va='top')
    ax2=f.add_axes([x0+4/Wd,26/H,(Wd-248)/Wd,1-58/H]); clean(ax2)
    cats=['2025 상반기\n영업이익률','2026 상반기\n영업이익률','증분 이익률\n(Δ이익 ÷ Δ매출)']
    vals=[389.7/4787.7*100,454/6358*100,(454-389.7)/(6358-4787.7)*100]; cols=[LS,NAVY,RED]
    ax2.bar(range(3),vals,width=0.56,color=cols,zorder=3)
    for i,v in enumerate(vals): ax2.text(i,v+0.25,f'{v:.1f}',ha='center',va='bottom',fontsize=6.2,fontweight='bold',color=cols[i] if i else GRAY)
    ax2.set_xticks(range(3)); ax2.set_xticklabels(cats,fontsize=5.1,linespacing=1.0); ax2.set_ylim(0,10.5); ax2.set_yticks([0,5,10])
    f.text(x0,4/H,'매출 +1,570억원 중 영업이익으로 남은 것은 약 64억원',fontsize=5.6,fontweight='bold',color=RED,va='bottom')
    f.text(0.0,4/H,'가격이 이익보다 먼저 움직였다',fontsize=5.6,fontweight='bold',color=RED,va='bottom')
    f.savefig('diag2/lseco_speed.png',dpi=450,facecolor='white'); plt.close(f)
# ---------------- GE 버노바: price + fundamentals in one row (D + F)
def gev(wpt=386,hpt=124):
    f=fig(wpt,hpt); H=hpt; Wd=wpt
    specs=[(0,176,'① 주가','(달러, 일봉 종가)'),(194,92,'② 총 백로그','(억달러)'),(298,88,'③ 가스터빈','(GW, 백로그·슬롯)')]
    axes=[]
    for x,w,t,u in specs:
        f.text(x/Wd,1-1/H,t,fontsize=6.9,fontweight='bold',color=NAVY,va='top')
        f.text(x/Wd,1-11.5/H,u,fontsize=5.1,color=LG,va='top')
        ax=f.add_axes([(x+1)/Wd,14/H,(w-(24 if x==0 else 20))/Wd,(H-40)/H]); clean(ax); ax.yaxis.tick_right(); axes.append(ax)
    dates,c=load('gev'); xs=np.array([(d-dates[0]).days for d in dates]); ax=axes[0]
    ax.plot(xs,c,color=NAVY,lw=0.8); pk=int(np.argmax(c))
    ax.plot(xs[pk],c[pk],'o',ms=2.4,color=RED); ax.text(xs[pk]-3,c[pk]+15,'7/6 1,195.94',fontsize=5.2,color=RED,ha='right',va='bottom',fontweight='bold')
    ax.plot(xs[-1],c[-1],'o',ms=2.6,mfc='white',mec=NAVY,mew=0.7)
    ax.text(xs[-1]-6,c[-1]-110,f'9/29 {c[-1]:,.2f}\n고점 대비 {c[-1]/1195.94*100-100:.1f}%',fontsize=5.2,color=NAVY,ha='right',va='top',fontweight='bold',linespacing=1.05)
    ax.set_ylim(550,1300); ax.set_yticks([600,900,1200]); ms=[dt.date(2026,m,1) for m in (2,4,6,8)]
    ax.set_xticks([(m-dates[0]).days for m in ms]); ax.set_xticklabels([f'{m.month}월' for m in ms])
    ax=axes[1]; ax.bar([0,1],[1290,1760],width=0.58,color=[LS,NAVY],zorder=3); ax.set_ylim(0,2200); ax.set_yticks([0,1000,2000])
    for i,v in enumerate([1290,1760]): ax.text(i,v+40,f'{v:,}',ha='center',va='bottom',fontsize=5.8,fontweight='bold',color=[GRAY,NAVY][i])
    ax.set_xticks([0,1]); ax.set_xticklabels(['1년 전','2Q']); ax.text(0.5,2080,'+36%',fontsize=6.2,fontweight='bold',color=RED,ha='center',va='top')
    ax=axes[2]; ax.bar([0,1],[100,116],width=0.58,color=[LS,NAVY],zorder=3)
    ax.bar([2],[125],width=0.58,color='white',edgecolor=SLATE,hatch='//////',lw=0.5,zorder=3)
    for i,(v,t,cl) in enumerate([(100,'100',GRAY),(116,'116',NAVY),(125,'125+',MID)]): ax.text(i,v+3,t,ha='center',va='bottom',fontsize=5.8,fontweight='bold',color=cl)
    ax.set_ylim(0,150); ax.set_yticks([0,50,100,150]); ax.set_xticks([0,1,2]); ax.set_xticklabels(['1Q','2Q','연말'])
    f.savefig('diag2/gev_2x2.png',dpi=450,facecolor='white'); plt.close(f)
if __name__=='__main__':
    hdhyundai(); eotech(); lseco(); gev()
