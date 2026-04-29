import streamlit as st
import PyPDF2
import random

# --- 설정: 나만의 비밀번호를 정해줘! ---
MY_PASSWORD = "순두"  # <--- 여기에 원하는 비밀번호를 적어!

st.set_page_config(page_title="전기기사 암기 마스터", page_icon="⚡")

# --- 로그인 로직 ---
if 'login_success' not in st.session_state:
    st.session_state.login_success = False

if not st.session_state.login_success:
    st.title("🔐 접근 제한")
    pw_input = st.text_input("비밀번호를 입력해줘", type="password")
    if st.button("로그인"):
        if pw_input == MY_PASSWORD:
            st.session_state.login_success = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸어!")
    st.stop() # 로그인이 안 되면 아래 코드를 실행하지 않음

# --- 여기서부터는 로그인 성공 시 보이는 화면 ---
st.title("⚡ 전기기사 암기 마스터")
st.write("PDF를 업로드하면 자동으로 퀴즈를 만들어줄게!")

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

uploaded_file = st.file_uploader("정리한 PDF 파일을 올려줘", type="pdf")

if uploaded_file and st.button("🚀 퀴즈 생성하기"):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    lines = text.split('\n')
    temp_data = {}
    last_q = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if '?' in line:
            last_q = line
            temp_data[last_q] = ""
        elif last_q and temp_data.get(last_q) == "":
            temp_data[last_q] = line
            
    st.session_state.quiz_data = temp_data
    if temp_data:
        st.session_state.current_q = random.choice(list(temp_data.keys()))
        st.success(f"{len(temp_data)}개의 문제를 찾았어!")
    else:
        st.warning("문제를 찾지 못했어. PDF 텍스트 형식을 확인해줘!")

if st.session_state.quiz_data:
    st.divider()
    q = st.session_state.current_q
    st.subheader(f"📝 문제: {q}")
    
    with st.expander("💡 정답 확인하기"):
        st.write(st.session_state.quiz_data[q])
        
    if st.button("다음 문제 넘어가기 ➡️"):
        st.session_state.current_q = random.choice(list(st.session_state.quiz_data.keys()))
        st.rerun()
