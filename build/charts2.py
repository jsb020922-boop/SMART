from render2 import render
CH={
 'sksquare':dict(title='SK스퀘어',code='402340',bands=[(1190000,1210000,'120만원 박스 상단')],lines=[(1000000,'100만원 1차 지지','left')]),
 'hdhyundai':dict(title='HD현대',code='267250',bands=[(225000,238000,'22.5만~23.8만원 이평 밀집(추세 회복 확인)')],lines=[(190000,'19만원 1차 지지','left')]),
 'hdksoe':dict(title='HD한국조선해양',code='009540',bands=[(360000,370000,'36만~37만원 60일선·9월 반등 고점')],lines=[(314000,'314,000원 7월 저점(무효화)','left')]),
 'lselectric':dict(title='LS ELECTRIC',code='010120',bands=[(216000,223000,'21.6만~22.3만원 120일선·8월 고점')],lines=[(200000,'20만원 1차 지지','left')]),
 'hanwhaaero':dict(title='한화에어로스페이스',code='012450',bands=[(1150000,1160000,'115만원대 120일선(추세 회복 확인)')],lines=[(1000000,'100만원 1차 지지','left')]),
 'dbins':dict(title='DB손해보험',code='005830',bands=[(205000,208000,'20.5만~20.8만원 9월 고점')],lines=[(177000,'17.7만원 60일선','left')]),
 'eotech':dict(title='이오테크닉스',code='039030',bands=[(505000,511000,'50.5만~51.1만원 9월 고점')],lines=[(450000,'45만원 20일선','left')]),
 'rfmat':dict(title='RF머트리얼즈',code='327260',bands=[(50200,51200,'5.0만~5.1만원 9월 고점')],lines=[(37000,'3.7만원 60·120일선','left')]),
 'isc':dict(title='ISC',code='095340',bands=[(215000,221300,'21.5만~22.1만원 9월 고점')],lines=[(190000,'19만원 20·120일선','left')]),
 'lseco':dict(title='LS에코에너지',code='229640',bands=[(65000,67600,'6.5만~6.8만원 9월 고점')],lines=[(56800,'5.7만원 120일선(돌파 기준)','left')]),
 'samsungsdi':dict(title='삼성SDI',code='006400',bands=[(530000,546000,'53만~55만원 20·120일선')],lines=[(510000,'51만원 1차 지지','left')]),
 'skinno':dict(title='SK이노베이션',code='096770',band_side='left',bands=[(160000,164700,'16.0만~16.5만원 9월 고점대')],lines=[(122000,'12.2만원 120일선','left')]),
 'gev':dict(title='GE 버노바',code='GEV',chg='+1.34%',dec=2,h_pt=160,bands=[(1000,1011,'1,000~1,010달러 120일선')],lines=[(870,'870달러 9월 저점','left')]),
 'anet':dict(title='아리스타 네트웍스',code='ANET',dec=2,band_side='left',bands=[(211.9,214.89,'212~215달러 8·9월 고점')],lines=[(198,'198달러 20일선','left')]),
 'msft':dict(title='마이크로소프트',code='MSFT',chg='+0.15%',dec=2,band_side='left',bands=[(516,519.4,'516~519달러 9월 고점')],lines=[(486,'486달러 9월 저점','left')]),
 'eth':dict(title='이더리움',code='ETH/USDT',chg='+1.13%',dec=2,mas=('ma7','ma25','ma99'),ma_labels=('7','25','99'),bands=[(2780,2812,'2,780~2,810달러 9월 고점')],lines=[(2578.10,'MA(25) 2,578.10','left')],partial_last_vol=True),
 'stx':dict(title='스택스',code='STX/BTC',chg='+1.06%',dec=8,mas=('ma7','ma25','ma99'),ma_labels=('7','25','99'),lines=[(0.00000359,'MA(25) 0.00000359','left'),(0.00000280,'MA(99) 0.00000280','left')]),
 'zec':dict(title='지캐시',code='ZEC/ETH',chg='-5.15%',dec=5,mas=('ma7','ma25','ma99'),ma_labels=('7','25','99'),lines=[(0.52147,'MA(25) 0.52147','left'),(0.34122,'MA(99) 0.34122','left')]),
}
if __name__=='__main__':
    import sys,os; os.makedirs('charts2',exist_ok=True)
    for k in (sys.argv[1:] or CH):
        cfg=dict(CH[k]); render(k,cfg.pop('title'),cfg.pop('code'),f'charts2/{k}.png',**cfg); print(k)
