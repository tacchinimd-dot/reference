"""
상품 레퍼런스 보드 실행기
- 실행.bat 을 더블클릭하거나
- 터미널에서 python launch.py 로 실행하세요
"""

import sys, os, threading, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import product_board_server
except Exception as e:
    print(f"  오류: product_board_server 로드 실패 — {e}")
    input("  Enter 를 눌러 종료...")
    sys.exit(1)

URL = "http://localhost:5000"

print("  서버를 시작하는 중...")

# ── 서버 실행 (non-daemon: 메인 스레드가 꺼져도 유지) ────
def run_server():
    try:
        product_board_server.start(open_browser=False)
    except OSError as e:
        print(f"\n  오류: 서버 시작 실패 — {e}")
        print("  포트 5000이 이미 사용 중일 수 있습니다.")
        os._exit(1)

server_thread = threading.Thread(target=run_server, daemon=False)
server_thread.start()

# ── 서버 준비 확인 후 브라우저 오픈 ──────────────────────
def wait_and_open():
    print("  서버 응답 대기 중", end="", flush=True)
    for _ in range(30):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(URL + "/ping", timeout=1)
            print("\n  서버 준비 완료!")
            print(f"  브라우저를 엽니다 → {URL}")
            os.startfile(URL)
            return
        except Exception:
            print(".", end="", flush=True)
    print("\n  서버가 응답하지 않습니다. 포트 5000 사용 여부를 확인해주세요.")

threading.Thread(target=wait_and_open, daemon=True).start()

# ── 메인 스레드 유지 ──────────────────────────────────────
try:
    server_thread.join()
except KeyboardInterrupt:
    print("\n  서버를 종료합니다.")
    os._exit(0)
