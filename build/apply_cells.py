import pymupdf
from pedit import FONTS
d=pymupdf.open('v3_step1.pdf')
PILL=(1.0,0.953,0.812)
def spans(page,rect):
    out=[]
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if pymupdf.Rect(s['bbox']).intersects(rect) and s['text'].strip(): out.append(s)
    return out
def find(page,sub,occ=0):
    hits=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if sub in s['text']]
    assert hits,(page.number+1,sub); return hits[occ]
def put(page,x,y,text,font='Pretendard-Regular',size=8.1,color=0x333333,align='left',x1=None):
    ff=f'/root/.fonts/{font}.ttf'; alias='F_'+font.replace('-','_')
    page.insert_font(fontname=alias,fontfile=ff)
    w=pymupdf.Font(fontfile=ff).text_length(text,fontsize=size)
    if align=='center': x=(x+x1)/2-w/2
    elif align=='right': x=x1-w
    rgb=tuple(((color>>k)&255)/255 for k in (16,8,0))
    page.insert_text((x,y),text,fontname=alias,fontsize=size,color=rgb)
    return w
def clear(page,rect,pills=True):
    # remove text in rect, and pill backgrounds fully inside rect
    page.add_redact_annot(rect,fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED if pills else pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
def cell(page,sub,new,occ=0,align='left',font=None,size=None,color=None,cx=None,maxw=None,pad=(1.2,0.8),x=None):
    s=find(page,sub,occ); r=pymupdf.Rect(s['bbox'])
    # include pill drawing around span
    rr=pymupdf.Rect(r.x0-2.5,r.y0-0.2,r.x1+2.5,r.y1+0.2)
    fn=FONTS.get(s['font'],'Pretendard-Regular') if font is None else font
    fs=size or s['size']; col=s['color'] if color is None else color
    x,y=s['origin']
    clear(page,rr,pills=True)
    if cx: w=put(page,cx[0],y,new,fn,fs,col,'center',cx[1])
    else: w=put(page,(x if x is not None else r.x0) if align=='left' else s['origin'][0],y,new,fn,fs,col,align,r.x1)
    if maxw: assert w<=maxw,(sub,new,w,maxw)
    return w
REG='Pretendard-Regular'
# ---- p3 KPI + Fig1 source
p=d[2]
cell(p,'9월 28일 종가 6,889.74','9월 30일 종가 6,838.04',align='center')
cell(p,'8월 말 대비 +0.45%p','8월 말 대비 +2.33%p (9/30)',align='center')
cell(p,'KOSPI 범위는 9월 28일','자료: DART180 리서치. KOSPI 범위는 9월 30일 종가 6,838.04 기준')
# ---- p6 Table 4
p=d[5]
for i in range(3): cell(p,'9월 30일 종가 재산출','–',0,font=REG,size=8.1,color=0x333333,x=439.0)
cell(p,'+1.11% ','+1.11% (9/23·9/28 종가 혼합)',maxw=569.8-441)
cell(p,'재산출','',font=REG)
cell(p,'1,357.5~1,365.1원','9/28 1,365.1원, 9/30 1,352.8원',maxw=150)
cell(p,'+3.83% (9/23)','+0.26% (9/30)',maxw=130)
# ---- p9 Table 6 + sources
p=d[8]
for o,n in [('5.17% (9/25)','5.25% (9/29)'),('5.49% (9/25)','5.57% (9/29)'),('4.81% (9/25)','4.89% (9/29)'),('1,365.1원 (9/28)','1,352.8원 (9/30)'),('104~105달러 (9/25)','105.28달러 (9/29)')]:
    cell(p,o,n,maxw=90)
cell(p,'9월 30일 종가로 교체','',font=REG)
cell(p,'서울외국환중개, DART180 리서치. 9월 말 값은','자료: 미 재무부, CME, ICE, 서울외국환중개, DART180 리서치. 미 국채·브렌트는 현지 시각 9월 29일 종가, 원/달러는 9월 30일 기준',maxw=399.7)
cell(p,'발표 후 업데이트','',font=REG)
cell(p,'9월 월간 수출은 10월 1일','관세청, 2026년 9월 1~20일 수출입 현황(잠정치), 2026.9.21. 9월 월간 수출입동향은 10월 1일 발표 예정')
# ---- p10 Table 7
p=d[9]
cell(p,'Revision 자료 반영','989.7조원, 7월 말 대비 +1.5%',0,font=REG,size=8.1,color=0x333333,maxw=489.8-369.3-3,x=367.0)
cell(p,'Revision 자료 반영','–',0,font=REG,size=8.1,color=0x333333,x=367.0)
src=find(p,'자료: 한국거래소, FnGuide, 관세청')
cell(p,'자료: 한국거래소, FnGuide, 관세청','자료: 한국거래소, FnGuide, 관세청, DART180 리서치. 2026년 이익 전망은 8월 27일 기준, 반도체 제외 전망은 9월 집계치 미확보',maxw=399.7)
# ---- p8 Fig 2 caption + source
p=d[7]
cell(p,'그림 2. 미국 국채 만기별 금리','그림 2. 미국 국채 만기별 금리 (8월 28일 · 9월 29일)')
s=find(p,'9월 25일은 현지 시각'); print('p8 src',s['text'])
cell(p,'9월 25일은 현지 시각',s['text'].replace('9월 25일은','9월 29일은'))
# ---- p13 Fig 6 label
p=d[12]
cell(p,'9월28일6,889.74','9월 30일 6,838.04',align='center')
# ---- p14 Fig 7 label + source
p=d[13]
cell(p,'10년물5.17% ·','10년물 5.25% · 레벨 유지, 확산 정체',align='right')
cell(p,'9월 말은 10년물 5.17%(','자료: DART180 리서치. 8월 말은 10년물 4.73%(8월 28일), 9월 말은 10년물 5.25%(9월 29일, 현지 종가) 기준')
# ---- p15 source
p=d[14]
s=find(p,'일봉 기준(9월 29일)')
cell(p,'일봉 기준(9월 29일)',s['text'].replace('일봉 기준(9월 29일)','9월 30일 종가 기준'))
d.save('v3_step2.pdf')
print('saved')
