# 상품 레퍼런스 보드 — 프로젝트 현황

## 프로젝트 개요
신상품 기획 시 경쟁사 제품을 레퍼런스로 수집하는 협업 보드 툴.
상품 URL을 입력하면 이미지·상품명·가격·소재를 자동 파싱하여 카드로 표시.

---

## 파일 구성

| 파일 | 역할 |
|---|---|
| `product_reference_board.html` | 보드 UI 전체 (카드, 탭, 협업 소켓) |
| `product_board_server.py` | Flask 서버 + Playwright 파싱 + Socket.IO |
| `launch.py` | 서버 시작 + 브라우저 자동 오픈 |
| `실행.bat` | 매번 사용 시 더블클릭 실행 파일 |
| `설치.bat` | 최초 1회 패키지 설치 파일 |
| `requirements.txt` | Render.com 배포용 패키지 목록 |
| `render.yaml` | Render.com 배포 설정 |
| `사용가이드.txt` | 설치·실행·협업 방법 안내 |
| `board_state.json` | 보드 상태 자동 저장 (런타임 생성) |
| `레퍼런스_백업.xlsx` | 상품 추가 이력 백업 (런타임 생성) |

---

## 완료된 작업

### 핵심 기능
- [x] 상품 URL 입력 → Playwright로 자동 파싱 (이미지·상품명·가격·소재)
- [x] HTTP fallback 파서 (og:image 등 메타태그 기반)
- [x] 파싱 실패 시 수동 입력 모달 자동 오픈
- [x] 카드 드래그 이동 (상단 핸들 바 분리 — 이미지 클릭 충돌 방지)
- [x] 카드 이미지 클릭 시 로컬 파일 업로드 (canvas 리사이즈 → base64)
- [x] 카드 필드(상품명·가격·소재·메모) 더블클릭 인라인 편집
- [x] 카드 우상단 색상 라벨 (카테고리 구분)
- [x] URL 없이 빈 카드 수동 생성
- [x] 자유 텍스트 박스 추가 (T 버튼)
- [x] 도형 추가 — 사각형·원 (크기 조절 핸들 + 색상 피커)
- [x] Ctrl+C / Ctrl+V 인앱 클립보드 복사·붙여넣기
- [x] Delete / Backspace 선택 요소 삭제
- [x] 다중 탭 지원 (탭 추가·삭제·이름 더블클릭 변경)
- [x] 탭별 카드 전체 삭제 (Clear 버튼)

### 데이터 관리
- [x] localStorage 자동 저장 (브라우저 로컬)
- [x] 서버 측 board_state.json 저장 (재시작 후에도 유지)
- [x] 상품 추가 시 레퍼런스_백업.xlsx 자동 기록

### 실시간 협업 (Socket.IO)
- [x] Flask-SocketIO + eventlet 서버 구축
- [x] 접속 시 전체 상태 동기화 (state_sync)
- [x] 실시간 브로드캐스트: item_add / item_update / item_delete
- [x] 실시간 브로드캐스트: tab_add / tab_delete / tab_rename / tab_clear
- [x] 접속자 수 실시간 표시 (좌측 상단 상태 표시)
- [x] 서버 연결 상태 표시 (초록/빨강)

### 배포 준비
- [x] requirements.txt 생성
- [x] render.yaml 생성 (Playwright Chromium 포함 빌드 설정)
- [x] PORT 환경변수 대응 (Render 동적 포트)
- [x] RENDER 환경변수 감지 시 브라우저 오픈 스킵

### 버그 수정 (2026-03-26)
- [x] **스크래핑 전면 실패 수정** — 어떤 URL을 넣어도 이미지·상품명·가격을 가져오지 못하던 문제 해결
  - **원인 1: Playwright 빈 결과 시 fallback 미실행** — Playwright가 exception 없이 빈 결과를 반환하면 HTTP fallback이 동작하지 않음
    - 수정: Playwright → 빈 결과 시 HTTP fallback 자동 시도 → 두 결과 병합 (3단계 전략)
  - **원인 2: 봇 감지 차단** — User-Agent 오래됨(Chrome/124), `navigator.webdriver` 감지됨
    - 수정: Chrome/131로 업데이트, `navigator.webdriver` 숨기기, Sec-CH-UA 헤더 추가, `window.chrome` 에뮬레이션
  - **원인 3: 이미지 없으면 무조건 수동입력 모달** — 이미지만 없어도 카드 미생성
    - 수정: 이미지·상품명·가격 모두 없을 때만 수동 입력 모달 표시 (일부라도 있으면 카드 생성)
- [x] **가격 통화 중복 수정** — "KRW KRW 349000" → "KRW 349000" (ld+json에서 이미 통화 포함 시 meta 태그에서 재추가 방지)
- [x] **소재 오탐 수정** — extractMaterial이 "JSON", "HTML" 등 기술 용어를 소재로 잘못 추출하던 문제 필터링 추가

---

## 앞으로 해야 할 작업

### 즉시 필요
- [ ] **GitHub repository 생성 및 파일 업로드**
  - 업로드 대상: html, py, requirements.txt, render.yaml
  - 제외 대상: board_state.json, 레퍼런스_백업.xlsx, __pycache__
- [ ] **Render.com 배포**
  - GitHub repo 연결
  - Start Command: `python product_board_server.py`
  - 배포 완료 후 URL 확인

### 배포 후 개선 검토
- [ ] **데이터 영속성 문제 해결**
  - Render 무료 플랜은 재시작 시 board_state.json 초기화됨
  - 해결 방안: Redis / SQLite + Render Disk / 외부 DB 연동
- [ ] **.gitignore 추가** (board_state.json, xlsx, __pycache__ 제외)

### 선택적 기능 추가 (요청 시)
- [ ] 카드 정렬·그룹화 기능
- [ ] 보드 이미지 전체 캡처·내보내기
- [ ] 특정 탭만 xlsx 백업
- [ ] 카드 검색·필터

---

## 실행 방법

### 로컬 실행 (팀원 없이 혼자)
```
실행.bat 더블클릭 → 브라우저 자동 오픈
```

### 팀원 협업 (같은 네트워크)
```
CMD 창에 표시되는 http://192.168.x.x:5000 주소를 팀원에게 공유
```

### 클라우드 배포 후 (Render.com)
```
https://[프로젝트명].onrender.com 주소를 팀원에게 공유
실행.bat 불필요 — 24시간 접속 가능
```

---

## 기술 스택
- **Frontend**: Vanilla HTML/CSS/JS, Socket.IO client
- **Backend**: Python, Flask, Flask-SocketIO, eventlet
- **Scraper**: Playwright (headless Chromium) + urllib fallback
- **Storage**: JSON 파일 (로컬), openpyxl xlsx 백업
- **Deploy**: Render.com (무료 플랜)
