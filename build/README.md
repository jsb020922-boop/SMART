# DART180 Monthly 10월 — VI~X장 재구성 빌드

최종본: `../DART180_Monthly_10월_전략_최종.pdf` (60p)

- 1~19p: `DART180_Monthly_10월_전략_v3.pdf` 원본 유지 (2p Contents의 VII~X 시작 페이지만 33·46·53·60으로 갱신)
- 20~60p: 이 폴더의 소스로 WeasyPrint 70.0 + Pretendard(TTF)로 생성

## 구성
- `c_vi.py` ~ `c_x.py` : 장별 본문(종목별 핵심 질문, 개요 박스, V3 본문, 밸류에이션, 가격 확인구간, 판단·확인·리스크)
- `diags.py`, `dg.py` : 종목별 맞춤 도식(HTML/CSS)
- `render.py`, `charts.py` : 일봉 차트 재도식화 (`charts/*.png`)
- `digit.py`, `digit2.py`, `extract_all.py`, `crypto.py`, `configs.py`, `cal.py` : V3 HTS·Binance 차트 이미지에서 OHLCV·이동평균선 추출
  - 추출 결과는 `data_*.json`. 고점·저점·현재가(당일 시·고·저·종)는 V3 표기 값으로 고정
- `style.css` : DART180 하우스 양식

## 재빌드
V3 원본을 `../v3.pdf`, 원본 차트 이미지를 `../img/`에 둔 뒤 `python3 main.py` → `new_sections.pdf`를 V3 1~19p와 병합.

## 9월 30일 마감 수정 (최종 마감)
- 1~19p: 원본 문단을 같은 CSS로 다시 조판해 제자리 교체(`pedit.py`, `apply_edits.py`), 표 셀·그림 라벨 교체(`apply_cells.py`), 그림 2·3·4 재도식(`v3figs.py` → `v3figs/`)
- 20~60p: 국내 종가 9월 30일 반영(`update930.py` → `d930/`, `patch930.py`), 일봉 차트 확대 재렌더(`render2.py`, `charts2.py` → `charts2/`), 반복 도식 4개 교체(`diag_new.py` → `diag2/`)
- 기준 시점: 국내 9월 30일 종가, 미국 현지 9월 29일 종가(9월 30일 장은 발간 시점 개장 전), 암호자산 Binance 9월 29일 일봉
- 재빌드: `python3 main.py` → `new_sections.pdf`, `apply_edits.py` → `apply_cells.py`로 1~19p 수정 후 병합
