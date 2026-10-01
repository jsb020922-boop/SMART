"""QA for v30 -> v31: footers, watermark and image positions unchanged, one-line source notes, banned phrases, broken glyphs."""
import sys, pymupdf as fitz, re
a=fitz.open(sys.argv[1] if len(sys.argv) > 1 else 'base/DART180_Monthly_10월_전략_v30.pdf')
b=fitz.open(sys.argv[2] if len(sys.argv) > 2 else 'v31.pdf')
print('pages',a.page_count,b.page_count)
bad=[]
def imgs(p, wm):
    return sorted(tuple(round(v,1) for v in x['bbox']) for x in p.get_image_info()
                  if (abs(x['bbox'][2]-x['bbox'][0]-272.1)<1) == wm and x['width']>1)
nsrc=0; nonconf=[]
banned=['캡처','진행 중 값','장중 집계','확정 종가','재도식','HTS','미확보','확인하지 못','기준: 일봉','주: 8/31']
for i in range(a.page_count):
    pa,pb=a[i],b[i]
    ta=sorted(x[4].strip() for x in pa.get_text('blocks') if x[1]>805)
    tb=sorted(x[4].strip() for x in pb.get_text('blocks') if x[1]>805)
    if ta!=tb: bad.append((i+1,'footer'))
    if imgs(pa,True)!=imgs(pb,True): bad.append((i+1,'wm',imgs(pa,True),imgs(pb,True)))
    oa,ob=imgs(pa,False),imgs(pb,False)
    if len(oa)!=len(ob): bad.append((i+1,'imgcount',len(oa),len(ob)))
    elif any(abs(x[0]-y[0])>0.2 or abs(x[2]-y[2])>0.2 or abs((x[3]-x[1])-(y[3]-y[1]))>0.2 for x,y in zip(oa,ob)):
        bad.append((i+1,'imgsize'))
    txt=pb.get_text().replace('\xa0',' ')
    for ln in txt.split('\n'):
        if ln.strip().startswith('자료:'):
            nsrc+=1
            if not re.match(r'^자료: .*DART180 리서치\.$',ln.strip()): nonconf.append((i+1,ln))
    for w in banned:
        if w in txt: bad.append((i+1,'banned',w))
    if '\x00' in txt or '�' in txt: bad.append((i+1,'glyph'))
print('issues',bad); print('sources',nsrc,'nonconforming',nonconf)
