"""Round 4, step A: native span/cell/image edits on the untouched V3 pages (final_in pp.1-19)."""
import pymupdf
from celledit import cell, find, put, clear, REG
import os
BASE='base/v3_p1_19.pdf' if os.path.exists('base/v3_p1_19.pdf') else '../final_in.pdf'
d=pymupdf.open(BASE)
if len(d)>19: d.delete_pages(19,len(d)-1)
# ---- p2 Contents
p=d[1]
cell(p,'2. Earnings | 높은 이익, 약해진 Revision','2. Earnings | 높은 이익, 업종별로 갈린 Revision')
# ---- p3 KPI, Fig 1
p=d[2]
cell(p,'9월 28일 종가 6,889.74','9월 30일 종가 6,838.04',align='center')
cell(p,'8월 말 대비 +0.45%p','코스닥 +2.59% · 코스피 +0.26%',align='center',maxw=100)
cell(p,'KOSPI 범위는 9월 28일','자료: DART180 리서치. KOSPI 범위는 9월 30일 종가 6,838.04 기준')
cell(p,'· 장기금리 5.3% 돌파','· 10년물 5.3% 종가 안착')
# ---- p6 Table 3 FX cell
p=d[5]
cell(p,'1,357.5~1,365.1원','9/28 1,365.1원, 9/30 1,352.8원',maxw=150)
# ---- p8 Fig 2 caption + source
p=d[7]
cell(p,'그림 2. 미국 국채 만기별 금리','그림 2. 미국 국채 만기별 금리 (8월 28일 · 9월 29일)')
s=find(p,'9월 25일은 현지 시각')
cell(p,'9월 25일은 현지 시각',s['text'].replace('9월 25일은','9월 29일은'))
# ---- p9 Table 6 + sources
p=d[8]
for o,n in [('5.17% (9/25)','5.25% (9/29)'),('5.49% (9/25)','5.57% (9/29)'),('4.81% (9/25)','4.89% (9/29)'),('1,365.1원 (9/28)','1,352.8원 (9/30)'),('104~105달러 (9/25)','105.28달러 (9/29)')]:
    cell(p,o,n,maxw=90)
cell(p,'9월 30일 종가로 교체','',font=REG)
cell(p,'서울외국환중개, DART180 리서치. 9월 말 값은','자료: 미 재무부, CME, ICE, 서울외국환중개, DART180 리서치. 미 국채·브렌트는 현지 시각 9월 29일 종가, 원/달러는 9월 30일 기준',maxw=399.7)
cell(p,'발표 후 업데이트','',font=REG)
cell(p,'9월 월간 수출은 10월 1일','관세청, 2026년 9월 1~20일 수출입 현황(잠정치), 2026.9.21. 9월 월간 수출입동향은 10월 1일 발표 예정')
# ---- p10 title + section heading
p=d[9]
cell(p,'Earnings | 높은 이익, 약해진 Revision','Earnings | 높은 이익, 업종별로 갈린 Revision')
cell(p,'상향 속도와 확산은 약해졌다','상향은 일부 업종에 모였다')
# ---- p11 Fig 4 source
p=d[10]
cell(p,'신용거래융자 9월 22일','자료: 금융투자협회, DART180 리서치. 투자자예탁금은 7월 31일~9월 22일, 신용거래융자는 7월 31일~9월 15일 기준',maxw=399.7)
# ---- p13 Fig 6 labels
p=d[12]
cell(p,'9월28일6,889.74','9월 30일 6,838.04',align='center')
cell(p,'· 장기금리5.3% 돌파','· 10년물 5.3% 종가 안착')
cell(p,'+ 4분기가이던스하향','+ 코스피 추정치 하향 전환')
cell(p,'+ 추정치하향전환','+ 4분기 가이던스 하향')
cell(p,'+ 메모리가격·CAPEX 둔화','+ 하이퍼스케일러 CAPEX 하향',maxw=75)
cell(p,'핵심전제훼손','둘 이상 동시 확인 시 전제 폐기',align='center',maxw=100)
# ---- p14 Fig 7 labels + source
p=d[13]
cell(p,'10년물5.17% ·','10년물 5.25% · 레벨 유지, 상향 업종 집중',align='right')
cell(p,'4분기가이던스하향→추정치하향전환→핵심전제폐기','추정치·가이던스·CAPEX 하향 중 둘 이상 → 핵심 전제 폐기',align='right',maxw=150)
cell(p,'9월 말은 10년물 5.17%(','자료: DART180 리서치. 8월 말은 10년물 4.73%(8월 28일), 9월 말은 10년물 5.25%(9월 29일, 현지 종가) 기준')
# ---- p15 source + price-position labels (전력기기, 방산)
p=d[14]
s=find(p,'일봉 기준(9월 29일)')
cell(p,'일봉 기준(9월 29일)',s['text'].replace('일봉 기준(9월 29일)','9월 30일 종가 기준'))
cell(p,'가격 반영:','가격 위치:',occ=1)
cell(p,'격 반영:','격 위치:',occ=1)
cell(p,'상향, 확산 정체','상향, 대형주 집중',maxw=80)
# ---- p18 Fig 9 group labels
p=d[17]
cell(p,'완충·관찰','완충 · 위험선호',occ=0,align='center')
cell(p,'변동성 완충과 비주식 자산','보험 완충과 고위험 대체자산',align='center')
# ---- p19 Table 10 coin rows
p=d[18]
for o,n in [('ETF 자금, 스테이킹','ETF 순유입, 저항 돌파'),('위험선호 후퇴','ETF 유출·달러 강세'),
            ('sBTC 예치 규모','BTC 안정, 상대강도'),('급등 후 변동성','BTC 급락, 보안 사고'),
            ('프라이버시 사용가치','프라이버시·접근성'),('차폐 풀, 규제','눌림·지지 확인')]:
    cell(p,o,n,maxw=66)
# ---- Fig 2/3/4 images (redrawn at full column width)
FIGDIR='v3figs/' if os.path.exists('v3figs/v3fig2.png') else ''
for pn,png,y0 in [(8,FIGDIR+'v3fig2.png',259.2),(10,FIGDIR+'v3fig3.png',173.1),(11,FIGDIR+'v3fig4.png',495.6)]:
    p=d[pn-1]
    info=[i for i in p.get_image_info(xrefs=True) if abs(i['bbox'][1]-y0)<1.5]
    assert len(info)==1,(pn,info)
    p.delete_image(info[0]['xref'])
    from PIL import Image
    w,h=Image.open(png).size
    p.insert_image(pymupdf.Rect(170.1,y0,569.8,y0+399.7*h/w),filename=png)
d.save('src_v4A.pdf',garbage=3,deflate=True)
print('saved src_v4A.pdf',len(d))
