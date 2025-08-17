# SRT 자동예매 매크로 (Streamlit GUI 버전)

사용자가 웹 GUI를 통해 편리하게 SRT 표를 예매할 수 있도록 돕는 프로그램입니다.

## 주요 기능
- **사용자 친화적 GUI**: Streamlit을 사용하여 모든 정보를 웹 인터페이스에서 쉽게 입력하고 제어할 수 있습니다.
- **자동 ChromeDriver 관리**: `webdriver-manager`가 자동으로 `chromedriver`를 다운로드하고 관리해주므로, 번거로운 수동 설치가 필요 없습니다.
- **실시간 로그**: 매크로의 모든 동작 상태를 실시간으로 확인할 수 있습니다.
- **자동 스크롤**: 로그가 업데이트될 때마다 최신 로그가 자동으로 보이도록 스크롤됩니다.
- **최신 로그 우선 표시**: 가장 최근의 로그 메시지가 맨 위에 표시됩니다.
- **간편한 시작/중지**: 버튼 클릭 한 번으로 매크로를 시작하고 안전하게 중지할 수 있습니다.

## 설치 및 실행 (권장: uv)

1) uv 설치 (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

2) 의존성 동기화 및 앱 실행 (cmd)

```cmd
uv venv
uv sync
uv run streamlit run streamlit_app.py
```

Troubleshooting (잠금/해결 이슈 시):

```cmd
uv lock --upgrade
uv sync
```

## 사용법

1.  **Streamlit 앱 실행:**
    uv를 사용하는 경우 위 설치 절차의 마지막 명령으로 실행됩니다. pip를 사용할 경우 아래 참고를 확인하세요.

2.  **정보 입력:**
    웹 브라우저에 나타난 사이드바에서 아래 정보를 입력합니다.
    - SRT 회원번호
    - 비밀번호
    - 출발역 / 도착역
    - 출발일 및 시간
    - 조회할 기차 범위

3.  **매크로 시작:**
    `매크로 시작` 버튼을 클릭하면 자동 예매가 시작됩니다. `매크로 중지` 버튼을 누르면 안전하게 작업이 종료됩니다.

## 주의사항
- 같은 IP로 단기간에 너무 많은 요청을 보내면 SRT 보안 정책에 따라 해당 IP가 일시적으로 차단될 수 있습니다.
- 매크로 실행 중에는 웹 브라우저를 닫지 마세요.
 - 과도한 트래픽을 피하기 위해 조회 반복 사이에 최소 3~7초 랜덤 대기하도록 동작합니다.

---

## (선택) pip/venv로 실행하는 전통적 방법

uv를 사용할 수 없는 환경에서만 사용하세요.

1) 가상환경 생성/활성화

```cmd
python -m venv .venv
.venv\Scripts\activate
```

2) 의존성 설치 및 실행

```cmd
pip install -r requirements.txt
streamlit run streamlit_app.py
```

참고: 본 프로젝트는 `pyproject.toml`을 기준으로 관리되며 `requirements.txt`는 호환성 유지를 위해서만 남겨둡니다.