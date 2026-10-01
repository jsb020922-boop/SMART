"""QA for v32: body pages 2-63 against the v30 base (footers, watermark/image positions, one-line sources,
removed phrases, glyphs), covers on pages 1 and 64, official-evidence explanations, and every contents link."""
import re, sys, pymupdf as fitz
a = fitz.open(sys.argv[1] if len(sys.argv) > 1 else 'base/DART180_Monthly_10월_전략_v30.pdf')
b = fitz.open(sys.argv[2] if len(sys.argv) > 2 else 'v32.pdf')
bad = []


def imgs(p, wm):
    return sorted(tuple(round(v, 1) for v in x['bbox']) for x in p.get_image_info()
                  if (abs(x['bbox'][2] - x['bbox'][0] - 272.1) < 1) == wm and x['width'] > 1)


nsrc = 0
banned = ['캡처', '진행 중 값', '장중 집계', '확정 종가', '재도식', 'HTS', '미확보', '확인하지 못', '기준: 일봉', '주: 8/31', '투자 시사점']
for i in range(1, a.page_count):
    pa, pb = a[i], b[i]
    ta = sorted(x[4].strip() for x in pa.get_text('blocks') if x[1] > 805)
    tb = sorted(x[4].strip() for x in pb.get_text('blocks') if x[1] > 805)
    if ta != tb: bad.append((i + 1, 'footer'))
    if imgs(pa, True) != imgs(pb, True): bad.append((i + 1, 'wm'))
    oa, ob = imgs(pa, False), imgs(pb, False)
    if len(oa) != len(ob): bad.append((i + 1, 'imgcount', len(oa), len(ob)))
    elif any(abs(x[0] - y[0]) > 0.2 or abs(x[2] - y[2]) > 0.2 or abs((x[3] - x[1]) - (y[3] - y[1])) > 0.2 for x, y in zip(oa, ob)):
        bad.append((i + 1, 'imgsize'))
    txt = pb.get_text().replace('\xa0', ' ')
    for ln in txt.split('\n'):
        if ln.strip().startswith('자료:'):
            nsrc += 1
            if not re.match(r'^자료: .*DART180 리서치\.$', ln.strip()): bad.append((i + 1, 'source', ln))
    bad += [(i + 1, 'banned', w) for w in banned if w in txt]
    if '\x00' in txt or '�' in txt: bad.append((i + 1, 'glyph'))

# covers: one full-height image, nothing else
for i in (0, b.page_count - 1):
    p = b[i]
    info = p.get_image_info()
    if len(info) != 1 or abs(info[0]['bbox'][3] - info[0]['bbox'][1] - p.rect.height) > 0.5 or p.get_text().strip() or p.get_links():
        bad.append((i + 1, 'cover'))
if b.page_count != a.page_count + 1: bad.append(('pages', b.page_count))

# explanations on p10/p14: image above, source below, one bold phrase, darker and larger than the source
for pn, n in ((10, 2), (14, 2)):
    L = [l for bl in b[pn - 1].get_text('dict')['blocks'] for l in bl.get('lines', [])]
    ex = [s for l in L for s in l['spans'] if abs(s['size'] - 8.8) < 0.05]
    runs = sum(1 for k, s in enumerate(ex) if 'Bold' in s['font'] and (k == 0 or 'Bold' not in ex[k - 1]['font']))
    if runs != n: bad.append((pn, 'bold runs', runs))
    if any(s['color'] != 0x2b2b2b and s['color'] != 0x111111 for s in ex): bad.append((pn, 'ex colour'))

# links: printed number == target page == footer number
links = b[1].get_links()
for l in links:
    words = [w.strip() for w in b[1].get_text('text', clip=l['from']).replace('\xa0', ' ').split('\n') if w.strip()]
    num = [int(w) for w in words if w.isdigit()]
    foot = ' '.join(x[4] for x in b[l['page']].get_text('blocks') if x[1] > 805).replace('\xa0', ' ')
    if num != [l['page'] + 1] or not foot.strip().endswith(f'리서치 {l["page"] + 1}'):
        bad.append(('link', words[:2], l['page'] + 1))
rects = sorted((l['from'] for l in links), key=lambda r: r.y0)
bad += [('link overlap', r.y0) for r, s in zip(rects, rects[1:]) if r.y1 > s.y0]
print('pages', b.page_count, 'sources', nsrc, 'links', len(links))
print('issues', bad)
