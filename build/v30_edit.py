"""v30 edit: official-evidence commentary (p10, p14) and one-line source notes across the report.

step 1  native: every source note that stays one line is replaced in place (same baseline, size, colour)
step 2  reflow: multi-line source notes on single-column pages become one line and the content below moves up
step 3  p10: commentary under each official image; p14: page re-stacked with commentary under each Micron table
"""
import sys, pymupdf, pedit, relayout as R

BASE = sys.argv[1] if len(sys.argv) > 1 else 'base/DART180_Monthly_10월_전략_v30.pdf'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'v31.pdf'
LB = lambda t: f'<span class="lb">{t}</span>'

# ------------------------------------------------------------------ source notes: page -> [(old substring, new)]
SRC = {
    3: [('KOSPI 범위는', '자료: DART180 리서치.')],
    4: [('자료: 한국거래소, DART180 리서치', '자료: 한국거래소, DART180 리서치.')],
    5: [('자료: 한국거래소, 미 재무부', '자료: 한국거래소, 미 재무부, 연방준비제도, DART180 리서치.')],
    6: [('자료: 미 재무부, 미 노동통계국', '자료: 미 재무부, 미 노동통계국, FnGuide, 관세청, 서울외국환중개, DART180 리서치.'),
        ('자료: 한국거래소, 각 거래소', '자료: 한국거래소, 각 거래소, DART180 리서치.')],
    7: [('자료: DART180 리서치', '자료: DART180 리서치.')],
    8: [('Daily Treasury', '자료: 미 재무부, DART180 리서치.')],
    9: [('자료: 미 재무부, CME', '자료: 미 재무부, CME, ICE, 서울외국환중개, DART180 리서치.'),
        ('자료: 연방준비제도(9월 16일)', '자료: 연방준비제도, 한국은행, 일본은행, DART180 리서치.')],
    10: [('자료: Federal Reserve', '자료: Federal Reserve, DART180 리서치.'),
         ('자료: U.S. Bureau of Labor', '자료: 미국 노동통계국(BLS), DART180 리서치.')],
    11: [('자료: 한국은행 금융통화위원회', '자료: 한국은행, DART180 리서치.'),
         ('자료: 관세청, 2026년', '자료: 관세청, DART180 리서치.')],
    12: [('자료: FnGuide, DART180 리서치. 9월 21일', '자료: FnGuide, DART180 리서치.'),
         ('자료: 한국거래소, FnGuide, 관세청', '자료: 한국거래소, FnGuide, 관세청, DART180 리서치.')],
    13: [('자료: 금융투자협회', '자료: 금융투자협회, DART180 리서치.')],
    14: [('단위: 백만달러', '자료: Micron, DART180 리서치.'), ('FY2027 1분기(FQ1-27) 회사 전망', '자료: Micron, DART180 리서치.')],
    15: [('자료: 각 기관 발표 일정', '자료: 각 기관 발표 일정, 각 사, DART180 리서치.')],
    16: [('시나리오 확률은 DART180 추정', '자료: DART180 리서치.')],
    17: [('자료: DART180 정성평가', '자료: 미 재무부, DART180 리서치.')],
    18: [('자료: FnGuide, 각 사 실적발표', '자료: FnGuide, 각 사 실적발표, 한국거래소, DART180 리서치.')],
    20: [('자료: DART180 리서치', '자료: DART180 리서치.')],
    21: [('산업 분류는 태그로만 표시', '자료: DART180 리서치.'), ('자료: 각 사 실적발표·공시', '자료: 각 사 실적발표·공시, 한국거래소, DART180 리서치.')],
    22: [('자료: 각 사 실적발표, Binance', '자료: 각 사 실적발표, Binance, DefiLlama, DART180 리서치.'), ('자료: DART180 리서치', '자료: DART180 리서치.')],
    23: [('자료: 한국거래소, DART180 리서치. 현재가', '자료: 한국거래소, DART180 리서치.')],
    24: [('자료: SK스퀘어 NAV', '자료: SK스퀘어, SK하이닉스, FnGuide, DART180 리서치.')],
    26: [('자료: HD현대 2026년', '자료: HD현대, 증권사 추정치, 한국거래소, DART180 리서치.')],
    28: [('자료: HD한국조선해양 2026년', '자료: HD한국조선해양, DART180 리서치.')],
    30: [('자료: LS ELECTRIC 2026년', '자료: LS ELECTRIC, DART180 리서치.')],
    32: [('자료: 한화에어로스페이스 2026년', '자료: 한화에어로스페이스, DART180 리서치.')],
    34: [('자료: DB손해보험 2026년', '자료: DB손해보험, DART180 리서치.')],
    36: [('자료: 한국거래소, DART180 리서치. 현재가', '자료: 한국거래소, DART180 리서치.')],
    37: [('자료: S&P Global', '자료: S&P Global, 한국거래소, DART180 리서치.')],
    39: [('자료: 언론 보도', '자료: 언론 보도, DART180 리서치.')],
    41: [('자료: ISC 2026년', '자료: ISC, DART180 리서치.')],
    43: [('자료: LS에코에너지 2026년', '자료: LS에코에너지, 한국거래소, DART180 리서치.')],
    45: [('자료: 삼성SDI 2026년', '자료: 삼성SDI, DART180 리서치.')],
    47: [('자료: SK이노베이션 2026년', '자료: SK이노베이션, DART180 리서치.')],
    49: [('자료: NYSE, Nasdaq', '자료: NYSE, Nasdaq, DART180 리서치.')],
    50: [('Utility Dive, DART180', '자료: GE 버노바, Utility Dive, DART180 리서치.'), ('Utility Dive, NYSE', '자료: GE 버노바, Utility Dive, NYSE, DART180 리서치.')],
    52: [('실적발표(8월 4일), DART180 리서치. 2025년', '자료: 아리스타 네트웍스, DART180 리서치.'), ('실적발표(8월 4일), DART180 리서치', '자료: 아리스타 네트웍스, DART180 리서치.')],
    54: [('콘퍼런스콜(7월 29일)', '자료: 마이크로소프트, DART180 리서치.'), ('FY26 실적발표(7월 29일)', '자료: 마이크로소프트, DART180 리서치.')],
    56: [('자료: IMF Working Paper', '자료: IMF, DART180 리서치.'), ('자료: Binance, DART180 리서치. 9월 29일 일봉 기준(캡처', '자료: Binance, DART180 리서치.')],
    57: [('자료: DefiLlama', '자료: DefiLlama, Farside, DART180 리서치.')],
    59: [('자료: Stacks 공식 블로그', '자료: Stacks, DART180 리서치.')],
    60: [('달러 환산은 BTC', '자료: Binance, Fortune, DART180 리서치.')],
    61: [('자료: DART180 리서치', '자료: DART180 리서치.')],
    63: [('자료: 각 기관 발표 일정', '자료: 각 기관 발표 일정, 각 사, DART180 리서치.')],
}
# repeated notes on stock pages (price-zone tables and daily charts)
for pn in range(23, 63):
    SRC.setdefault(pn, [])
    SRC[pn] += [('가격 구간은 목표', '자료: DART180 리서치.'), ('자료: 한국거래소, DART180 리서치. 기준:', '자료: 한국거래소, DART180 리서치.'),
                ('자료: NYSE, DART180 리서치. 기준:', '자료: NYSE, DART180 리서치.'), ('자료: Nasdaq, DART180 리서치. 기준:', '자료: Nasdaq, DART180 리서치.'),
                ('자료: Binance, DART180 리서치. 단위:', '자료: Binance, DART180 리서치.')]
SRC_PRICE_BINANCE = {58, 62}   # coin price tables whose note starts '자료: Binance, ... 9월 29일 일봉 기준. 가격 구간은 ...'


def source_groups(page):
    """source notes: a '자료' line plus continuation lines of the same size and x"""
    L = [l for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])]
    L.sort(key=lambda l: (round(l['bbox'][1], 1), l['bbox'][0]))
    out, i = [], 0
    while i < len(L):
        l = L[i]; t = ''.join(s['text'] for s in l['spans'])
        if t.startswith('자료') and l['spans'][0]['size'] < 8:
            grp, j = [l], i + 1
            while j < len(L):
                n = L[j]; tn = ''.join(s['text'] for s in n['spans'])
                if (abs(n['spans'][0]['size'] - l['spans'][0]['size']) < 0.05 and abs(n['bbox'][0] - l['bbox'][0]) < 2
                        and 0 < n['bbox'][1] - grp[-1]['bbox'][1] < 12 and not tn.startswith('자료')):
                    grp.append(n); j += 1
                else:
                    break
            out.append((''.join(''.join(s['text'] for s in g['spans']) for g in grp).replace('\xa0', ' '), grp))
            i = j
        else:
            i += 1
    return out


def new_text(pn, full):
    if pn in SRC_PRICE_BINANCE and '가격 구간은' in full:
        return '자료: Binance, DART180 리서치.'
    for o, n in SRC.get(pn, []):
        if o in full:
            return n
    raise KeyError((pn, full))


def put(page, x, y, text, size, color, font='Pretendard-Regular'):
    ff = f'/root/.fonts/{font}.ttf'; alias = 'V31_' + font.replace('-', '_')
    page.insert_font(fontname=alias, fontfile=ff)
    page.insert_text((x, y), text, fontname=alias, fontsize=size, color=tuple(((color >> k) & 255) / 255 for k in (16, 8, 0)))
    return pymupdf.Font(fontfile=ff).text_length(text, fontsize=size)


def redact_lines(page, lines):
    for l in lines:
        r = pymupdf.Rect(l['bbox'])
        page.add_redact_annot(pymupdf.Rect(r.x0 - 0.5, r.y0 + 0.4, r.x1 + 0.5, r.y1 - 0.4), fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)


# ------------------------------------------------------------------ step 1: one-line notes in place
d = pymupdf.open(BASE)
multi = {}          # page -> [(new, grp)]
log = []
for pn in range(1, len(d) + 1):
    page = d[pn - 1]
    for full, grp in source_groups(page):
        new = new_text(pn, full)
        if full == new:
            continue
        s0 = grp[0]['spans'][0]
        if len(grp) == 1 or pn in (10, 14):
            redact_lines(page, grp)
            w = put(page, grp[0]['bbox'][0], s0['origin'][1], new, s0['size'], s0['color'])
            log.append((pn, len(grp), round(w, 1), new))
        else:
            multi.setdefault(pn, []).append((new, grp))
d.save('v30_A.pdf', garbage=3, deflate=True)

# ------------------------------------------------------------------ step 2: multi-line notes -> one line, reflow
src = pymupdf.open('v30_A.pdf'); out = pymupdf.open('v30_A.pdf')
for pn, items in sorted(multi.items()):
    page = src[pn - 1]
    ops = []
    for new, grp0 in items:
        # re-locate the group on the native-edited source page
        grp = [g for f, g in source_groups(page) if abs(g[0]['bbox'][1] - grp0[0]['bbox'][1]) < 0.5][0]
        sd = pedit.render_snip(new, 'src1', 399.7)
        ops.append(dict(y0=grp[0]['bbox'][1], y1=grp[-1]['bbox'][3], base=grp[0]['spans'][0]['origin'][1], sd=sd,
                        x0=grp[0]['bbox'][0], width=399.7, label=new[:14]))
        log.append((pn, len(grp), 'reflow', new))
    R.compose(out, src, pn - 1, ops)

# ------------------------------------------------------------------ step 3a: p10 commentary under each official image
FOMC = (LB('투자 시사점:') + ' 연준은 12대 0 만장일치로 정책금리를 0.25%p 올려 3.75~4.00%로 인상하고 물가가 여전히 높은 수준이라고 평가했다. '
        '이는 물가 안정을 위해 긴축 기조를 이어갈 수 있다는 신호로 해석된다. 추가 인상 우려와 높은 할인율은 주식시장의 밸류에이션 회복을 제약하는 요인이며, '
        'DART180의 지수 상단에 대한 신중한 관점과 연결된다. 10월 FOMC에서는 물가 평가와 추가 인상 가능성의 변화를 확인하고, 장기금리 흐름도 함께 점검한다.')
CPI = (LB('투자 시사점:') + ' 8월 CPI는 전월 대비 0.4%(전년 대비 3.4%), 식품·에너지를 뺀 근원 CPI는 전월 대비 0.3% 올라 7월 0.2%보다 높아졌다. '
       '에너지 가격 변동을 제외한 근원 물가에서도 상승 압력이 이어져, 금리 부담이 빠르게 해소될 것으로 판단하기는 이르다. '
       '주식시장에서는 물가 안정에 따른 전반적인 밸류에이션 상승보다 실제 이익과 가이던스가 확인되는 업종에 대한 선별적 접근이 유효하다. '
       '다음 확인 지표는 10월 14일 발표되는 9월 CPI의 월간 상승률과 미국 국채금리의 안정 여부다.')
INTRO10 = '9월 FOMC 성명과 8월 CPI 보도자료는 10월 지수 상단을 정하는 금리 경로의 근거다. 연준이 물가를 어떻게 평가하는지와 근원 물가의 월간 상승률이 내려오는지가 핵심이다.'


def place_snip(page, sd, x0, width, top):
    """place a rendered snippet so its first text line's top sits at `top`"""
    L = pedit.snip_lines(sd)
    t0 = L[0]['bbox'][1]; bot = max(l['bbox'][3] for l in L)
    dy = top - t0
    page.show_pdf_page(pymupdf.Rect(x0, dy, x0 + width, dy + bot + 3), sd, 0, clip=pymupdf.Rect(0, 0, width, bot + 3))
    return bot + dy


def region_lines(page, x0, x1, y0, y1):
    return [l for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
            if l['bbox'][0] >= x0 - 1 and l['bbox'][2] <= x1 + 1 and l['bbox'][1] >= y0 and l['bbox'][3] <= y1]


p = out[9]
intro = region_lines(p, 17, 570, 120, 160)
base0 = min(l['spans'][0]['origin'][1] for l in intro)
redact_lines(p, intro)
sd = pedit.render_snip(INTRO10, 'p', 547.0)
L = pedit.snip_lines(sd); dy = base0 - L[0]['spans'][0]['origin'][1]
bot = max(l['bbox'][3] for l in L)
p.show_pdf_page(pymupdf.Rect(19.8, dy, 19.8 + 547.0, dy + bot + 3), sd, 0, clip=pymupdf.Rect(0, 0, 547.0, bot + 3))
assert dy + bot < 168, 'p10 intro too tall'
srcs = {round(g[0]['bbox'][0]): g for f, g in source_groups(p)}
b10 = []
for x0, txt in [(17, FOMC), (302, CPI)]:
    g = srcs[x0]
    sd = pedit.render_snip(txt, 'pl', 267.9)
    b10.append(place_snip(p, sd, g[0]['bbox'][0], 267.9, g[-1]['bbox'][3] + 9.0))
assert max(b10) < R.LIMIT, ('p10 overflow', b10)
log.append((10, 'commentary bottoms', [round(b, 1) for b in b10]))

# ------------------------------------------------------------------ step 3b: p14 re-stacked
INTRO14 = '마이크론의 FY2026 4분기 실적(발표치)과 FY2027 1분기 가이던스(회사 전망)를 원문 표로 확인한다.'
MU1 = (LB('투자 시사점:') + ' 마이크론의 FY2026 4분기(FQ4-26) 매출은 542.29억달러, 조정(Non-GAAP) EPS는 33.42달러, 조정 매출총이익률은 87.0%를 기록했다(GAAP EPS 32.87달러). '
       '전분기 매출 414.56억달러와 조정 매출총이익률 84.9%를 웃돌아 매출 확대와 수익성 개선이 함께 나타났다. '
       '다만 사업부별로는 클라우드 메모리(137.69억→162.83억달러)와 코어 데이터센터(115.24억→180.02억달러) 매출이 모두 전분기보다 늘었지만 클라우드 메모리의 영업이익률은 78%에서 76%로 낮아져, 수익성 개선이 모든 사업부에서 같은 속도로 나타난 것은 아니다. '
       '이는 메모리 업황에 대한 선별적 긍정 관점을 보강한다. 해당 분기는 14주로 구성돼 분기 간 매출 비교에는 회계기간 차이를 함께 고려해야 한다.')
MU2 = (LB('투자 시사점:') + ' 마이크론은 FY2027 1분기(FQ1-27) 매출을 615억달러±15억달러, 조정 EPS를 38.15달러±1달러(GAAP 37.84달러±1달러)로 제시했다. '
       '매출 전망 중간값은 이번 분기보다 약 13.4% 높지만, 조정 매출총이익률은 87.0%에서 약 86.25%로 소폭 낮아질 것으로 예상했다. '
       '매출 성장에 대한 회사의 기대가 이어지는 가운데 수익성의 변화도 함께 살펴야 한다. '
       '국내 반도체에 대한 판단은 각 기업의 실적과 다음 분기 가이던스, 이후 이익 추정치 변화와 외국인 수급을 통해 구체화한다.')

src14 = pymupdf.open('v30_A.pdf')     # p14 had only native edits so far
sp = src14[13]
bars = sorted([dd['rect'] for dd in sp.get_drawings() if abs(dd['rect'].x0 - 17.0) < 0.5 and abs(dd['rect'].height - 20.45) < 0.6], key=lambda r: r.y0)
groups14 = sorted([g for f, g in source_groups(sp)], key=lambda g: g[0]['bbox'][1])
seg1 = (bars[0].y0 - 0.3, groups14[0][-1]['bbox'][3] + 1.0)     # caption 1 + results table + source
seg2 = (bars[1].y0 - 0.3, groups14[1][-1]['bbox'][3] + 1.0)     # caption 2 + guidance table + source
intro14 = region_lines(sp, 17, 570, 120, 160)
start = min(l['bbox'][1] for l in intro14) - 0.8

p = out[13]
p.add_redact_annot(pymupdf.Rect(0, start, R.W, R.BODY_BOT), fill=False)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                   text=pymupdf.PDF_REDACT_TEXT_REMOVE)
p = out.reload_page(p)
tiny = []
for info in p.get_image_info(xrefs=True):
    r = pymupdf.Rect(info['bbox'])
    if R._is_wm(r):
        continue
    if r.y0 >= start - 0.5:
        tiny.append(pymupdf.Rect(r.x1 - 3, r.y0 + 1, r.x1 - 1, r.y0 + 3))
for t in tiny:
    p.add_redact_annot(t, fill=False)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE, text=pymupdf.PDF_REDACT_TEXT_NONE)

y = min(l['bbox'][1] for l in intro14)
y = place_snip(p, pedit.render_snip(INTRO14, 'p', 547.0), 19.8, 547.0, y) + 18.0
for (a, b), txt in [(seg1, MU1), (seg2, MU2)]:
    sd = R._segment_doc(src14, 13, a, b)
    p.show_pdf_page(pymupdf.Rect(0, y, R.W, y + (b - a)), sd, 0, clip=pymupdf.Rect(0, a, R.W, b))
    y += (b - a) + 8.0
    y = place_snip(p, pedit.render_snip(txt, 'p', 547.0), 19.8, 547.0, y) + 16.0
log.append((14, 'bottom', round(y - 16.0, 1)))
assert y - 16.0 < R.LIMIT, ('p14 overflow', y)

out.save(OUT, garbage=4, deflate=True)
for l in log:
    print(l)
print('saved', OUT)
