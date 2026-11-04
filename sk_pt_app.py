# [우측 컬럼: AI Agent 채팅창]
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

    # 대화 기록 초기화
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요. AI Literacy 인증 평가 진행에 도움을 드릴 AI Agent입니다."}
        ]

    # 채팅 메시지 박스
    chat_box = st.container(height=480)

    # 입력 폼
    with st.form("chat_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns([8, 2])
        with f_col1:
            user_input = st.text_input("질문 입력", placeholder="내용을 입력하세요. (최대 4000자)", label_visibility="collapsed")
        with f_col2:
            submit_btn = st.form_submit_button("전송", use_container_width=True)

    # 전송 버튼 클릭 시 처리
    if submit_btn and user_input.strip():
        prompt = user_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # LLM 호출용 메시지 구성
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
            # Groq API 호출
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
            )
            ans = res.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"오류 발생: {str(e)}"})

    # 세션에 쌓인 대화 목록을 순서대로 출력 (rerun 없이 자연스럽게 표시)
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
