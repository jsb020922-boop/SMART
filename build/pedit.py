import pymupdf, re, html
from weasyprint import HTML
COLX0,COLX1=170.1,569.8
def spans_in(page,y0,y1,x0=COLX0-1,x1=COLX1+2):
    out=[]
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            if l['bbox'][1]>=y0-0.5 and l['bbox'][3]<=y1+0.5 and l['bbox'][0]>=x0 and l['bbox'][2]<=x1:
                out.append(l)
    out.sort(key=lambda l:(round(l['bbox'][1],1),l['bbox'][0]))
    return out
def find_para(page,start_sub,end_sub=None):
    """return (y0,y1,lines) for paragraph containing start_sub .. end_sub (line-level)"""
    L=[l for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) if l['bbox'][0]>=COLX0-1]
    L.sort(key=lambda l:(round(l['bbox'][1],1),l['bbox'][0]))
    txt=lambda l:''.join(s['text'] for s in l['spans'])
    i0=next(i for i,l in enumerate(L) if start_sub in txt(l))
    extra=0
    if isinstance(end_sub,tuple): end_sub,extra=end_sub
    i1=i0 if end_sub is None else next(i for i,l in enumerate(L) if i>=i0 and end_sub in txt(l))
    i1+=extra
    sel=L[i0:i1+1]
    return sel[0]['bbox'][1],sel[-1]['bbox'][3],sel
def runs(lines):
    R=[]
    for l in lines:
        for s in l['spans']:
            f=s['font'];c=s['color'];t=s['text']
            if 'Semi-Bold' in f and c==0x8a5a00: k='ph'
            elif 'Bold' in f and c==0x0d4176: k='lb'
            elif 'Bold' in f and c==0x1a1a1a: k='em'
            elif 'Bold' in f and c==0x0b1f5c: k='q'
            elif 'Bold' in f: k='b'
            else: k='t'
            if R and R[-1][0]==k: R[-1][1]+=t
            else: R.append([k,t])
    return R
def to_html(R):
    h=[]
    for k,t in R:
        e=html.escape(t)
        if k=='t': h.append(e)
        elif k=='ph': h.append(f'<ph>{e}</ph>')
        elif k=='lb': h.append(f'<span class="lb">{e}</span>')
        elif k=='em': h.append(f'<span class="em">{e}</span>')
        elif k=='q': h.append(f'<span class="q">{e}</span>')
        else: h.append(f'<b>{e}</b>')
    return ''.join(h)
CSS='''@page{size:399.7pt 700pt;margin:0} body{margin:0;font-family:Pretendard}
.p{font-size:9.2pt;line-height:14.55pt;color:#383838;text-align:justify;margin:0;word-break:break-all}
.n{font-size:7.54pt;line-height:11pt;color:#6d6d6d;margin:0;word-break:break-all}
.n82{font-size:8.2pt;line-height:12.3pt;color:#6f6f6f;margin:0;word-break:break-all;text-align:justify}
.pl{font-size:9.2pt;line-height:14.55pt;color:#383838;text-align:left;margin:0;word-break:break-all}
.src1{font-size:7.3pt;line-height:10.2pt;color:#6d6d6d;margin:0;white-space:nowrap}
.src71{font-size:7.1pt;line-height:9.9pt;color:#6d6d6d;margin:0;white-space:nowrap}
.lb{font-weight:700;color:#0d4176}.em{font-weight:700;color:#1a1a1a;text-decoration:underline;text-decoration-thickness:0.75pt;text-underline-offset:2.2pt}
.q{font-weight:700;color:#0b1f5c} b{font-weight:700;color:#1a1a1a}'''
def render_snip(inner,cls='p',width=399.7,css_extra=''):
    doc=f'<html><head><style>{CSS.replace("399.7pt",f"{width}pt")}{css_extra}</style></head><body><p class="{cls}">{inner}</p></body></html>'
    pdf=HTML(string=doc).write_pdf(); sd=pymupdf.open('pdf',pdf); return sd
def snip_lines(sd):
    p=sd[0]; L=[l for b in p.get_text('dict')['blocks'] for l in b.get('lines',[])]
    return L
def replace_para(page,y0,y1,lines,new_inner,cls='p',x0=COLX0,width=399.7,max_extra=0.5):
    sd=render_snip(new_inner,cls,width)
    SL=snip_lines(sd); assert SL
    s_top=SL[0]['spans'][0]['origin'][1]; s_bot=max(l['bbox'][3] for l in SL)
    p_top=lines[0]['spans'][0]['origin'][1]
    dy=p_top-s_top
    new_y1=s_bot+dy
    if new_y1>y1+max_extra: raise ValueError(f'new paragraph taller: {new_y1:.1f} > {y1:.1f} (+{new_y1-y1:.1f})')
    # redact old text + underline/highlight drawings inside
    r=pymupdf.Rect(x0-0.5,y0-0.8,x0+width+1.5,y1+1.2)
    page.add_redact_annot(r,fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    clip=pymupdf.Rect(0,0,width,s_bot+3)
    page.show_pdf_page(pymupdf.Rect(x0,dy,x0+width,dy+s_bot+3),sd,0,clip=clip,overlay=True)
    return len(SL), len(lines), new_y1-y1

def find_para2(page,start_sub,end_sub=None):
    y0,y1,sel=find_para(page,start_sub,end_sub)
    L=[l for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) if l['bbox'][0]>=COLX0-1]
    band=[l for l in L if l['bbox'][1]>=y0-1 and l['bbox'][3]<=y1+1]
    band.sort(key=lambda l:(round(l['bbox'][1]),l['bbox'][0]))
    return y0,y1,band
FONTS={'Pretendard':'Pretendard-Regular','Pretendard-Bold':'Pretendard-Bold','Pretendard-Semi-Bold':'Pretendard-SemiBold','Pretendard-Medium':'Pretendard-Medium','Pretendard-Light':'Pretendard-Light'}
def span_replace(page,old,new,align='left',occurrence=None,font=None,color=None,size=None):
    hits=[]
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if s['text'].strip()==old.strip() or (old in s['text']): hits.append(s)
    assert hits, ('span not found',old)
    if occurrence is not None: hits=[hits[occurrence]]
    for s in hits:
        full=s['text']; newtext=full.replace(old,new) if old in full else new
        r=pymupdf.Rect(s['bbox']); rr=pymupdf.Rect(r.x0-0.3,r.y0+0.8,r.x1+0.3,r.y1-0.8)
        page.add_redact_annot(rr,fill=False)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        fn=FONTS.get(font or s['font'],'Pretendard-Regular'); ff=f'/root/.fonts/{fn}.ttf'
        alias='F_'+fn.replace('-','_')
        page.insert_font(fontname=alias,fontfile=ff)
        fsz=size or s['size']
        w=pymupdf.Font(fontfile=ff).text_length(newtext,fontsize=fsz)
        ox,oy=s['origin']
        if align=='center': ox=(r.x0+r.x1)/2-w/2
        elif align=='right': ox=r.x1-w
        c=color if color is not None else s['color']
        rgb=tuple(((c>>k)&255)/255 for k in (16,8,0))
        page.insert_text((ox,oy),newtext,fontname=alias,fontsize=fsz,color=rgb)
    return len(hits)
def remove_drawings_in(page,rect,pred=None):
    """cover highlight pills: paint white over rect is wrong (watermark); instead use redaction line-art removal"""
    page.add_redact_annot(rect,fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,text=pymupdf.PDF_REDACT_TEXT_NONE)
