import re, html as H
from weasyprint import HTML
CNT={'fig':10,'tab':10}
def nextno(k): return '@F@' if k=='fig' else '@T@'
def P(label,text): return f'<p class="p"><span class="lb">{label}:</span> {text}</p>' if label else f'<p class="p">{text}</p>'
def box(title,rows):
    r=''.join(f'<div class="row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in rows)
    return f'<div class="box"><div class="bt">{title}</div>{r}</div>'
def figure(title,inner,src,chart=False):
    n=nextno('fig')
    body=f'<div class="chartwrap">{inner}</div>' if chart else f'<div class="fig">{inner}</div>'
    return f'<div class="blk"><div class="cap">그림 {n}. {title}</div>{body}<div class="src">{src}</div></div>'
BADGE={'저항':'b-res','확인':'b-cfm','지지':'b-sup','무효화':'b-inv','밀집':'b-now','현재':'b-now','기준':'b-now'}
def table(title,rows,src,head=('구분','가격','해석','성격')):
    n=nextno('tab')
    th=f'<tr><th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th><th class="bd">{head[3]}</th></tr>'
    tr=''.join(f'<tr><td class="k">{a}</td><td class="pz">{b}</td><td>{c}</td><td class="bd"><span class="bdg {BADGE.get(d,"b-now")}">{d}</span></td></tr>' for a,b,c,d in rows)
    return f'<div class="blk"><div class="cap">표 {n}. {title}</div><table class="t">{th}{tr}</table><div class="src">{src}</div></div>'
def gtable(title,head,rows,src,widths=None):
    n=nextno('tab')
    th='<tr>'+''.join(f'<th{(" style=%swidth:%spt%s"%(chr(34),widths[i],chr(34))) if widths else ""}>{h}</th>' for i,h in enumerate(head))+'</tr>'
    tr=''.join('<tr>'+''.join(f'<td{" class=k" if j==0 else ""}>{c}</td>' for j,c in enumerate(r))+'</tr>' for r in rows)
    return f'<div class="blk"><div class="cap">표 {n}. {title}</div><table class="t">{th}{tr}</table><div class="src">{src}</div></div>'
def chapter(num,rh,title,intro,sec=None):
    s=f'<div class="chap"><div class="rh"><span>{rh}</span><span>2026. 9. 30.</span></div><div class="rule"></div><div class="band"><span class="num">{num}</span><span class="ttl">{title}</span></div><div class="col">'
    if sec: s+=f'<div class="sec"><span class="sn">01</span><h2>{sec}</h2></div>'
    else: s+='<div style="height:26pt"></div>'
    s+=''.join(t if t.startswith('<') else P(None,t) for t in intro)+'</div></div>'
    return s
def stock(d,first=False):
    s=f'<div class="stock{" first" if first else ""}"><div class="col">'
    s+=(f'<div class="sh"><div class="no"><b>{d["no"]:02d}</b><i>/18</i></div><span class="nm">{d["name"]}</span>'
        f'<span class="sub">{d["sub"]}</span><span class="tag">{d["tag"]}</span></div>')
    s+=P(None,d['lead'])
    s+=box(d.get('ov_title','회사 개요 · 투자 연관성'),d['ov'])
    for blk in d['a']:
        s+=blk
    for blk in d['b']:
        s+=blk
    s+=box('판단 · 확인 · 리스크',d['summary'])
    if d.get('foot'): s+=f'<p class="src" style="border-top:none;margin-top:4pt">{d["foot"]}</p>'
    s+='</div></div>'
    return s
def number(doc,fig0=11,tab0=11):
    import re
    c={'F':fig0-1,'T':tab0-1}
    def rep(m):
        c[m.group(1)]+=1; return str(c[m.group(1)])
    return re.sub(r'@([FT])@',rep,doc)
def page(parts,out,start_page,fig0=11,tab0=11):
    doc=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><style>@page:first{{counter-reset: page {start_page}}}</style></head><body>{"".join(parts)}</body></html>'
    doc=number(doc,fig0,tab0)
    open(out.replace('.pdf','.html'),'w').write(doc)
    HTML(string=doc,base_url='.').write_pdf(out)
