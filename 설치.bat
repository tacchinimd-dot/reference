@echo off
chcp 65001 > nul
echo ================================================
echo   상품 레퍼런스 보드 - 최초 설치
echo   (처음 한 번만 실행하면 됩니다)
echo ================================================
echo.

:: Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo        https://www.python.org 에서 Python을 설치한 후 다시 실행해주세요.
    echo        설치 시 "Add Python to PATH" 옵션을 반드시 체크하세요.
    pause
    exit /b 1
)

echo [1/3] Python 확인 완료
python --version

echo.
echo [2/3] 필요한 패키지 설치 중...
pip install flask flask-cors flask-socketio eventlet openpyxl playwright
if errorlevel 1 (
    echo [오류] 패키지 설치에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo [3/3] Playwright 브라우저 설치 중... (시간이 걸릴 수 있습니다)
playwright install chromium
if errorlevel 1 (
    echo [오류] 브라우저 설치에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   설치 완료!
echo   이제 실행.bat 을 더블클릭해서 사용하세요.
echo ================================================
pause
