from build import *
import diags
def E(t): return f'<span class="em">{t}</span>'
def Q(t): return f'<span class="q">{t}</span>'
KRSRC='한국거래소, DART180 리서치. 이동평균선 5·20·60·120일, 9월 29일 장중 기준. HTS 일봉 데이터를 재도식화'
def chart(key,title,src=KRSRC):
    return figure(title,f'<img src="charts/{key}.png">',f'자료: {src}',chart=True)
def dfig(key,title,src):
    return figure(title,getattr(diags,key)(),src)
PZSRC='자료: DART180 리서치. 9월 29일 장중 기준. 가격 구간은 목표주가가 아니라 투자 논리가 가격 추세로 연결되는지 확인하는 기준'
def pos(cur,hi,lo): return f'{(cur-lo)/(hi-lo)*100:.0f}%'
def overview_table(title,rows,src):
    n=nextno('tab')
    th=('<tr><th style="width:74pt">종목</th><th>핵심 질문</th><th class="num" style="width:40pt">고점 대비</th><th class="num" style="width:40pt">저점 대비</th>'
        '<th class="num" style="width:34pt">범위 위치</th><th style="width:52pt">가격 단계</th></tr>')
    tr=''.join(f'<tr><td class="k">{a}</td><td class="q">{b}</td><td class="num">{c}</td><td class="num">{d}</td><td class="num" style="background:#f6f6f8">{e}</td><td>{f}</td></tr>' for a,b,c,d,e,f in rows)
    return f'<div class="blk"><div class="cap">표 {n}. {title}</div><table class="t ov">{th}{tr}</table><div class="src">{src}</div></div>'
