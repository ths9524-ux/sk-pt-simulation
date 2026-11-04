import os
import streamlit as st
from openai import OpenAI

# 페이지 와이드 설정
st.set_page_config(
    page_title="SK하이닉스 신입 채용 면접 [문제해결PT]",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# API 키 및 클라이언트 초기화
# Streamlit Cloud 배포 시 Secrets의 GROQ_API_KEY 또는 OPENAI_API_KEY를 읽어옵니다.
api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("API 키가 설정되지 않았습니다. Streamlit Secrets에 GROQ_API_KEY 또는 OPENAI_API_KEY를 등록해주세요.")
    st.stop()

# Groq 키를 사용하시는 경우 기본 base_url 지정 (OpenAI 공식 키라면 base_url 인자 생략 가능)
if "gsk_" in api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    MODEL_NAME = "qwen-2.5-32b" # Groq 제공 Qwen 모델 또는 llama-3.1-8b-instant
else:
    client = OpenAI(api_key=api_key)
    MODEL_NAME = "gpt-4o-mini"

# CSS 스타일 및 레이아웃
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

# 1. 상단 바 (제목, 30분 카운트다운 타이머, 시험 종료 버튼)
col_head1, col_head2 = st.columns([6, 4])
with col_head1:
    st.markdown("<div class='top-title'>SK하이닉스 신입 채용 면접 [문제해결PT]</div>", unsafe_allow_html=True)

with col_head2:
    # 30:00 -> 00:00으로 1초씩 줄어드는 실시간 HTML/JS 타이머 컴포넌트
    timer_html = """
    <div style="display:flex; justify-content:flex-end; align-items:center; font-family:sans-serif;">
        <span style="font-size:15px; font-weight:600; color:#374151; margin-right:8px;">제한시간</span>
        <span id="countdown" style="font-size:18px; font-weight:700; color:#111827; min-width:65px; margin-right:15px;">30:00</span>
        <button style="background:#9ca3af; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:600; cursor:not-allowed;">최종 제출 및 시험 종료</button>
    </div>
    <script>
        let duration = 30 * 60; // 30분
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

# 2. 본문 3단 레이아웃 (좌측 문제 지문 : 중앙 답안 작성 : 우측 AI 채팅)
left_col, mid_col, right_col = st.columns([3, 4, 3])

# --- [좌측 컬럼: 문제 및 참고자료] ---
with left_col:
    st.markdown("""
    <div class="box-card">
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
    </div>
    """, unsafe_allow_html=True)

# --- [중앙 컬럼: 답안 작성란] ---
with mid_col:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:6px;">
        <h4 style="margin:0;">답안 작성</h4>
        <span style="font-size:11px; color:#ef4444;">답안은 내용 위주로 평가하며, 복사/붙여넣기 시 서식이 어긋나도 편하게 작성해 주세요.</span>
    </div>
    """, unsafe_allow_html=True)
    
    answer_text = st.text_area(
        label="답안 작성란",
        label_visibility="collapsed",
        height=540,
        placeholder="AI Agent를 활용하여 문제를 해결하며, 중요한 정보는 확인하세요..."
    )
    
    c_status, c_save = st.columns([6, 4])
    with c_status:
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
        if st.button("새 채팅", key="new_chat"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "안녕하세요. AI Literacy 인증 평가 진행에 도움을 드릴 AI Agent입니다."}
            ]
            st.rerun()

    # 대화 기록 유지
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요. AI Literacy 인증 평가 진행에 도움을 드릴 AI Agent입니다."}
        ]

    chat_box = st.container(height=490)
    for msg in st.session_state.chat_history:
        with chat_box.chat_message(msg["role"]):
            st.write(msg["content"])

    # 사용자 질의 입력
    if prompt := st.chat_input("내용을 입력하세요. (최대 4000자)"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with chat_box.chat_message("user"):
            st.write(prompt)

        # 시스템 지침 설정
        messages = [
            {
                "role": "system",
                "content": (
                    "당신은 SK하이닉스 문제해결 PT 평가를 지원하는 사내 AI Agent입니다. "
                    "지원자의 질의에 대해 명확하고 논리적인 의사결정 근거와 통찰을 한국어로 제공하세요."
                )
            }
        ]
        for msg in st.session_state.chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        with chat_box.chat_message("assistant"):
            with st.spinner("답변 작성 중..."):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=0.7,
                    )
                    reply_text = response.choices[0].message.content
                    st.write(reply_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply_text})
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")