"""Segment-based recomposition of a V3 page.

Content above the first edit stays native. Everything from the first edit down to the
body bottom is cleared from the page and redrawn: untouched bands are copied from the
source page as clipped Form XObjects (shifted by the running offset), edited paragraphs
are re-typeset with the house CSS (pedit.CSS) and placed at the same first baseline.
"""
import pymupdf, pedit
from weasyprint import HTML

W = 595.2756
BODY_BOT = 805.0      # footer text starts at 820.4
LIMIT = 794.9         # V3 @page bottom margin 47pt (841.9 - 47)
PARA_GAP = 6.23       # baseline gap between paragraphs = 14.55 + 6.23
WM_RECT = pymupdf.Rect(157.3, 324.7, 429.4, 526.5)
COLX0 = pedit.COLX0


def render_html(inner_html, width=399.7, css_extra=''):
    doc = (f'<html><head><style>{pedit.CSS.replace("399.7pt", f"{width}pt")}{css_extra}</style></head>'
           f'<body>{inner_html}</body></html>')
    return pymupdf.open('pdf', HTML(string=doc).write_pdf())


def snip_metrics(sd):
    L = pedit.snip_lines(sd)
    assert L, 'empty snippet'
    top_base = L[0]['spans'][0]['origin'][1]
    bot = max(l['bbox'][3] for l in L)
    dr = [d['rect'].y1 for d in sd[0].get_drawings()]
    if dr:
        bot = max(bot, max(dr))
    return top_base, bot, L


def _is_wm(bbox):
    # the watermark sits at slightly different spots across the report, so it is told apart by its size
    r = pymupdf.Rect(bbox)
    return abs(r.width - WM_RECT.width) < 1 and abs(r.height - WM_RECT.height) < 1


def _wm_xref(page):
    for info in page.get_image_info(xrefs=True):
        r = pymupdf.Rect(info['bbox'])
        if abs(r.x0 - WM_RECT.x0) < 1 and abs(r.y0 - WM_RECT.y0) < 1:
            return info['xref']
    return None


def _segment_doc(src_doc, pno, a, b):
    sd = pymupdf.open()
    sd.insert_pdf(src_doc, from_page=pno, to_page=pno)
    p = sd[0]
    wm = _wm_xref(p)
    if wm:
        p.delete_image(wm)
    for r in (pymupdf.Rect(0, 0, W, a), pymupdf.Rect(0, b, W, 841.89)):
        if r.height > 0:
            p.add_redact_annot(r, fill=False)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
                       graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                       text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    # the base page keeps its watermark, so a segment must not carry a second copy
    # (reload first: get_image_info caches its result on the page object)
    p = sd.reload_page(p)
    infos = p.get_image_info()
    others = [pymupdf.Rect(i['bbox']) for i in infos if not _is_wm(i['bbox'])]
    marks = []
    for r in {tuple(i['bbox']) for i in infos if _is_wm(i['bbox'])}:
        r = pymupdf.Rect(r)
        pts = [pymupdf.Rect(x, y, x + 2, y + 2) for y in range(int(r.y0) + 2, int(r.y1) - 3, 4)
               for x in range(int(r.x0) + 2, int(r.x1) - 3, 8)]
        free = [t for t in pts if not any(t.intersects(o) for o in others)]
        assert free, f'p{pno + 1}: no free point to drop the watermark'
        marks.append(free[0])
    if marks:
        for t in marks:
            p.add_redact_annot(t, fill=False)
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
                           graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                           text=pymupdf.PDF_REDACT_TEXT_NONE)
        p = sd.reload_page(p)
    assert not any(_is_wm(i['bbox']) and i['width'] > 1 for i in p.get_image_info()), \
        f'p{pno + 1}: watermark left in segment {a:.1f}-{b:.1f}'
    return sd


def content_bottom(page, a, b):
    ys = [l['bbox'][3] for bl in page.get_text('dict')['blocks'] for l in bl.get('lines', [])
          if l['bbox'][1] >= a - 0.5 and l['bbox'][3] <= b + 0.5]
    ys += [d['rect'].y1 for d in page.get_drawings() if d['rect'].y0 >= a - 0.5 and d['rect'].y1 <= b + 0.5]
    ys += [pymupdf.Rect(i['bbox']).y1 for i in page.get_image_info()
           if pymupdf.Rect(i['bbox']).y0 >= a - 0.5 and pymupdf.Rect(i['bbox']).y1 <= b + 0.5
           and not _is_wm(i['bbox'])]
    return max(ys) if ys else a


def para(page, start_sub, end_sub, html, cls='p', x0=COLX0, width=399.7):
    """op replacing a paragraph located by substrings"""
    y0, y1, lines = pedit.find_para2(page, start_sub, end_sub)
    sd = pedit.render_snip(html, cls, width)
    return dict(y0=y0, y1=y1, base=lines[0]['spans'][0]['origin'][1], sd=sd, x0=x0, width=width,
                label=start_sub[:16])


def para_from_orig(page, start_sub, end_sub, fixes, cls='p', x0=COLX0, width=399.7):
    y0, y1, lines = pedit.find_para2(page, start_sub, end_sub)
    h = pedit.to_html(pedit.runs(lines))
    for o, n in fixes:
        assert o in h, (start_sub, o, h)
        h = h.replace(o, n)
    assert '<ph>' not in h, (start_sub, h)
    sd = pedit.render_snip(h, cls, width)
    return dict(y0=y0, y1=y1, base=lines[0]['spans'][0]['origin'][1], sd=sd, x0=x0, width=width,
                label=start_sub[:16], html=h)


def insert_after(page, start_sub, end_sub, html, cls='p', x0=COLX0, width=399.7, gap=PARA_GAP):
    """op inserting a new paragraph after the paragraph located by substrings"""
    y0, y1, lines = pedit.find_para2(page, start_sub, end_sub)
    last_base = lines[-1]['spans'][0]['origin'][1]
    lh = 14.55 if cls == 'p' else 11.0
    sd = pedit.render_snip(html, cls, width)
    return dict(y0=y1 + 1.2, y1=y1 + 1.2, base=last_base + lh + gap, sd=sd, x0=x0, width=width,
                insert=True, label='+' + start_sub[:14])


def block(y0, y1, sd, base, x0=COLX0, width=399.7, label='block'):
    return dict(y0=y0, y1=y1, base=base, sd=sd, x0=x0, width=width, label=label)


def compose(out_doc, src_doc, pno, ops, limit=LIMIT, verbose=True):
    """Rebuild out_doc[pno] from src_doc[pno] applying ops (sorted by y0)."""
    ops = sorted(ops, key=lambda o: o['y0'])
    src = src_doc[pno]
    out = out_doc[pno]
    start = ops[0]['y0'] - 0.8 if not ops[0].get('insert') else ops[0]['y0']
    # 1) clear the recomposed band on the output page (keep watermark)
    out.add_redact_annot(pymupdf.Rect(0, start, W, BODY_BOT), fill=False)
    out.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                         graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                         text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    out = out_doc.reload_page(out)
    tiny = []
    for info in out.get_image_info(xrefs=True):
        r = pymupdf.Rect(info['bbox'])
        if _is_wm(r):
            continue
        if r.y0 >= start - 0.5 and r.y1 <= BODY_BOT:
            pt = pymupdf.Rect(r.x1 - 3, r.y0 + 1, r.x1 - 1, r.y0 + 3)
            assert not any(_is_wm(i['bbox']) and pt.intersects(i['bbox']) for i in out.get_image_info()), \
                'image marker inside watermark'
            tiny.append(pt)
    for t in tiny:
        out.add_redact_annot(t, fill=False)
    if tiny:
        out.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
                             graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                             text=pymupdf.PDF_REDACT_TEXT_NONE)
    # 2) walk segments
    off = 0.0
    cur = start
    log = []

    def place(a, b, dy, x1=W):
        if b - a <= 0.3:
            return
        sd = _segment_doc(src_doc, pno, a, b)
        out.show_pdf_page(pymupdf.Rect(0, a + dy, x1, b + dy), sd, 0, clip=pymupdf.Rect(0, a, x1, b))

    for op in ops:
        if op.get('insert'):
            place(cur, op['y0'], off)
            cur = op['y0']
            base_new = op['base'] + off
        else:
            # margin labels beside the edited paragraph move with it; big section numbers can be
            # taller than the text line, so the margin band is widened to their full glyph boxes
            ma, mb = op['y0'] - 0.8, op['y1'] + 1.2
            for bl in src.get_text('dict')['blocks']:
                for l in bl.get('lines', []):
                    r = pymupdf.Rect(l['bbox'])
                    if r.x1 < op['x0'] - 1 and r.y1 > ma and r.y0 < mb:
                        ma, mb = min(ma, r.y0 - 0.5), max(mb, r.y1 + 0.5)
            place(cur, op['y0'] - 0.8, off)
            place(ma, mb, off, x1=op['x0'] - 1)
            cur = op['y1'] + 1.2
            base_new = op['base'] + off
        tb, bot, SL = snip_metrics(op['sd'])
        dy = base_new - tb
        if op.get('top_snip') is not None:
            dy = op['top_at'] + off - op['top_snip']
        clip = pymupdf.Rect(0, 0, op['width'], bot + 3)
        out.show_pdf_page(pymupdf.Rect(op['x0'], dy, op['x0'] + op['width'], dy + bot + 3), op['sd'], 0, clip=clip)
        new_bottom = bot + dy
        if op.get('insert'):
            # the gap that followed the anchor paragraph now follows the inserted one
            delta = new_bottom - (op['y0'] - 1.2 + off)
        else:
            delta = new_bottom - (op['y1'] + off)
        log.append((op['label'], round(delta, 1), len(SL)))
        off += delta
    place(cur, BODY_BOT, off)
    bottom = content_bottom(src, cur, BODY_BOT) + off
    if verbose:
        print(f'p{pno + 1}:', log, 'bottom', round(bottom, 1))
    if bottom > limit:
        raise ValueError(f'p{pno + 1} overflow: bottom {bottom:.1f} > {limit}')
    return off, bottom


V3TAB_CSS = """
@page{size:399.7pt 700pt;margin:0} body{margin:0;font-family:Pretendard}
.cap3{background:#eaeaea;border-bottom:0.75pt solid #9a9a9a;font-size:8.9pt;font-weight:700;color:#111;padding:0 6.2pt;height:19.12pt;line-height:19.12pt}
table.v3{width:399.7pt;border-collapse:collapse;margin-top:7.37pt;table-layout:fixed}
table.v3 th{background:#043a71;color:#fff;font-size:8.3pt;font-weight:700;text-align:center;line-height:11.2pt;padding:4.05pt 5.1pt}
table.v3 td{font-size:8.1pt;color:#333;line-height:11.2pt;padding:3.39pt 5.1pt;border-bottom:0.5pt solid #e4e4e4;vertical-align:middle}
table.v3 td.c{text-align:center} table.v3 td.k{color:#222}
table.v3 tr.hl td{background:#f1f4f9} table.v3 tr.hl td.k{color:#0b1f5c}
.src3{font-size:7.3pt;color:#6d6d6d;border-top:0.4pt solid #9a9a9a;margin-top:7.09pt;padding-top:3.02pt;line-height:10.2pt}
"""


def v3table(caption, widths, head, rows, src, aligns, hl=()):
    th = ''.join(f'<th style="width:{w - 10.2:.2f}pt">{h}</th>' for w, h in zip(widths, head))
    trs = ''
    for i, r in enumerate(rows):
        cls = ' class="hl"' if i in hl else ''
        tds = ''
        for j, (c, a) in enumerate(zip(r, aligns)):
            k = ('k ' if j == 0 else '') + ('c' if a == 'c' else '')
            tds += f'<td class="{k.strip()}">{c}</td>'
        trs += f'<tr{cls}>{tds}</tr>'
    html = (f'<html><head><style>{V3TAB_CSS}</style></head><body><div class="cap3">{caption}</div>'
            f'<table class="v3"><tr>{th}</tr>{trs}</table><div class="src3">{src}</div></body></html>')
    sd = pymupdf.open('pdf', HTML(string=html).write_pdf())
    top = min(d['rect'].y0 for d in sd[0].get_drawings())
    return sd, top


def table_op(page, cap_sub, sd, top):
    """replace the V3 table whose caption contains cap_sub (caption bar .. source line)"""
    cap = [l for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
           if cap_sub in ''.join(s['text'] for s in l['spans'])][0]
    cy = cap['bbox'][1]
    bar = [d['rect'] for d in page.get_drawings() if d['rect'].y0 < cy and d['rect'].y1 > cy and d['rect'].width > 390]
    y0 = min(r.y0 for r in bar)
    srcl = sorted([l for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
                   if l['bbox'][1] > cy and ''.join(s['text'] for s in l['spans']).startswith('자료')], key=lambda l: l['bbox'][1])[0]
    y1 = srcl['bbox'][3]
    return dict(y0=y0 + 0.8, y1=y1, base=0, sd=sd, x0=COLX0, width=399.7, top_snip=top, top_at=y0, label='T:' + cap_sub[:10])
