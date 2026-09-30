from common import *
def appendix():
    rows=[('9/30 밤','미국 8월 PCE (현지 9/30)','시장 전체','-','근원 PCE 방향, 연간 개정 폭'),
          ('10/1 새벽','마이크론 실적 (현지 9/30)','반도체','SK스퀘어 · 이오테크닉스 · ISC','다음 분기 가이던스, HBM 매출'),
          ('10/1','한국 9월 수출입동향','반도체 · 조선','SK스퀘어 · HD한국조선해양','반도체 수출 물량, 선박 수출'),
          ('10/2 밤','미국 9월 고용보고서','시장 전체','-','비농업 고용, 임금'),
          ('10/7~8','삼성전자 잠정실적(예상)','반도체','SK스퀘어 · 이오테크닉스','전사 매출·영업이익 (부문 이익률은 확정실적)'),
                    ('10/14 밤','미국 9월 CPI','성장주 · 디지털자산','마이크로소프트 · 디지털자산','근원 월간 0.3% 지속 여부'),
          ('10/15','미국 PPI(밤) · TSMC 실적(예상)','반도체 · AI 인프라','ISC · 아리스타 네트웍스','TSMC 4분기 가이던스, CAPEX'),
          ('10/22','한국은행 금통위','금융 · 원화','DB손해보험','금리 결정, 성장·물가 전망'),
          ('10월 하순','SK하이닉스·빅테크 실적(예상)','반도체 · AI 인프라','SK스퀘어 · 마이크로소프트 · GE 버노바','HBM 공급 계획, CAPEX 가이던스'),
          ('10월 하순','국내 3분기 실적(예상)','전력기기 · 조선 · 2차전지','LS ELECTRIC · HD한국조선해양 · 삼성SDI','수주잔고, 영업이익률, AMPC 제외 이익'),
          ('10/29 새벽','FOMC 결과 (현지 10/27~28)','시장 전체','-','추가 인상 여부와 경로'),
          ('10/29 밤','미국 3분기 GDP · 9월 PCE','시장 전체','-','성장과 물가의 동행 여부'),
          ('수시','미·이란 호르무즈 협상','에너지 · 조선','SK이노베이션 · HD현대','단계적 합의, 브렌트 100달러'),
          ('수시','방산 수출 · 조선 수주','방산 · 조선','한화에어로스페이스 · HD한국조선해양','계약 규모, 선가'),
          ('수시','미중 무역휴전 후속 협상','AI · 반도체 장비','-','수출통제·관세 세부안')]
    n='@T@'
    th=('<tr><th style="width:44pt;text-align:center">날짜</th><th style="width:80pt;text-align:center">이벤트</th><th style="width:60pt;text-align:center">영향 자산군</th>'
        '<th style="width:98pt;text-align:center">관련 종목</th><th style="text-align:center">핵심 체크포인트</th></tr>')
    tr=''.join(f'<tr><td style="text-align:center">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a,b,c,d,e in rows)
    tbl=f'<div class="blk"><div class="cap">표 {n}. 10월 이벤트 캘린더</div><table class="t cal">{th}{tr}</table><div class="src">자료: 각 기관 발표 일정, 각 사, DART180 리서치. 날짜는 한국 시간 기준(미국 지표는 밤 9시 30분, FOMC 결과는 새벽 3시). 예상은 회사 공지 전 일정</div></div>'
    s=('<div class="chap"><div class="rh"><span>Appendix</span><span>2026. 9. 30.</span></div><div class="rule"></div>'
       '<div class="band"><span class="num">X</span><span class="ttl">부록 | October Market Calendar</span></div><div class="col">'
       '<div class="sec"><span class="sn">01</span><h2>October Market Calendar</h2></div>'
       +P(None,'10월 일정은 본 보고서의 가설을 검증하는 일자다. 영향을 받는 업종과 종목, 확인 항목을 함께 정리했다.')
       +tbl
       +'<div class="sec" style="margin-top:8pt"><span class="sn">02</span><h2>Monthly Checklist</h2></div>'
       +P('매주 확인','① 미국채 10년물 5% 하회 여부 ② 원/달러 1,400원 방어 ③ 외국인 순매수의 업종 확산과 자사주 매입 종료 이후 수급 ④ 업종별 이익 추정치 변화율 ⑤ 신용융자 잔고 방향 ⑥ 상승 종목 수와 지수 방향의 일치 여부 ⑦ BTC 방향과 현물 ETF·ETP 누적 흐름. 금리·유가 경고선은 장중 터치(경고), 종가 돌파(확인), 3거래일 이상 안착(반증)으로 구분하고 매크로 악화는 밸류에이션 조정 신호로 본다. '+E('추정치 하향 전환, 4분기 가이던스 하향, 하이퍼스케일러 CAPEX 하향 중 둘 이상이 동시에 확인되면 핵심 전제를 폐기하며,')+' 앞의 두 조건은 연결될 수 있어 따로 세지 않는다.')
       +P('Top Picks 반증 조건','SK스퀘어는 SK하이닉스 4분기 추정치 하향 또는 할인율 40%대 고착, HD현대는 정유·조선 이익 동반 둔화에 따른 2026년 추정치 하향, HD한국조선해양은 신규 수주 선가의 하락 전환과 영업이익률 2분기 연속 하락, LS ELECTRIC은 수주잔고 2분기 연속 정체, 한화에어로스페이스는 지상방산 영업이익률 하락과 납품 지연, DB손해보험은 K-ICS 비율 추가 하락과 장기보험손익 후퇴다.')
       +'<p class="src" style="border-top:none;margin-top:4pt">※ 본 자료는 정보 제공을 목적으로 작성되었으며 특정 종목의 매매를 권유하지 않는다. 기재된 수치는 작성 시점 기준이며 이후 변동될 수 있다. 투자 판단의 최종 책임은 투자자 본인에게 있다.</p>'
       +'</div></div>')
    return s
