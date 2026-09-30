import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for w in ['Regular','Medium','SemiBold','Bold','Light']: fm.fontManager.addfont(f'/root/.fonts/Pretendard-{w}.ttf')
plt.rcParams.update({'font.family':'Pretendard','axes.linewidth':0.45,'axes.edgecolor':'#9a9a9a','xtick.color':'#6f6f6f','ytick.color':'#6f6f6f','xtick.labelsize':5.8,'ytick.labelsize':5.8})
NAVY='#0b1f5c'; SLATE='#8fa3c9'; LS='#c9d3e3'; RED='#c0392b'; GRAY='#6f6f6f'; GRID='#ececec'
def fig(w,h): return plt.figure(figsize=(w/72,h/72),dpi=450)
def fig2():
    W,H=399.7,130
    f=fig(W,H); ax=f.add_axes([46/W,26/H,(W-46-44)/W,(H-34)/H])
    names=['2년물','10년물','30년물']; a=[4.34,4.73,5.22]; b=[4.89,5.25,5.57]
    y=[2,1,0]
    for yy,x0,x1 in zip(y,a,b):
        ax.plot([x0,x1],[yy,yy],color=SLATE,lw=1.4,zorder=2)
        ax.plot(x0,yy,'o',ms=4.2,mfc='white',mec=SLATE,mew=0.9,zorder=3)
        ax.plot(x1,yy,'o',ms=4.6,color=NAVY,zorder=3)
        ax.text(x0,yy+0.22,f'{x0:.2f}%',ha='center',va='bottom',fontsize=6.0,color=GRAY)
        ax.text(x1,yy+0.22,f'{x1:.2f}%',ha='center',va='bottom',fontsize=6.6,color=NAVY,fontweight='bold')
        f.text(1-4/W,(26+(yy+0.5)/3*(H-34))/H,f'+{round((x1-x0)*100):.0f}bp',ha='right',va='center',fontsize=7,color=RED,fontweight='bold')
    ax.set_yticks(y); ax.set_yticklabels(names,fontsize=6.4,color='#383838'); ax.set_ylim(-0.5,2.65)
    ax.set_xlim(4.15,5.85); ax.set_xticks([4.2,4.5,4.8,5.0,5.2,5.5,5.8]); ax.set_xticklabels([f'{v:.1f}%' for v in [4.2,4.5,4.8,5.0,5.2,5.5,5.8]])
    ax.axvline(5.0,color='#bbbbbb',lw=0.6,ls=(0,(2,2)))
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(length=0,pad=3); ax.grid(axis='x',color=GRID,lw=0.5); ax.set_axisbelow(True)
    f.text(46/W,4/H,'○ 8월 28일',fontsize=6.2,color=SLATE,va='bottom'); f.text(100/W,4/H,'● 9월 29일(현지 종가)',fontsize=6.2,color=NAVY,va='bottom')
    f.savefig('v3fig2.png',dpi=450,facecolor='white'); plt.close(f)
def fig3():
    W,H=399.7,187
    f=fig(W,H); ax=f.add_axes([62/W,40/H,(262-62)/W,(H-52)/H])
    names=['232개사 합계','삼성전자','SK하이닉스']; prev=[247.9,105.9,76.9]; now=[257.8,111.4,78.1]; ch=['+4%','+5%','+2%']
    y=[2,1,0]
    for yy,p0,p1,c in zip(y,prev,now,ch):
        ax.plot([p0,p1],[yy,yy],color=SLATE,lw=1.2,zorder=2)
        ax.plot(p0,yy,'o',ms=4.2,mfc='white',mec=SLATE,mew=0.9,zorder=3); ax.plot(p1,yy,'o',ms=4.6,color=NAVY,zorder=3)
        ax.text(p1+6,yy,f'{p1:.1f}조원',va='center',fontsize=6.4,color=NAVY,fontweight='bold'); ax.text(p1+6+(58 if p1>200 else 50),yy,c,va='center',fontsize=6.4,color=RED,fontweight='bold')
    ax.set_yticks(y); ax.set_yticklabels(names,fontsize=6.4,color='#383838'); ax.set_ylim(-0.6,2.6); ax.set_xlim(0,350)
    ax.set_xticks([0,50,100,150,200,250,300,350])
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(length=0,pad=3); ax.grid(axis='x',color=GRID,lw=0.5); ax.set_axisbelow(True)
    ax.set_xlabel('3분기 영업이익 추정치 (조원)',fontsize=6.0,color=GRAY,labelpad=3)
    f.text(62/W,4/H,'○ 3개월 전',fontsize=6.2,color=SLATE,va='bottom'); f.text(112/W,4/H,'● 9월 21일',fontsize=6.2,color=NAVY,va='bottom')
    ax2=f.add_axes([292/W,40/H,(W-300)/W,(H-72)/H])
    ax2.bar([0,1],[127,105],width=0.6,color=[NAVY,SLATE])
    for i,(v,t) in enumerate([(127,'127개\n(55%)'),(105,'105개\n(45%)')]): ax2.text(i,v+3,t,ha='center',va='bottom',fontsize=6.4,fontweight='bold',color=[NAVY,SLATE][i],linespacing=1.05)
    ax2.set_ylim(0,150); ax2.set_xticks([0,1]); ax2.set_xticklabels(['상향','하향'],fontsize=6.4); ax2.set_yticks([])
    for s in ['top','right','left']: ax2.spines[s].set_visible(False)
    ax2.tick_params(length=0,pad=3)
    f.text((292+(W-300)/2)/W,1-4/H,'추정치 변경 기업 수 (3개월)',ha='center',va='top',fontsize=6.4,color=GRAY)
    f.savefig('v3fig3.png',dpi=450,facecolor='white'); plt.close(f)
def fig4():
    W,H=399.7,128
    f=fig(W,H); xl=['7/31','8/26','9/4','9/15','9/22']
    dep=[104.1,98.9,93.5,105.3,101.0]; cr=[28.9,33.1,33.6,32.8,None]
    for k,(ttl,vals,col,ylim) in enumerate([('투자자예탁금 (조원)',dep,NAVY,(85,112)),('신용거래융자 잔고 (조원)',cr,'#4a6fa5',(26,36))]):
        x0=k*(W/2+6)
        f.text((x0+2)/W,1-2/H,ttl,fontsize=6.6,color='#383838',va='top',fontweight='bold')
        ax=f.add_axes([(x0+4)/W,16/H,(W/2-18)/W,(H-34)/H])
        xs=[i for i,v in enumerate(vals) if v is not None]; ys=[v for v in vals if v is not None]
        ax.fill_between(xs,ys,ylim[0],color='#eef0f5',zorder=1); ax.plot(xs,ys,color=col,lw=1.1,zorder=3); ax.plot(xs,ys,'o',ms=3,color=col,zorder=4)
        for i,v in zip(xs,ys):
            last=(i==xs[-1] and k==0)
            ax.text(i,v+(ylim[1]-ylim[0])*0.05,f'{v:.1f}',ha='center',va='bottom',fontsize=6.2,fontweight='bold',color=RED if last else col)
#        if k==1: ax.text(4,ylim[0]+(ylim[1]-ylim[0])*0.1,'9/22 미집계',ha='center',fontsize=5.6,color=GRAY)
        ax.set_xlim(-0.4,4.4); ax.set_ylim(*ylim); ax.set_xticks(range(5)); ax.set_xticklabels(xl); ax.set_yticks([])
        for s in ['top','right','left']: ax.spines[s].set_visible(False)
        ax.tick_params(length=0,pad=3); ax.grid(axis='y',color=GRID,lw=0.5)
    f.savefig('v3fig4.png',dpi=450,facecolor='white'); plt.close(f)
fig2(); fig3(); fig4()
