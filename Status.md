  # 상품 레퍼런스 보드 — 배포 가이드

  > 이 문서는 아무것도 모르는 상태에서 시작해 실시간 협업 대시보드를 새로운
  URL로 배포하는 것을 목표로 합니다.
  > Claude Code에게 이 파일을 읽게 한 뒤 질문하면 단계별로 안내받을 수
  있습니다.

  ---

  ## 1. 이 프로젝트가 무엇인가요?

  팀원들이 URL 하나만으로 동시에 접속해 상품 레퍼런스를 실시간으로
  추가·수정·삭제할 수 있는 웹 대시보드입니다.

  - 별도 설치 없이 브라우저만으로 사용 가능
  - 한 명이 수정하면 접속 중인 모든 사람에게 즉시 반영
  - 탭 구분, 상품 카드, 웹 스크래핑, Excel 내보내기 기능 포함

  ---

  ## 2. 파일 구조

  ```
  reference/
  ├── product_board_server.py       # Flask + Socket.IO 서버 (백엔드)
  ├── product_reference_board.html  # 대시보드 UI (프론트엔드)
  ├── requirements.txt              # Python 패키지 목록
  ├── render.yaml                   # Render 배포 설정
  └── STATUS.md                     # 이 문서
  ```

  ---

  ## 3. 배포 방법 (처음부터 끝까지)

  ### Step 1. GitHub 저장소 복사 (Fork)

  1. https://github.com/tacchinimd-dot/reference 접속
  2. 우측 상단 **`Fork`** 버튼 클릭
  3. **`Create fork`** 클릭
  4. 본인 계정에 동일한 파일들이 복사됩니다

  > GitHub 계정이 없다면 https://github.com 에서 무료로 가입 후 진행하세요.

  ---

  ### Step 2. Render 계정 만들기

  1. https://render.com 접속
  2. **`Get Started for Free`** 클릭
  3. GitHub 계정으로 로그인 (권장)

  ---

  ### Step 3. Render에서 새 서비스 만들기

  1. Render 대시보드에서 **`New +`** → **`Web Service`** 클릭
  2. **`Connect a repository`** 선택
  3. GitHub 계정 연결 후 방금 Fork한 저장소(`reference`) 선택
  4. 아래와 같이 설정:

  | 항목 | 값 |
  |------|-----|
  | Name | 원하는 이름 (예: my-reference-board) |
  | Region | Singapore (한국과 가장 가까움) |
  | Branch | main |
  | Runtime | Python 3 |
  | Build Command | `pip install -r requirements.txt && playwright
  install-deps chromium && playwright install chromium` |
  | Start Command | `python product_board_server.py` |
  | Plan | **Free** |

  5. **`Environment Variables`** 섹션에서 **`Add Environment Variable`**
  클릭:
     - Key: `RENDER` / Value: `true`

  6. **`Create Web Service`** 클릭

  ---

  ### Step 4. 배포 완료 확인

  - 배포에 3~5분 소요됩니다
  - Logs 탭에서 아래 메시지가 보이면 성공:
    ```
    ==> Your service is live 🎉
    ```
  - 상단에 표시된 URL (예: `https://my-reference-board.onrender.com`) 접속
  - 좌측 상단에 **"● 연결됨"** 표시 확인

  ---

  ### Step 5. 서버 상시 유지 설정 (UptimeRobot)

  Render 무료 플랜은 15분간 접속이 없으면 서버가 잠듭니다.
  UptimeRobot으로 주기적으로 ping을 보내 잠들지 않게 합니다.

  1. https://uptimerobot.com 접속 → 무료 가입
  2. **`Add New Monitor`** 클릭
  3. 설정:
     - Monitor Type: `HTTP(s)`
     - Friendly Name: 원하는 이름
     - URL: Render에서 받은 URL
     - Monitoring Interval: `5 minutes`
  4. **`Create Monitor`** 클릭

  ---

  ## 4. 배포 과정에서 발생했던 문제들과 해결 방법

  실제 배포 과정에서 아래 문제들이 발생했습니다. 동일한 에러가 발생하면 이
  내용을 참고하세요.

  ---

  ### 문제 1. Socket.IO 프로토콜 버전 불일치
  ```
  The client is using an unsupported version of the Socket.IO or Engine.IO
  protocols
  ```
  **원인**: `eventlet` 라이브러리가 deprecated되면서 서버-클라이언트 간
  프로토콜 버전이 맞지 않음
  **해결**: `async_mode`를 `eventlet`에서 `threading`으로 변경, `eventlet`
  패키지 제거

  ---

  ### 문제 2. Werkzeug 프로덕션 에러
  ```
  RuntimeError: The Werkzeug web server is not designed to run in
  production.
  ```
  **원인**: `threading` 모드에서 Werkzeug 서버를 프로덕션 환경에서
  사용하려면 명시적 허용 필요
  **해결**: `socketio.run()`에 `allow_unsafe_werkzeug=True` 옵션 추가

  ---

  ### 문제 3. socket.io.js 400 에러
  ```
  GET /socket.io/socket.io.js HTTP/1.1" 400
  ```
  **원인**: `python-socketio 5.x`부터 서버에서 `/socket.io/socket.io.js`
  파일을 직접 제공하지 않음
  **해결**: HTML에서 해당 경로 대신 CDN URL로 변경

  ```html
  <!-- 변경 전 -->
  <script src="/socket.io/socket.io.js"></script>

  <!-- 변경 후 -->
  <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
  ```

  ---

  ## 5. 자주 묻는 질문

  **Q. 배포 후 "서버 꺼짐"이 표시돼요**
  A. Render Logs 탭에서 에러 메시지를 확인하세요. 위 "문제들과 해결 방법"
  섹션을 참고하거나, 에러 메시지를 Claude Code에 붙여넣어 질문하세요.

  **Q. 여러 팀이 각자 다른 URL을 써도 되나요?**
  A. 네. 각 팀이 이 저장소를 Fork해서 각자 Render에 배포하면 독립된 URL과
  데이터로 운영됩니다.

  **Q. 데이터가 사라져요**
  A. Render 무료 플랜은 재배포 시 서버 내 파일이 초기화됩니다. 중요한
  데이터는 Excel 내보내기 기능으로 백업하세요.

  **Q. 접속자가 많으면 느려지나요?**
  A. Render 무료 플랜은 소규모 팀(10명 이하)에 적합합니다. 더 많은 인원이
  필요하면 유료 플랜($7/월) 업그레이드를 권장합니다.

  ---

  ## 6. Claude Code에게 질문하는 방법

  이 저장소를 받은 후 Claude Code에서 아래와 같이 질문하세요:

  ```
  STATUS.md 파일과 GitHub 저장소(https://github.com/[내 계정]/reference)를
  읽고, 새로운 URL로 배포하는 것을 처음부터 도와주세요.
  ```

  Claude Code가 이 문서를 읽고 단계별로 안내합니다.
