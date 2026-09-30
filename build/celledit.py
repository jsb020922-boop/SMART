import pymupdf
from pedit import FONTS
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
