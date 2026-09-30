import c_vi, c_vii, c_viii, c_ix, c_x
from build import page, stock
parts=[c_vi.opener()]+[stock(s) for s in c_vi.STOCKS]
parts+=[c_vii.opener()]+[stock(s) for s in c_vii.STOCKS]
parts+=[c_viii.opener()]+[stock(s) for s in c_viii.STOCKS]
parts+=[c_ix.opener()]+[stock(s) for s in c_ix.STOCKS]
parts+=[c_x.appendix()]
page(parts,'new_sections.pdf',20)
