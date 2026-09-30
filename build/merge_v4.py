"""Merge edited pp.1-19 (p1_19_v4.pdf) with the rebuilt stock chapters (new_sections.pdf)."""
import pymupdf
a = pymupdf.open('p1_19_v4.pdf'); b = pymupdf.open('new_sections.pdf')
out = pymupdf.open(); out.insert_pdf(a, from_page=0, to_page=18); out.insert_pdf(b)
out.set_metadata({'title': 'DART180 Monthly 10월 전략 | 10월에 공략해야 할 18개 종목', 'author': 'DART180 Research',
                  'subject': '2026년 10월 Monthly Strategy 최종본', 'creator': 'DART180 Research', 'producer': 'WeasyPrint 70.0'})
out.save('DART180_Monthly_10월_전략_최종.pdf', garbage=4, deflate=True)
print('pages', len(out))
