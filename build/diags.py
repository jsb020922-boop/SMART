from dg import *
W=386
def row(*cols,gap=18,align='flex-start'):
    return f'<div class="flexrow" style="width:{W}pt;gap:{gap}pt;align-items:{align}">'+''.join(cols)+'</div>'
def col(html,w): return f'<div style="width:{w}pt">{html}</div>'
def title(t,u=None,right=None):
    r=f'<div style="font-size:8.6pt;font-weight:700;color:{NAVY}">{right}</div>' if right else ''
    return (f'<div class="flexrow" style="justify-content:space-between;align-items:flex-end"><div class="dg"><div class="dt">{t}</div>'
            +(f'<div class="du">{u}</div>' if u else '')+f'</div>{r}</div>')
def note(t,c='dn',mt=4): return f'<div class="dg" style="margin-top:{mt}pt"><div class="{c}">{t}</div></div>'
def tagb(t,bg=NAVY): return f'<span style="display:inline-block;font-size:5.8pt;font-weight:700;color:#fff;background:{bg};padding:0.8pt 3.2pt">{t}</span>'
def hbar(lbl,v,vmax,w,col,txt,tc='#fff',h=15):
    bw=max(v/vmax*w,1.5)
    inside=bw>len(txt)*4.2
    lab=(f'<div style="position:absolute;left:5pt;top:0;line-height:{h}pt;font-size:6.6pt;font-weight:700;color:{tc};white-space:nowrap">{txt}</div>' if inside
         else f'<div style="position:absolute;left:{bw+4:.1f}pt;top:0;line-height:{h}pt;font-size:6.6pt;font-weight:700;color:{col};white-space:nowrap">{txt}</div>')
    return (f'<div style="display:flex;align-items:center;margin-top:3pt"><div style="width:58pt;font-size:6.2pt;color:#555;line-height:7.6pt">{lbl}</div>'
            f'<div style="position:relative;width:{w}pt;height:{h}pt"><div style="position:absolute;left:0;top:0;width:{bw:.1f}pt;height:{h}pt;background:{col}"></div>{lab}</div></div>')

# 1 ---------------- SK스퀘어 : NAV / Asset map (F)
def sksquare():
    top=(title('SK스퀘어 순자산가치(NAV) 구성','(조원, 9월 23일 회사 공시 기준)','NAV 276.9조원')
         +'<div style="margin-top:5pt">'+hstack([('SK하이닉스 지분가치 272.0조원 · 98.2%',272.0,NAVY,'#fff'),('',4.9,SLATE,'#fff')],w=W,h=20,fs=7.2)+'</div>'
         +'<div style="text-align:right;font-size:6pt;color:#7a7a7a;margin-top:2pt">기타 자산 4.9조원 · 1.8%</div>')
    nav_w=236; px_w=nav_w*1190000/2098568
    mid=(f'<div style="position:relative;height:46pt;width:{nav_w+6}pt;margin-top:5pt">'
         f'<div style="position:absolute;left:0;top:0;width:{nav_w}pt;height:17pt;background:{LS}"></div>'
         f'<div style="position:absolute;left:5pt;top:0;line-height:17pt;font-size:7pt;font-weight:700;color:{NAVY}">주당 NAV 2,098,568원</div>'
         f'<div style="position:absolute;left:0;top:25pt;width:{px_w:.1f}pt;height:17pt;background:{NAVY}"></div>'
         f'<div style="position:absolute;left:5pt;top:25pt;line-height:17pt;font-size:7pt;font-weight:700;color:#fff">주가 1,190,000원</div>'
         f'<div style="position:absolute;left:{px_w:.1f}pt;top:33pt;width:{nav_w-px_w:.1f}pt;border-top:0.8pt dashed {RED}"></div>'
         f'<div style="position:absolute;left:{nav_w-0.8:.1f}pt;top:17pt;height:16pt;border-left:0.8pt dashed {RED}"></div>'
         f'<div style="position:absolute;left:{px_w+(nav_w-px_w)/2-27:.1f}pt;top:27pt;width:54pt;text-align:center;background:#fff;font-size:7.6pt;font-weight:700;color:{RED}">할인 43.3%</div></div>')
    right=(f'<div class="dg"><div class="dt" style="font-size:7pt">주당 NAV를 움직이는 두 변수</div></div>'
           f'<div style="margin-top:4pt;font-size:6.2pt;line-height:8.6pt">{tagb("이익")} <b style="color:#1a1a1a">SK하이닉스 2Q 영업이익 60.5조원</b><br><span style="color:#7a7a7a">전년 대비 +557.2%, 3Q 추정 78.1조원(3개월 전 대비 +2%)</span></div>'
           f'<div style="margin-top:4pt;font-size:6.2pt;line-height:8.6pt">{tagb("소각")} <b style="color:#1a1a1a">SK하이닉스 40조원 자사주 취득·소각</b><br><span style="color:#7a7a7a">11월 19일 종료 시 보유 주식 수가 같아도 지분율 상승</span></div>'
           f'<div style="margin-top:4pt;font-size:6.3pt;font-weight:700;color:{RED};line-height:8.8pt">→ 두 변수 모두 주당 NAV를 올린다. 주가에 남은 변수는 할인율</div>')
    midblk=('<div style="margin-top:9pt">'+title('주당 NAV와 주가','(원, 9월 23일)')+'</div>'
            +row(col(mid,nav_w+8),col(right,W-nav_w-8-16),gap=16))
    return top+midblk

# 2 ---------------- HD현대 : comparison + price-vs-estimate divergence (E + B)
def hdhyundai():
    left=vbars('2분기 연결 영업이익 기여','(억원, 2026년 2분기)',[
        ('HD현대오일뱅크<br>(정유)',18241,MID,'18,241 · 44%',MID),('HD한국조선해양<br>(조선)',16451,NAVY,'16,451 · 40%',NAVY),('기타 자회사·<br>연결조정(차감)',6554,SLATE,'6,554 · 16%',GRAY)],
        w=172,h=90,vmax=21000,grid=(10000,20000),barw=0.62,
        notes=note('연결 영업이익 4조 1,246억원(전년 대비 +262.2%, 전 분기 대비 +45.5%). 기타는 연결 합계에서 두 자회사를 뺀 값',mt=2))
    right='<img src="diag2/hdhyundai_line.png" style="width:196pt;display:block">'
    return row(left,col(right,196),gap=18)

# 3 ---------------- HD한국조선해양 : business flow with lag (A)
def hdksoe():
    tl=(f'<div class="flexrow" style="width:{W}pt;font-size:6pt;color:#7a7a7a;margin-bottom:4pt">'
        f'<div style="width:148pt;border-bottom:0.6pt solid #9a9a9a;padding-bottom:2pt">2~3년 전 · 고선가 수주와 건조 착수</div><div style="width:10pt"></div>'
        f'<div style="flex:1;border-bottom:0.6pt solid {RED};padding-bottom:2pt;color:{RED};font-weight:700">2026년 · 매출 인식과 마진 전환 ▶</div></div>')
    fl=flow([('① 고선가 수주','상반기 163.8억달러',['연간 목표의 96%','VLGC 38척 · LNG선 17척'],'고부가 선종'),
             ('② 건조','수주잔고 500척+',['약 3년 6개월치 일감'],'가시성'),
             ('③ 매출 인식','2Q 8조 9,270억원',['전년 대비 +20%'],'증가'),
             ('④ 마진','영업이익률 18.4%',['영업이익 1조 6,451억원','전년 대비 +73%'],'개선'),
             ('⑤ 이익 Revision','자회사 동반 증가',['HD현대중공업 1조 399억(+121%)','HD현대삼호 5,341억(+44%)'],'다음 관건: 선가')],w=W)
    bars=vbars('매출보다 빠른 이익','(2분기 전년 대비 증가율, %)',[('매출',20,LS,'+20%',GRAY),('영업이익',73,NAVY,'+73%',NAVY),('HD현대중공업<br>영업이익',121,MID,'+121%',MID)],w=160,h=58,vmax=150,grid=(50,100))
    om=vbars('영업이익률','(2분기, %)',[('2025.2Q<br>(역산)',12.8,LS,'12.8%',GRAY),('2026.2Q',18.4,RED,'18.4%',RED)],w=100,h=58,vmax=24,grid=())
    q=(f'<div style="width:78pt;font-size:6.3pt;line-height:9pt;color:#383838;background:#f4f6f8;border-left:2.4pt solid {NAVY};padding:5pt 6pt">'
       f'<b style="color:{NAVY}">현재 질문</b><br>수주량은 이미 충분하다. 하반기 판단 기준은 수주량에서 <b>선가와 선종 믹스</b>로 옮겨간다</div>')
    return tl+fl+'<div style="margin-top:9pt"></div>'+row(bars,om,q,gap=10)

# 4 ---------------- LS ELECTRIC : order-to-revenue / capacity-demand map (G)
def lselectric():
    def blk(h,m,subs,col=NAVY,w=86):
        return (f'<div style="width:{w}pt;border:0.6pt solid #d8dbe4;border-top:2.4pt solid {col};padding:5pt 5pt;background:#fff">'
                f'<div style="font-size:6.8pt;font-weight:700;color:{NAVY}">{h}</div><div style="font-size:7.8pt;font-weight:700;color:#1a1a1a;margin-top:2pt">{m}</div>'
                +''.join(f'<div style="font-size:5.9pt;color:#7a7a7a;line-height:8pt;margin-top:1pt">{s}</div>' for s in subs)+'</div>')
    arrow=lambda t: f'<div style="width:22pt;text-align:center;align-self:center;font-size:5.6pt;color:{GRAY};line-height:7pt">{t}<br><span style="font-size:10pt;color:{LG}">→</span></div>'
    tank=vbars('수주잔고','(조원)',[('1Q 말<br>(역산)',5.6,LS,'약 5.6',GRAY),('2Q 말',7.0,NAVY,'7.0',NAVY)],w=78,h=52,vmax=8.4)
    flowrow=(f'<div class="flexrow" style="width:{W}pt;align-items:stretch">'
             +blk('수요','북미 데이터센터 전력 병목',['변전·배전·건물 내 전력 제어까지','8월 美 DC 배전 486억원 계약'],col=NAVY)
             +arrow('유입')+blk('신규 수주 (2Q)','약 2조 1,000억원',['한 분기 매출의 1.3배','잔고 +1조 4,000억원'],col=MID,w=80)
             +arrow('적립')+f'<div style="width:78pt;border:0.6pt solid #d8dbe4;padding:4pt 3pt 0;background:#fff">{tank}</div>'
             +arrow('인식')+blk('매출 (2Q)','1조 5,770억원',['전년 대비 +32.2%','북미 약 4,000억원(분기 최대)'],col=RED,w=82)+'</div>')
    bottom=row(
        vbars('영업이익과 이익률','(억원, 2분기)',[('2025.2Q<br>(역산)',1086,LS,'1,086',GRAY),('2026.2Q',1785,NAVY,'1,785',NAVY)],w=110,h=48,vmax=2200),
        note('<b style="color:#0b1f5c">Book-to-bill 약 1.33배</b> = 신규 수주 약 2.1조원 ÷ 매출 1.58조원. 수주가 매출보다 빠르게 쌓여 잔고가 한 분기 만에 1조 4,000억원 늘었다. 영업이익 +64.4%로 매출 증가율(+32.2%)의 두 배, 영업이익률은 약 9.1%(역산)에서 11.3%로 올랐다.<br><br><b style="color:#c0392b">확인 순서</b>: 수주 → 잔고 → 매출 인식 → 이익률. 잔고가 두 분기 연속 정체하면 파이프라인의 첫 단계가 멈춘 것',c='dn',mt=14),gap=16)
    return flowrow+'<div style="margin-top:8pt"></div>'+bottom

# 5 ---------------- 한화에어로스페이스 : comparison (E)
def hanwhaaero():
    r1=(title('지상방산 수주잔고와 분기 매출','(조원, 2026년 2분기 말)')
        +hbar('수주잔고',38.3,38.3,316,NAVY,'38조 3,000억원')+hbar('2분기 매출',2.1075,38.3,316,RED,'2조 1,075억원 → 잔고는 분기 매출의 약 18배(약 4.5년치)'))
    r2=('<div style="margin-top:9pt"></div>'+title('2분기 지상방산 매출 구성','(억원)')
        +'<div style="margin-top:4pt">'+hstack([('수출 1조 2,324억원 · 58%',12324,NAVY,'#fff'),('내수 등 8,751억원 · 42% (차감)',8751,LS,NAVY)],w=W,h=17)+'</div>')
    r3=('<div style="margin-top:9pt"></div>'+title('2분기 연결 영업이익 1조 3,655억원의 출처','(억원)')
        +'<div style="margin-top:4pt">'+hstack([('한화오션 7,361 · 54%',7361,SLATE,'#fff'),('지상방산 5,330 · 39% (+2%)',5330,NAVY,'#fff'),('기타 964',964,LS,NAVY)],w=W,h=17)+'</div>')
    return r1+r2+r3+note('9월 11일 크로아티아 천무 6,410억원 수출 계약. 연결 이익의 절반 이상은 조선 자회사(한화오션)에서 나와 방산 본업의 가시성(잔고)과 연결 이익의 증가 폭을 구분해서 본다. 내수 등·기타는 합계에서 차감',mt=5)

# 6 ---------------- DB손해보험 : 3 diagnostic panels (D)
def dbins():
    w=112
    p1=vbars('① 장기보험손익','(억원, 2분기)',[('2025.2Q<br>(역산)',2570,LS,'2,570',GRAY),('2026.2Q',5105,NAVY,'5,105',NAVY)],w=w,h=62,vmax=6500,
             notes=note('+98.6%. 보험손익 5,618억원(+109.9%)의 91%',c='dnv',mt=0))
    p2=vbars('② 분기 순이익','(억원, 2026년)',[('1Q<br>(상반기-2Q)',2685,LS,'2,685',GRAY),('2Q',7111,NAVY,'7,111',NAVY)],w=w,h=62,vmax=9000,
             notes=note('상반기 9,796억원(+8.0%). 2Q에 손실계약 환입 포함',c='dr',mt=0))
    p3=vbars('③ K-ICS 비율','(%)',[('3월 말',232.1,LS,'232.1',GRAY),('6월 말',204.3,RED,'204.3',RED)],w=w,h=62,vmax=280,
             notes=note('한 분기 -27.8%p. 추가 하락 시 주주환원 여력 축소',c='dr',mt=0))
    return row(p1,p2,p3,gap=22)+note('CSM 잔액 12조 8,000억원(6월 말, 원수 기준) · 자동차보험손익 62억원(-80.6%). 이익의 지속성은 ①, 일회성은 ②, 자본 여력은 ③으로 본다',mt=6)

# 7 ---------------- 이오테크닉스 : trend + process mix (B)
def eotech():
    left='<img src="diag2/eotech_slope.png" style="width:176pt;display:block">'
    def step(stage,name,desc,status,bg):
        return (f'<div style="display:flex;border:0.6pt solid #d8dbe4;margin-top:4pt;background:#fff">'
                f'<div style="width:46pt;background:#f4f6f8;font-size:5.9pt;color:#7a7a7a;padding:4pt 4pt;line-height:7.6pt">{stage}</div>'
                f'<div style="flex:1;padding:3.5pt 5pt"><div style="font-size:6.9pt;font-weight:700;color:{NAVY}">{name}</div><div style="font-size:5.9pt;color:#555;line-height:7.8pt;margin-top:1pt">{desc}</div></div>'
                f'<div style="width:46pt;align-self:center;text-align:center">{tagb(status,bg)}</div></div>')
    right=('<div class="dg"><div class="dt">레이저가 들어가는 반도체 공정</div><div class="du">(AI 메모리: 웨이퍼를 더 얇게 갈고 더 많이 쌓는 방향)</div></div>'
           +step('웨이퍼 전공정','어닐링 장비','웨이퍼 표면을 레이저로 열처리','성장 · 확인 필요',RED)
           +step('박막 웨이퍼','레이저 커팅 장비','얇은 웨이퍼 절단. 고적층 HBM에서 적용 범위 확대 가능','성장 · 확인 필요',RED)
           +step('패키지','레이저 마커','패키지에 식별 정보를 새김. 주력 공급사','매출 기반',NAVY)
           +note('HBM 공정 채용과 매출 기여는 아직 숫자로 미확인. 성장 장비의 신규 고객 수주가 첫 확인 지표',c='dr',mt=4))
    return row(col(left,176),col(right,192),gap=18)

# 8 ---------------- RF머트리얼즈 : capacity / demand map (G)
def rfmat():
    left=vbars('매출 경로','(억원, E는 회사 인터뷰 기준 전망)',[('2024<br>(역산)',445,LS,'445',GRAY),('2025',641,NAVY,'641',NAVY),('2026E',1000,SLATE,'1,000',MID,True),('2027E',1600,SLATE,'1,600',MID,True)],
               w=168,h=84,vmax=1900,grid=(500,1000,1500),notes=note('2027E는 2026E의 1.6배, 2025년의 2.5배(회사 전망). 3분기 매출이 연 1,000억원 경로 위에 있는지가 첫 확인',c='dn',mt=0))
    def cap(label,a,b,alab,blab,col):
        return (f'<div style="margin-top:6pt"><div style="font-size:6.6pt;font-weight:700;color:{NAVY}">{label}</div>'
                f'<div style="display:flex;align-items:flex-end;gap:6pt;height:44pt;margin-top:2pt">'
                f'<div style="width:40pt;height:{a/2.6*40:.1f}pt;background:{LS};font-size:6.2pt;font-weight:700;color:{GRAY};text-align:center;line-height:9pt">1.0</div>'
                f'<div style="font-size:9pt;color:{LG};align-self:center">→</div>'
                f'<div style="width:40pt;height:{b/2.6*40:.1f}pt;background:{col};font-size:6.4pt;font-weight:700;color:#fff;text-align:center;line-height:10pt">약 2.5배</div>'
                f'<div style="font-size:5.9pt;color:#555;line-height:8pt;margin-left:4pt;align-self:center">{alab}<br><b style="color:{col}">{blab}</b></div></div></div>')
    right=('<div class="dg"><div class="dt">수요와 생산능력(CAPA)의 시차</div><div class="du">(2026년 = 1.0)</div></div>'
           +cap('고객 요청 물량(확정 수주 아님)',1,2.5,'2026년 물량 대비','2027년 요청 물량',NAVY)
           +cap('생산능력: 안산 2개 공장 → 통합 신공장',1,2.5,'신공장 약 9,900㎡','2027년 말 완공 예정',RED)
           +note('요청 물량 2.5배는 2027년(2026년 대비), CAPA 2.5배는 2027년 말 완공 기준. 매출 전망 1.6배(2027E/2026E)와 기준이 달라 같은 폭으로 비교하지 않는다',c='dr',mt=5))
    return row(left,col(right,194),gap=18)

# 9 ---------------- ISC : trend + AI mix (B)
def isc():
    left=vbars('2분기 매출과 영업이익','(억원)',[('2025.2Q<br>매출(역산)',517,LS,'517',GRAY),('2026.2Q<br>매출',729,NAVY,'729',NAVY),('2025.2Q<br>OP(역산)',137,LS,'137',GRAY),('2026.2Q<br>OP',213,RED,'213',RED)],
               w=170,h=84,vmax=880,grid=(400,800),notes=note('매출 +41%(분기 최대), 영업이익 +55%<br>영업이익률 약 26.6%(역산) → 29%',c='dnv',mt=0))
    def stack(lbl,ai,non,tot):
        h=84; ah=ai/tot*h; nh=non/tot*h
        return (f'<div style="width:62pt;text-align:center"><div style="height:{h}pt;display:flex;flex-direction:column;justify-content:flex-end;margin:0 10pt">'
                f'<div style="height:{nh:.1f}pt;background:{LS};font-size:6pt;color:{NAVY};line-height:{nh:.1f}pt;font-weight:700">비AI {non/tot*100:.0f}%</div>'
                f'<div style="height:{ah:.1f}pt;background:{NAVY};font-size:6.4pt;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center">AI {ai/tot*100:.0f}%</div></div>'
                f'<div style="border-top:0.6pt solid #9a9a9a;font-size:6pt;color:#7a7a7a;padding-top:3pt;line-height:7.6pt">{lbl}</div></div>')
    mix=('<div class="dg"><div class="dt">AI / 비AI 매출 구성</div><div class="du">(2분기, %)</div></div><div style="display:flex;margin-top:16pt">'
         +stack('2025.2Q<br>AI 346억(역산)',346,171,517)+stack('2026.2Q<br>AI 591억',591,138,729)+'</div>')
    capn=note('AI 매출 +71%. 연간 생산능력 약 21만 개 → 2029년 최대 64만 개(약 3배) 증설 계획',c='dr',mt=4)
    return row(left,col(mix+capn,150),gap=30)

# 10 ---------------- LS에코에너지 : growth speed + incremental margin (C)
def lseco():
    return ('<img src="diag2/lseco_speed.png" style="width:386pt;display:block">'
            +note('데이터센터향 버스덕트 상반기 매출 전년 대비 약 3배 · 400kV급 초고압 케이블 유럽·북미 사전적격성평가 완료. 2025년 상반기 매출·영업이익은 증가율로 역산, 증분 이익률 = (2026 상반기 영업이익 - 2025 상반기) ÷ (매출 증가분)',mt=5))

# 11 ---------------- 삼성SDI : turnaround bridge (C)
def samsungsdi():
    H=96; vmin=-1900; vmax=2500; rng=vmax-vmin; y=lambda v:(v-vmin)/rng*H
    steps=[('1Q26<br>영업손익',0,-1556,RED,'-1,556'),('분기 개선폭',-1556,2038,SLATE,'+3,594'),('2Q26<br>영업이익',0,2038,NAVY,'2,038'),('AMPC<br>(미국 세액공제)',2038,961,'#d98c84','-1,077'),('AMPC 제외<br>영업이익',0,961,RED,'961')]
    slot=236/len(steps); bw=slot*0.56; out=[f'<div class="dg"><div class="dt">영업손익 브리지: 흑자 전환은 어디서 왔나</div><div class="du">(억원)</div></div><div style="position:relative;width:236pt;height:{H}pt;margin-top:14pt">']
    out.append(f'<div style="position:absolute;left:0;right:0;bottom:{y(0):.1f}pt;border-top:0.6pt solid #9a9a9a"></div>')
    for i,(lab,a,b,c,t) in enumerate(steps):
        lo,hi=min(a,b),max(a,b); x=i*slot+(slot-bw)/2
        out.append(f'<div style="position:absolute;left:{x:.1f}pt;width:{bw:.1f}pt;bottom:{y(lo):.1f}pt;height:{(hi-lo)/rng*H:.1f}pt;background:{c}"></div>')
        ty=y(hi)+2
        out.append(f'<div style="position:absolute;left:{i*slot:.1f}pt;width:{slot:.1f}pt;bottom:{ty:.1f}pt;text-align:center;font-size:6.5pt;font-weight:700;color:{c if c!=SLATE else MID}">{t}</div>')
        if i<len(steps)-1:
            nv=b if i!=1 else 2038
            out.append(f'<div style="position:absolute;left:{x+bw:.1f}pt;width:{slot-bw:.1f}pt;bottom:{y(b if i in (0,1,3) else b):.1f}pt;border-top:0.5pt dotted #9a9a9a"></div>')
    out.append('</div><div style="position:relative;width:236pt;height:18pt">')
    for i,(lab,*_) in enumerate(steps):
        out.append(f'<div style="position:absolute;left:{i*slot:.1f}pt;width:{slot:.1f}pt;top:3pt;text-align:center;font-size:5.9pt;color:#7a7a7a;line-height:7.4pt">{lab}</div>')
    out.append('</div>')
    left=''.join(out)+note('2Q 매출 3조 7,688억원(+18.5%), 7개 분기 만의 흑자. AMPC 제외 961억원에도 관세 환급이 포함돼 이익의 질은 확인 필요',c='dr',mt=4)
    right=('<div class="dg"><div class="dt">ESS 수주 파이프라인</div><div class="du">(조원, 계약 기준)</div></div>'
           +f'<div style="display:flex;flex-direction:column;justify-content:flex-end;height:78pt;width:62pt;margin:14pt 0 0 30pt">'
           f'<div style="height:{1.5/3.6*78:.1f}pt;background:{NAVY};color:#fff;font-size:6.2pt;font-weight:700;text-align:center;line-height:7.6pt;padding-top:{1.5/3.6*78/2-7.6:.1f}pt;box-sizing:border-box">2026.3<br>1.5조</div>'
           f'<div style="height:{2.0/3.6*78:.1f}pt;background:{SLATE};color:#fff;font-size:6.2pt;font-weight:700;text-align:center;line-height:7.6pt;padding-top:{2.0/3.6*78/2-7.6:.1f}pt;box-sizing:border-box">2025 말<br>2조원+</div></div>'
           +'<div style="border-top:0.6pt solid #9a9a9a;width:122pt;margin-top:0"></div>'
           +note('2025년 말 LFP ESS 2조원 이상, 2026년 3월 미국 에너지 기업 1.5조원(2026~2029년). 생산은 스텔란티스 합작 인디애나 공장',mt=4))
    return row(col(left,236),col(right,124),gap=20)

# 12 ---------------- SK이노베이션 : segment comparison (E)
def skinno():
    left=vbars('2분기 영업이익 3조 4,873억원의 구성','(억원, 흑자 전환)',[('정유<br>재고 관련',5600,'#d98c84','약 5,600',RED),('정유<br>그 외',912,MID,'약 900',MID),('윤활유',6919,RED,'6,919',RED),('배터리<br>(일회성 포함)',8218,NAVY,'8,218',NAVY),('E&S·화학·<br>석유개발 등',13224,LS,'13,224',GRAY)],
               w=236,h=86,vmax=16000,grid=(5000,10000,15000),notes=note('정유 6,512억원 중 약 5,600억원이 재고 관련 이익, 배터리 흑자에는 보상금·IRA 세액공제 포함. E&S·화학·석유개발 등은 차감(연결조정 포함)',mt=0))
    right=vbars('윤활유: 외생 변수의 크기','(억원)',[('2026.1Q<br>(차감)',1885,LS,'1,885',GRAY),('2026.2Q',6919,RED,'6,919',RED)],w=112,h=86,vmax=8300,grid=(),
                notes=note('한 분기 +5,034억원. 중동 경쟁사 공급 차질로 그룹Ⅲ 기유 마진 상승',c='dr',mt=0))
    return row(left,right,gap=22)+note('정상 마진, 재고·래깅 효과, 보상금·세액공제를 나누면 반복을 기대할 수 있는 이익은 표면 숫자보다 작다. 유가 상승의 효과는 정제마진·가동률·조달 차질에 따라 달라진다',mt=5)

# 13 ---------------- GE 버노바 : 2x2 small multiples (E + D)
def gev():
    return ('<img src="diag2/gev_2x2.png" style="width:386pt;display:block">'
            +note('2분기 수주 유기적 +88%, 매출 유기적 +12% · 잉여현금흐름 51억달러(선수금 등 운전자본 포함) · 조정 EBITDA 마진 11.3%. 남은 변수는 마진과 이익의 현금 전환',c='dr',mt=4))

# 14 ---------------- 아리스타 네트웍스 : trend + margin structure (B)
def anet():
    left=vbars('분기 매출','(억달러)',[('2025.2Q<br>(역산)',22.0,LS,'22.0',GRAY),('2026.2Q',30.36,NAVY,'30.4',NAVY),('3Q 가이던스',33,SLATE,'약 33',MID,True)],w=150,h=62,vmax=40,grid=(10,20,30),
               notes=note('2분기 +37.7%. 처음으로 분기 30억달러를 넘었다',c='dnv',mt=0))
    H=62; steps=[('매출',0,100,NAVY,'100'),('매출원가',100,63.4,'#d98c84','-36.6'),('매출총이익',0,63.4,MID,'63.4'),('영업비용',63.4,49.9,'#d98c84','-13.5'),('영업이익',0,49.9,RED,'49.9')]
    slot=200/5; bw=slot*0.56
    out=['<div class="dg"><div class="dt">매출 100달러의 이익 구조</div><div class="du">(Non-GAAP, 2026년 2분기)</div></div>',f'<div style="position:relative;width:200pt;height:{H}pt;margin-top:16pt;border-bottom:0.6pt solid #9a9a9a">']
    for i,(lab,a,b,c,t) in enumerate(steps):
        lo,hi=min(a,b),max(a,b); x=i*slot+(slot-bw)/2
        out.append(f'<div style="position:absolute;left:{x:.1f}pt;width:{bw:.1f}pt;bottom:{lo/115*H:.1f}pt;height:{(hi-lo)/115*H:.1f}pt;background:{c}"></div>')
        out.append(f'<div style="position:absolute;left:{i*slot:.1f}pt;width:{slot:.1f}pt;bottom:{hi/115*H+2:.1f}pt;text-align:center;font-size:6.5pt;font-weight:700;color:{c if c!="#d98c84" else RED}">{t}</div>')
    out.append('</div><div style="position:relative;width:200pt;height:14pt">'+''.join(f'<div style="position:absolute;left:{i*slot:.1f}pt;width:{slot:.1f}pt;top:3pt;text-align:center;font-size:6pt;color:#7a7a7a">{s[0]}</div>' for i,s in enumerate(steps))+'</div>')
    right=''.join(out)+note('매출총이익률 63.4%, 영업이익률 49.9%. 3분기 가이던스 영업이익률 48~49%, EPS 1.06~1.08달러',c='dnv',mt=0)
    return row(left,col(right,200),gap=28)

# 15 ---------------- 마이크로소프트 : business flow loop (A)
def msft():
    fl=flow([('① AI CAPEX','4Q 약 410억달러',['금융리스 포함','전년 대비 +69%'],'투자'),
             ('② 용량','AI 인프라 확충',['데이터센터·GPU','Azure·Copilot 용량'],'확충'),
             ('③ 사용량','Azure +43%',['Azure·기타 클라우드','Copilot 3,000만 좌석+'],'확인'),
             ('④ 계약·매출','RPO 6,780억달러',['+84%','OpenAI 제외 +25%','12개월 인식 약 30%'],'축적'),
             ('⑤ 경제성','Cloud GM 65%',['전년 대비 하락','감가상각 확인'],'관건')],w=W)
    loop=(f'<div style="width:{W}pt;margin-top:3pt;position:relative;height:14pt">'
          f'<div style="position:absolute;left:36pt;right:36pt;top:0;height:8pt;border:0.8pt solid {LG};border-top:none"></div>'
          f'<div style="position:absolute;left:0;right:0;top:6pt;text-align:center;font-size:6pt;color:#7a7a7a;background:transparent"><span style="background:#fff;padding:0 4pt">장기 계약 확보 → 매출 전환 → 투자 경제성 확인은 서로 다른 단계 · 계약 증가만으로 회수가 증명되지 않는다</span></div></div>')
    cap=(f'<div style="margin-top:8pt">'+title('투자비와 매출의 비율','(억달러, FY26 연간)')
         +hbar('연간 매출',3318,3318,318,NAVY,'3,318억달러')+hbar('유형자산 투자',1159,3318,318,RED,'1,159억달러 · 매출의 35%')+'</div>')
    return fl+loop

# 16 ---------------- 이더리움 : 3 diagnostic panels + flow (D)
def eth():
    w=112
    p1=('<div class="dg"><div class="dt">① 스테이블코인 발행 잔액</div><div class="du">(억달러, 9월 29일 DefiLlama)</div></div>'
        +f'<div style="margin-top:14pt;width:{w}pt">'+hstack([('ETH 1,464 · 48%',1464,NAVY,'#fff'),('기타 체인',1599,LS,NAVY)],w=w,h=26,fs=6.4)+'</div>'
        +note('전체 3,063억달러의 약 48%가 이더리움에 발행',c='dnv',mt=4))
    p2=('<div class="dg"><div class="dt">② 스테이킹된 ETH</div><div class="du">(8월 기준)</div></div>'
        +f'<div style="margin-top:14pt;width:{w}pt">'+hstack([('4,170만 개',33.3,NAVY,'#fff'),('유통 공급 약 2/3',66.7,LS,NAVY)],w=w,h=26,fs=6.4)+'</div>'
        +note('공급량의 약 3분의 1이 스테이킹에 묶임',c='dnv',mt=4))
    p3=('<div class="dg"><div class="dt">③ 미국 현물 ETF 순유입</div><div class="du">(Farside, 9월 29일까지)</div></div>'
        +f'<div style="margin-top:9pt;width:{w}pt;border-left:2.4pt solid {NAVY};padding:3pt 0 3pt 6pt">'
        +f'<div style="font-size:5.9pt;color:{GRAY}">9월 23~29일 5거래일 합계</div><div style="font-size:10.5pt;font-weight:700;color:{NAVY};line-height:13pt">+2억 7,190만달러</div>'
        +f'<div style="font-size:5.9pt;color:{GRAY};margin-top:3pt">9월 29일 하루</div><div style="font-size:8.2pt;font-weight:700;color:{RED};line-height:10pt">-280만달러</div></div>'
        +note('하루 유출과 누적 유입을 구분. 직접 자금 경로',c='dnv',mt=4))
    fl=flow([('사용처','스테이블코인·DeFi·RWA',['송금, 대출·거래, 국채·펀드 토큰화'],''),
             ('실행','이더리움 네트워크',['스마트 계약 실행'],''),
             ('수수료','가스비는 ETH로 지불',['모든 거래의 수수료'],''),
             ('가격','ETF 수급·금리·달러',['사용 증가가 곧 가격 상승은 아님'],'')],w=W,accent_last=True)
    return row(col(p1,w),col(p2,w),col(p3,w),gap=22)+'<div style="margin-top:9pt"></div>'+fl

def cryptoflow():
    return flow([('① 매크로','금리·달러·유동성',['미국 정책·실질금리, DXY','유동성과 위험선호'],''),
                 ('② BTC와 현물 수급','BTC 방향',['현물 ETF·ETP 순유입','거래소 현물 거래량'],''),
                 ('③ 가격 확인','추세·지지·저항',['거래량 동반 돌파 여부','진입·확인·무효화 기준'],''),
                 ('④ 개별 요인','네트워크·이벤트',['사용량, 업그레이드','상품 출시, 규제'],'')],w=W,accent_last=True)

# 17 ---------------- 스택스 : layered flow (A)
def stx():
    def layer(name,desc,num,col,indent):
        return (f'<div style="display:flex;margin-top:3pt;margin-left:{indent}pt;border:0.6pt solid #d8dbe4;border-left:2.4pt solid {col};background:#fff">'
                f'<div style="width:78pt;padding:4pt 5pt;font-size:7pt;font-weight:700;color:{NAVY}">{name}</div>'
                f'<div style="flex:1;padding:4pt 5pt;font-size:6.1pt;color:#555;line-height:8.2pt">{desc}</div>'
                f'<div style="width:104pt;padding:4pt 5pt;font-size:6.2pt;font-weight:700;color:{col};text-align:right;line-height:8.2pt">{num}</div></div>')
    stack=('<div class="dg"><div class="dt">비트코인에서 STX까지의 연결 구조</div><div class="du">(아래에서 위로 가치가 올라온다)</div></div>'
           +layer('⑤ STX 사용','수수료, 스태킹(STX 예치 → BTC 보상)','가치 포착',RED,48)
           +layer('④ Bitcoin DeFi','대출·거래 애플리케이션','9/10~12/10 DeFi 보상<br>(월 1 BTC, 10/10 중간 점검)',MID,36)
           +layer('③ Stacks 스마트 계약','스택스 블록을 비트코인 블록에 기록해 보안을 빌림','9/10 Dual Stacking 종료<br>Bitcoin Staking 전환',MID,24)
           +layer('② sBTC','BTC와 1:1 연동, BTC를 금융에 활용','9/4 서명자 합류<br>(Ankr·The Tie·HashKey)',NAVY,12)
           +layer('① Bitcoin','가치저장·기관·ETF 보유. 기본 레이어는 프로그래밍 기능 최소화','BTC 방향이 선행 변수',NAVY,0))
    price=note('<b style="color:#0b1f5c">확인 기준</b>: 촉매의 효과는 달러 표시 TVL이 아니라 BTC 수량 기준 sBTC 순예치와 STX 현물 거래량, STX/BTC 상대강도로 본다. 1분기 스냅숏(sBTC 예치 5억 4,500만달러, 누적 지갑 40만 개+)은 과거 현황이다',mt=6)
    return stack+price

# 18 ---------------- 지캐시 : public vs shielded comparison (E)
def zec():
    rows=[('송금인','공개 주소가 장부에 남음','암호화'),('수취인','공개 주소가 장부에 남음','암호화'),('금액','누구나 조회 가능','암호화'),
          ('검증 방식','모든 노드가 거래 내용을 보고 검증','영지식증명: 유효성만 검증, 내용은 비공개'),
          ('공개 범위','전면 공개','조회 키로 감사인·규제기관에 선택적 공개'),('쓰임','투명한 가치 이전','급여 지급·기업 간 결제 등 정보 노출이 곤란한 거래')]
    h=(f'<table style="width:{W}pt;border-collapse:collapse;font-size:6.5pt">'
       f'<tr><th style="width:62pt"></th><th style="background:#e9ecf2;color:{NAVY};font-size:7pt;padding:4pt;text-align:left">Bitcoin식 공개 거래</th><th style="background:{NAVY};color:#fff;font-size:7pt;padding:4pt;text-align:left">Zcash 차폐(Shielded) 거래</th></tr>'
       +''.join(f'<tr><td style="padding:3.6pt 4pt;font-weight:700;color:{NAVY};border-bottom:0.5pt solid #e4e4e4">{a}</td><td style="padding:3.6pt 5pt;color:#555;border-bottom:0.5pt solid #e4e4e4">{b}</td><td style="padding:3.6pt 5pt;color:#1a1a1a;font-weight:{700 if c=="암호화" else 400};border-bottom:0.5pt solid #e4e4e4;background:#f7f8fb">{c}</td></tr>' for a,b,c in rows)
       +'</table>')
    fl=flow([('입력','송금인 · 금액 · 수취인',['차폐 주소 간 거래'],''),('증명','영지식증명(zk proof)',['내용 없이 규칙 준수만 증명'],''),
             ('네트워크','유효성은 검증',['이중 지불·위조 여부 확인'],''),('결과','정보는 비공개',['필요 시 조회 키로 선택 공개'],'')],w=W)
    return h+'<div style="margin-top:8pt"></div>'+fl
ALL=dict(sksquare=sksquare,hdhyundai=hdhyundai,hdksoe=hdksoe,lselectric=lselectric,hanwhaaero=hanwhaaero,dbins=dbins,eotech=eotech,rfmat=rfmat,isc=isc,lseco=lseco,samsungsdi=samsungsdi,skinno=skinno,gev=gev,anet=anet,msft=msft,eth=eth,stx=stx,zec=zec)
if __name__=='__main__':
    from weasyprint import HTML
    parts=[]
    for k,fn in ALL.items():
        parts.append(f'<div class="col" style="margin-top:14pt"><div class="cap">{k}</div><div class="fig">{fn()}</div></div>')
    doc='<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>'+''.join(parts)+'</body></html>'
    HTML(string=doc,base_url='.').write_pdf('diags_test.pdf')
