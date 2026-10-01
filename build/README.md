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

## 5차 수정 (v30 → v31: 공식자료 해설·출처 주석)
사용자가 직접 고친 `base/DART180_Monthly_10월_전략_v30.pdf`(63쪽)는 원본 소스가 없어 PDF를 제자리에서 고쳤다. 원고(해설 문장, 쪽별 출처 문구)는 모두 `v30_edit.py` 안에 있다.

```
python3 v30_edit.py   # base/…_v30.pdf → 본문 PDF (중간 산출물 v30_A.pdf; 6차부터 10·14쪽 설명이 바뀌고 출력 이름은 v32_body.pdf)
python3 qa_v31.py     # 바닥글·워터마크·이미지 위치 불변, 출처 한 줄 형식, 삭제 문구, 깨진 글자 점검
```

- 1단계: 한 줄로 끝나는 출처 주석은 같은 기준선·크기·색으로 제자리 교체
- 2단계: 여러 줄이던 출처 주석은 한 줄로 바꾸고 아래 내용을 위로 당김(`relayout.compose`, 클래스 `src1`)
- 3단계: 10쪽은 두 원문 이미지 아래에 「투자 시사점」 해설(클래스 `pl`), 14쪽은 도입 → 실적 표 → 해설 → 가이던스 표 → 해설 순서로 다시 쌓음
- `relayout.py`: 워터마크를 위치가 아니라 크기로 판별하도록 바꿈(쪽마다 위치가 조금씩 다름). 4차 빌드(`stepA_v4.py`·`stepB_v4.py`) 결과는 그대로 재현됨

## 6차 수정 (v31 → v32: 공식자료 설명 압축, 표지, 목차 링크)
```
python3 v30_edit.py     # base/…_v30.pdf → v32_body.pdf (본문, 10·14쪽 설명 포함)
python3 v32_finish.py   # 앞표지 교체·뒷표지 추가 후 목차 링크 → v32.pdf
python3 qa_v32.py       # 본문 2~63쪽 불변 항목, 표지, 설명 볼드·색, 목차 링크 28개 점검
```

- 10·14쪽: 원문 이미지 → 설명(원문당 3문장, 8.8pt #2b2b2b, 핵심 구절 하나만 볼드) → 출처 한 줄(괘선 포함 원래 블록을 아래로 이동). 원고는 `v30_edit.py`의 `FOMC`·`CPI`·`MU1`·`MU2`
- 설명 줄바꿈: WeasyPrint는 한글을 음절 단위로 끊으므로 `pedit.keep_words`가 폰트 폭을 재서 띄어쓰기에서만 줄을 바꾼다(텍스트 레이어의 공백 유지)
- 표지: `covers/front.webp`(앞), `covers/back.webp`(뒤). 원본 픽셀 그대로 무손실 PNG로 넣고 종횡비 유지, 남는 0.3pt 여백은 이미지 가장자리 색. 앞표지는 1쪽을 대체하고 뒷표지는 부록(63쪽) 뒤 64쪽에 추가해 본문 쪽 번호는 그대로
- 목차 링크: 표지 적용 뒤 2쪽의 28개 항목(장 10, 하위 18)에 테두리 없는 내부 이동 링크. 항목명~쪽 번호 전체가 클릭 영역이고 인접 영역은 겹치지 않음. 장은 해당 쪽 맨 위, 하위 항목은 그 쪽의 소제목 위치로 이동
