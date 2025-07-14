# edit date : 2024-07-15
# version : 2.0.0

import streamlit as st
import streamlit_scroll_to_top
from srt_macro import run_macro
import datetime

st.set_page_config(page_title="SRT 예매 매크로", page_icon="🚄")

# --- 상태 초기화 ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'log_content' not in st.session_state:
    st.session_state.log_content = "매크로 시작 버튼을 눌러 예매를 시작하세요."

# 로그를 표시할 플레이스홀더
log_placeholder = st.empty()

# --- UI 구성 ---
st.title("🚄 SRT 예매 매크로")
st.caption("Streamlit으로 만든 사용자 친화적 인터페이스")

with st.sidebar:
    st.header("예매 정보 입력")
    
    member_number = st.text_input("SRT 회원번호", placeholder="회원번호")
    password = st.text_input("비밀번호", type="password", placeholder="****")
    
    st.divider()
    
    arrival = st.text_input("출발역", value="수서")
    departure = st.text_input("도착역", value="오송")
    
    today = datetime.date.today()
    selected_date = st.date_input("출발일", value=today)
    
    time_options = [f"{h:02d}" for h in range(0, 23, 2)]
    standard_time = st.selectbox("기준 시간 (2시간 간격)", options=time_options, index=6) # Default to 12:00
    
    st.divider()

    from_train, to_train = st.slider(
        "조회할 기차 범위",
        min_value=1, max_value=10, value=(1, 3)
    )

    try_waitlist = st.checkbox("예약 대기 신청 시도", value=True)
    
    st.warning("주의: 매크로 실행 중에는 다른 작업을 삼가주세요.")


# --- 컨트롤 버튼 ---
col1, col2, col3 = st.columns([1,1,5])

def start_macro():
    if not all([member_number, password, arrival, departure, selected_date, standard_time]):
        st.toast("🚨 모든 입력 필드를 채워주세요!", icon="🚨")
        return
        
    st.session_state.running = True
    st.session_state.logs = [] # 로그 초기화
    st.session_state.log_content = "매크로 시작 중...\n"


def stop_macro():
    st.session_state.running = False
    st.toast("매크로 중지를 요청했습니다. 현재 작업을 완료 후 종료됩니다.", icon="info")

with col1:
    st.button("매크로 시작", on_click=start_macro, disabled=st.session_state.running, type="primary")

with col2:
    st.button("매크로 중지", on_click=stop_macro, disabled=not st.session_state.running)


# --- 로그 출력 ---
# 기존 CSS 스타일은 유지하되, log-container 클래스는 직접 사용하지 않음
st.markdown("""
<style>
    .log-container { /* 이 스타일은 더 이상 직접 사용되지 않지만, 혹시 모를 다른 요소에 영향을 줄까봐 남겨�� */
        height: 400px;
        overflow-y: scroll;
        border: 1px solid #e6e6e6;
        border-radius: 5px;
        padding: 10px;
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

# 로그를 표시할 텍스트 영역


# --- 매크로 실행 로직 ---
if st.session_state.running:
    date_str = selected_date.strftime("%Y%m%d")

    for log in run_macro(member_number, password, arrival, departure, date_str, standard_time, from_train, to_train, try_waitlist):
        st.session_state.logs.insert(0, log)
        st.session_state.log_content = "\n".join(st.session_state.logs)
        log_placeholder.text_area("매크로 로그", value=st.session_state.log_content, height=400, disabled=True, key=f"log_textarea_{len(st.session_state.logs)}")

        if "🎉" in log:
            st.balloons()
            st.session_state.running = False
            st.rerun()


st.markdown("---")
st.markdown("Made with ❤️ by Gemini")
streamlit_scroll_to_top.st_scroll_to_top()
