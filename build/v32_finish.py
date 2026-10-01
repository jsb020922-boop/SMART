"""v32 finish (after v30_edit.py): new front/back cover images, then internal links on the contents page.

front cover replaces page 1 (no second cover), back cover is added after the appendix (v31 had none);
the body keeps its page indices, so printed page N stays PDF page N.
"""
import io, re, sys, pymupdf
from PIL import Image, ImageStat

BODY = sys.argv[1] if len(sys.argv) > 1 else 'v32_body.pdf'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'v32.pdf'
FRONT, BACK = 'covers/front.webp', 'covers/back.webp'


def cover_page(doc, pno, path):
    """full-bleed image, aspect kept and centred; any sliver left by the ratio difference takes the image's edge colour"""
    w, h = doc[0].rect.width, doc[0].rect.height
    im = Image.open(path).convert('RGB')
    edges = [ImageStat.Stat(im.crop(box)).mean for box in ((0, 0, 2, im.height), (im.width - 2, 0, im.width, im.height))]
    fill = tuple(sum(e[k] for e in edges) / len(edges) / 255 for k in range(3))
    buf = io.BytesIO(); im.save(buf, 'PNG')                     # lossless, original pixel size
    page = doc.new_page(pno, width=w, height=h)
    page.draw_rect(page.rect, color=None, fill=fill, width=0)
    page.insert_image(page.rect, stream=buf.getvalue(), keep_proportion=True)
    return page


doc = pymupdf.open(BODY)
n_body = doc.page_count
cover_page(doc, 0, FRONT)
doc.delete_page(1)                                              # the old cover
cover_page(doc, -1, BACK)
assert doc.page_count == n_body + 1

# ------------------------------------------------------------------ contents links (page order is final now)
def lines(page):
    return [l for b in page.get_text('dict')['blocks'] for l in b.get('lines', []) if l['bbox'][1] < 805]


def text(l):
    return ''.join(s['text'] for s in l['spans']).replace('\xa0', ' ').strip()


def footer_no(page):
    t = ' '.join(x[4] for x in page.get_text('blocks') if x[1] > 805).replace('\xa0', ' ')
    m = re.search(r'DART180 리서치 (\d+)', t)
    return int(m.group(1)) if m else None


def destination(page, title, chapter):
    """y to land on: page top for chapter bars and stand-alone evidence pages, else the section heading"""
    if chapter or title.startswith('·'):
        bars = [l for l in lines(page) if l['spans'][0]['size'] >= 17 and l['bbox'][1] < 120]
        assert bars, ('no title bar', title)
        return 0.0
    key = re.sub(r'^\d+\.\s*', '', title)
    hits = [l for l in lines(page) if key in text(l) and l['spans'][0]['size'] >= 11]
    assert hits, ('heading not found', title)
    y = min(l['bbox'][1] for l in hits)
    return 0.0 if y < 40 else y - 16.0


toc = doc[1]
L = lines(toc)
items = sorted([l for l in L if abs(l['bbox'][0] - 85.0) < 1], key=lambda l: l['bbox'][1])
rows = []
for it in items:
    y0, y1 = it['bbox'][1], it['bbox'][3]
    same = [l for l in L if abs(l['bbox'][1] - y0) < 1.5 and l is not it]
    num = [l for l in same if l['bbox'][0] > 480 and text(l).isdigit()]
    roman = [l for l in same if abs(l['bbox'][0] - 59.5) < 1]
    assert len(num) == 1, text(it)
    rows.append(dict(title=text(it), page=int(text(num[0])), chapter=bool(roman), y0=y0, y1=y1,
                     x1=num[0]['bbox'][2]))
for i, r in enumerate(rows):
    lo = (rows[i - 1]['y1'] + r['y0']) / 2 if i else r['y0'] - 4
    hi = (r['y1'] + rows[i + 1]['y0']) / 2 if i + 1 < len(rows) else r['y1'] + 4
    r['rect'] = pymupdf.Rect(55.0 if r['chapter'] else 80.0, max(r['y0'] - 4, lo), r['x1'] + 4, min(r['y1'] + 4, hi))
    tgt = doc[r['page'] - 1]
    assert footer_no(tgt) == r['page'], (r['title'], r['page'], footer_no(tgt))
    r['to'] = destination(tgt, r['title'], r['chapter'])
for a, b in zip(rows, rows[1:]):
    assert a['rect'].y1 <= b['rect'].y0, ('overlap', a['title'], b['title'])
for r in rows:
    toc.insert_link({'kind': pymupdf.LINK_GOTO, 'from': r['rect'], 'page': r['page'] - 1,
                     'to': pymupdf.Point(0, r['to']), 'zoom': 0})
doc.save(OUT, garbage=4, deflate=True)
for r in rows:
    print(f"{r['page']:>3}  y={r['to']:6.1f}  {'*' if r['chapter'] else ' '} {r['title']}")
print(len(rows), 'links;', doc.page_count, 'pages; saved', OUT)
