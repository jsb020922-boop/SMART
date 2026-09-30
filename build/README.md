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

## 4차 수정 (Claude Revision 1~3부 반영)
수정 가능한 원본은 이 폴더 전체다. 텍스트를 고친 뒤 아래 순서로 다시 만들면 최종 PDF가 그대로 재현된다.

```
python3 stepA_v4.py   # 1~19p: 목차·표·그림 라벨 등 제자리 교체 (base/v3_p1_19.pdf → src_v4A.pdf)
python3 stepB_v4.py   # 1~19p: 문단·표 4·표 7 재조판과 아래 내용 자동 밀기 (→ p1_19_v4.pdf)
python3 main.py       # 20~60p: HTML 조판 (→ new_sections.pdf, new_sections.html)
python3 merge_v4.py   # 병합 (→ DART180_Monthly_10월_전략_최종.pdf)
```

- 1~19p 원고: `stepB_v4.py`(문단·표 텍스트), `stepA_v4.py`(셀·라벨). 재조판 엔진은 `relayout.py`, `pedit.py`
- 20~60p 원고: `c_vi.py`(최선호), `c_vii.py`(관심), `c_viii.py`(미국), `c_ix.py`(대체자산), `c_x.py`(부록), 도식은 `diags.py`
- `new_sections.html`은 20~60p의 조판 결과 HTML(참고용, `main.py`가 다시 만든다)
- 필요 환경: Python 3, WeasyPrint 70.0, PyMuPDF, Pretendard TTF(`/root/.fonts`), matplotlib(차트 재생성 시)
