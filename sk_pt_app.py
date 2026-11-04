import streamlit as st
from openai import OpenAI

# 1. 페이지 와이드 레이아웃 설정
st.set_page_config(
    page_title="SK하이닉스 신입 채용 면접 [문제해결PT]",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. API 키 확인 및 Groq 클라이언트 초기화
if "GROQ_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 GROQ_API_KEY가 등록되지 않았습니다.")
    st.stop()

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# Groq에서 가장 추천하는 안정적인 한국어 추론 모델
MODEL_NAME = "llama-3.3-70b-versatile"

# 3. 전역 스타일링
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
    }
    .top-title {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-top: 4px;
    }
    .box-card {
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }
    .ref-btn {
        background-color: #1f2937;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 4. 상단 헤더 및 30분 실시간 카운트다운 타이머
col_head1, col_head2 = st.columns([6, 4])
with col_head1:
    st.markdown("<div class='top-title'>SK하이닉스 신입 채용 면접 [문제해결PT]</div>", unsafe_allow_html=True)

with col_head2:
    timer_html = """
    <div style="display:flex; justify-content:flex-end; align-items:center; font-family:sans-serif;">
        <span style="font-size:15px; font-weight:600; color:#374151; margin-right:8px;">제한시간</span>
        <span id="countdown" style="font-size:18px; font-weight:700; color:#111827; min-width:65px; margin-right:15px;">30:00</span>
        <button style="background:#9ca3af; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:600; cursor:not-allowed;">최종 제출 및 시험 종료</button>
    </div>
    <script>
        let duration = 30 * 60;
        let display = document.getElementById('countdown');
        let interval = setInterval(function () {
            let minutes = parseInt(duration / 60, 10);
            let seconds = parseInt(duration % 60, 10);
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            display.textContent = minutes + ":" + seconds;
            if (--duration < 0) {
                clearInterval(interval);
                display.textContent = "00:00";
                display.style.color = "#ef4444";
            }
        }, 1000);
    </script>
    """
    st.components.v1.html(timer_html, height=45)

# 5. 본문 3분할 레이아웃
left_col, mid_col, right_col = st.columns([3, 4, 3])

# --- [좌측 컬럼: 문제 및 참고자료] ---
with left_col:
    st.markdown("""<div class="box-card">
<span style="color:#6b7280; font-size:12px; font-weight:600;">문제 1/1 [공통]</span>
<h4 style="margin-top:6px; margin-bottom:12px;">신규 사업 적정성 평가 및 의사결정 보고서 작성</h4>
<b>문제 지문</b>
<div style="font-size:13px; color:#4b5563; line-height:1.6; margin-top:8px;">
AI 도입 및 반도체 신규 패키징 라인 구축과 관련된 사업성을 검토하고, 예상되는 리스크와 이에 대한 해결 방안을 포함한 종합 의사결정 보고서를 작성하시오.<br><br>
제시된 참고자료와 AI Agent와의 질의응답을 적극 활용하여 논리적인 결론을 도출하십시오.
</div>
<hr style="margin: 14px 0; border: none; border-top: 1px solid #e5e7eb;">
<b>제출 형식</b>
<p style="font-size:12px; color:#6b7280; margin-top:4px;">신규 사업 적정성 평가 및 의사결정 보고서 (3000자 이내)</p>
</div>
<div class="box-card">
<span style="background:#fee2e2; color:#ef4444; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;">참고자료</span>
<div style="margin-top:12px; font-size:13px; display:flex; justify-content:space-between; align-items:center;">
<span>1. 생성형 AI 도입 사례 연구 보고서.pdf</span>
<span class="ref-btn">보기</span>
</div>
<div style="margin-top:10px; font-size:13px; display:flex; justify-content:space-between; align-items:center;">
<span>2. 생성형 AI의 경제적 잠재력.pdf</span>
<span class="ref-btn">보기</span>
</div>
</div>""", unsafe_allow_html=True)

# --- [중앙 컬럼: 답안 작성란] ---
with mid_col:
    st.markdown("""<div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:6px;">
<h4 style="margin:0;">답안 작성</h4>
<span style="font-size:11px; color:#ef4444;">답안은 내용 위주로 평가하며, 복사/붙여넣기 시 서식이 어긋나도 편하게 작성해 주세요.</span>
</div>""", unsafe_allow_html=True)

    st.text_area(
        label="답안 작성란",
        label_visibility="collapsed",
        height=540,
        placeholder="AI Agent를 활용하여 문제를 해결하며, 중요한 정보는 확인하세요..."
    )

    c_stat, c_save = st.columns([6, 4])
    with c_stat:
        st.markdown("<div style='margin-top:10px; font-size:13px; color:#6b7280;'><b>상태 |</b> 저장되지 않음</div>", unsafe_allow_html=True)
    with c_save:
        if st.button("임시저장", use_container_width=True):
            st.toast("답안이 임시저장되었습니다.")

# --- [우측 컬럼: AI Agent 채팅창] ---
with right_col:
    chat_h1, chat_h2 = st.columns([7, 3])
    with chat_h1:
        st.markdown("<h4 style='margin:0;'>AI 채팅</h4>", unsafe_allow_html=True)
    with chat_h2:
        if st.button("새 채팅", key="new_chat_btn"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "안녕하세요. AI Literacy 인증 평가 진행에 도움을 드릴 AI Agent입니다."}
            ]
            st.rerun()

    # 대화 기록 유지
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요. AI Literacy 인증 평가 진행에 도움을 드릴 AI Agent입니다."}
        ]

    # 채팅 메시지 출력 컨테이너
    chat_box = st.container(height=480)

    # 입력 폼
    with st.form("chat_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns([8, 2])
        with f_col1:
            user_input = st.text_input("질문 입력", placeholder="내용을 입력하세요. (최대 4000자)", label_visibility="collapsed")
        with f_col2:
            submit_btn = st.form_submit_button("전송", use_container_width=True)

    # 전송 버튼 클릭 시 질문 처리 및 API 호출
    if submit_btn and user_input.strip():
        prompt = user_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # LLM 프롬프트 구성
        messages = [
            {
                "role": "system",
                "content": (
                    "당신은 SK하이닉스 문제해결 PT 평가를 지원하는 사내 AI Agent입니다. "
                    "지원자의 질의에 대해 논리적이고 구체적인 의사결정 근거와 통찰을 한국어로 제공하세요."
                )
            }
        ]
        for msg in st.session_state.chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        try:
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
            )
            ans = res.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"오류 발생: {str(e)}"})

    # 화면에 대화 내역 렌더링
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
