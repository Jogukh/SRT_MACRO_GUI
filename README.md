# SRT 자동예매 매크로 (Streamlit GUI 버전)

사용자가 웹 GUI를 통해 편리하게 SRT 표를 예매할 수 있도록 돕는 프로그램입니다.

## 주요 기능
- **사용자 친화적 GUI**: Streamlit을 사용하여 모든 정보를 웹 인터페이스에서 쉽게 입력하고 제어할 수 있습니다.
- **자동 ChromeDriver 관리**: `webdriver-manager`가 자동으로 `chromedriver`를 다운로드하고 관리해주므로, 번거로운 수동 설치가 필요 없습니다.
- **실시간 로그**: 매크로의 모든 동작 상태를 실시간으로 확인할 수 있습니다.
- **자동 스크롤**: 로그가 업데이트될 때마다 최신 로그가 자동으로 보이도록 스크롤됩니다.
- **최신 로그 우선 표시**: 가장 최근의 로그 메시지가 맨 위에 표시됩니다.
- **간편한 시작/중지**: 버튼 클릭 한 번으로 매크로를 시작하고 안전하게 중지할 수 있습니다.

## 설치 방법

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/your-repository/SRT_MACRO_GUI.git
    cd SRT_MACRO_GUI
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **필요 라이브러리 설치:**
    `requirements.txt` 파일을 통해 모든 종속성을 한 번에 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
    *만약 `requirements.txt` 파일이 없다면 아래 명령어를 실행하세요.*
    ```bash
    pip install streamlit selenium webdriver-manager streamlit-scroll-to-top
    ```

## 사용법

1.  **Streamlit 앱 실행:**
    아래 명령어를 터미널에 입력하여 GUI를 실행합니다.
    ```bash
    streamlit run streamlit_app.py
    ```

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