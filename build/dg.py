NAVY='#0b1f5c'; MID='#12457d'; SLATE='#8fa3c9'; LS='#c9d3e3'; RED='#c0392b'; GRAY='#7a7a7a'; LG='#9a9a9a'; PINK='#e8b4ae'
def fmt(v,dec=0):
    return f'{v:,.{dec}f}'
def vbars(title,unit,bars,w=170,h=72,vmax=None,vmin=0,grid=(),notes='',hatch=None,barw=0.52,title_h=True):
    """bars: list of (xlabel, value, color, valtext, valcolor[, hatched])"""
    vmax=vmax or max(b[1] for b in bars)*1.18
    n=len(bars); slot=w/n; bw=slot*barw
    rng=vmax-vmin; zero=(0-vmin)/rng*h
    out=[f'<div class="dg" style="width:{w}pt">']
    if title: out.append(f'<div class="dt">{title}</div>')
    if unit: out.append(f'<div class="du">{unit}</div>')
    out.append(f'<div class="vb" style="width:{w}pt;height:{h}pt;{"border-bottom:none;" if vmin<0 else ""}">')
    for g in grid:
        out.append(f'<div class="gl" style="bottom:{(g-vmin)/rng*h:.1f}pt"></div>')
    if vmin<0: out.append(f'<div class="gl" style="bottom:{zero:.1f}pt;border-top:0.6pt solid #9a9a9a"></div>')
    for i,b in enumerate(bars):
        lab,v,col,vt,vc=b[:5]; hat=b[5] if len(b)>5 else False
        x=i*slot+(slot-bw)/2
        top=max(v,0); bot=min(v,0)
        hh=(top-bot)/rng*h; bb=(bot-vmin)/rng*h
        style=f'left:{x:.1f}pt;width:{bw:.1f}pt;height:{max(hh,0.6):.1f}pt;bottom:{bb:.1f}pt;background:{col};'
        if hat: style=f'left:{x:.1f}pt;width:{bw-1.2:.1f}pt;height:{max(hh-1.2,0.6):.1f}pt;bottom:{bb:.1f}pt;background:repeating-linear-gradient(135deg,{col} 0,{col} 1.2pt,#fff 1.2pt,#fff 3pt);border:0.6pt solid {col};'
        out.append(f'<div class="bar" style="{style}"></div>')
        if v>=0: out.append(f'<div class="val" style="left:{i*slot:.1f}pt;width:{slot:.1f}pt;bottom:{bb+hh+2:.1f}pt;color:{vc}">{vt}</div>')
        else: out.append(f'<div class="val" style="left:{i*slot:.1f}pt;width:{slot:.1f}pt;top:{h-bb+2:.1f}pt;color:{vc}">{vt}</div>')
    out.append('</div>')
    out.append(f'<div class="vbx" style="width:{w}pt">')
    for i,b in enumerate(bars):
        out.append(f'<div class="xl" style="left:{i*slot:.1f}pt;width:{slot:.1f}pt">{b[0]}</div>')
    out.append('</div>')
    if notes: out.append(f'<div style="margin-top:1pt">{notes}</div>')
    out.append('</div>')
    return ''.join(out)
def hstack(segs,w=364,h=17,fs=6.5):
    tot=sum(s[1] for s in segs); out=[f'<div class="hs" style="width:{w}pt;height:{h}pt">']
    for lab,v,col,tc in segs:
        out.append(f'<div style="width:{v/tot*w:.1f}pt;background:{col};color:{tc};line-height:{h}pt;font-size:{fs}pt">{lab}</div>')
    out.append('</div>'); return ''.join(out)
def flow(steps,arrow='→',w=364,box_h=None,accent_last=True,colors=None):
    """steps: list of (head, main, sub-lines list, foot)"""
    n=len(steps); gap=12; bw=(w-gap*(n-1))/n
    out=[f'<div class="flexrow" style="width:{w}pt;align-items:stretch">']
    for i,(hd,mn,subs,ft) in enumerate(steps):
        col=(colors[i] if colors else (RED if (accent_last and i==n-1) else (NAVY if i==0 else '#898989')))
        out.append(f'<div style="width:{bw:.1f}pt;border:0.6pt solid #d8dbe4;border-left:2.4pt solid {col};padding:5pt 4pt 5pt 5.5pt;background:#fff;{"min-height:%spt;"%box_h if box_h else ""}">'
                   f'<div style="font-size:7.3pt;font-weight:700;color:{NAVY};line-height:9.5pt">{hd}</div>'
                   f'<div style="font-size:6.7pt;font-weight:700;color:#1a1a1a;margin-top:2.5pt;line-height:8.8pt">{mn}</div>'
                   + ''.join(f'<div style="font-size:5.9pt;color:{GRAY};line-height:8pt;margin-top:1pt">{s}</div>' for s in subs)
                   + (f'<div style="font-size:5.9pt;font-weight:700;color:{RED if (accent_last and i==n-1) else NAVY};margin-top:2.5pt">{ft}</div>' if ft else '')
                   + '</div>')
        if i<n-1: out.append(f'<div style="width:{gap}pt;text-align:center;font-size:8.5pt;color:{LG};align-self:center">{arrow}</div>')
    out.append('</div>'); return ''.join(out)
def qbox(title,text):
    return (f'<div style="background:#f4f6f8;border-left:2.4pt solid {NAVY};padding:5.5pt 9pt 6pt;margin-top:8pt">'
            f'<div style="font-size:6.4pt;font-weight:700;color:{NAVY}">{title}</div>'
            f'<div style="font-size:7pt;color:#383838;line-height:10.5pt;margin-top:2pt">{text}</div></div>')
def kv(k,v,color=NAVY):
    return f'<span style="font-weight:700;color:{color}">{k}</span> {v}'
