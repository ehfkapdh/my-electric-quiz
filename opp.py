import streamlit as st
import PyPDF2
import random

st.set_page_config(page_title="전기기사 암기 마스터", page_icon="⚡")

st.title("⚡ 전기기사 암기 마스터")
st.write("PDF를 업로드하면 자동으로 퀴즈를 만들어줄게!")

# 세션 상태 초기화 (문제를 기억하기 위함)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

# 1. PDF 업로드 기능
uploaded_file = st.file_uploader("정리한 PDF 파일을 올려줘", type="pdf")

if uploaded_file and st.button("🚀 퀴즈 생성하기"):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # 이미지의 고양이(?) 아이콘과 반짝이 아이콘 구조를 텍스트로 분리
    lines = text.split('\n')
    temp_data = {}
    last_q = None
    
    for line in lines:
        line = line.strip()
        if '?' in line: # 질문 추출
            last_q = line
            temp_data[last_q] = ""
        elif last_q and temp_data[last_q] == "": # 질문 바로 다음 줄을 정답으로
            temp_data[last_q] = line
            
    st.session_state.quiz_data = temp_data
    st.session_state.current_q = random.choice(list(temp_data.keys()))
    st.success(f"{len(temp_data)}개의 문제를 찾았어!")

# 2. 퀴즈 화면
if st.session_state.quiz_data:
    st.divider()
    q = st.session_state.current_q
    st.subheader(f"📝 문제: {q}")
    
    with st.expander("💡 정답 확인하기"):
        st.write(st.session_state.quiz_data[q])
        
    if st.button("다음 문제 넘어가기 ➡️"):
        st.session_state.current_q = random.choice(list(st.session_state.quiz_data.keys()))
        st.rerun()

# 3. 필요한 라이브러리 안내 (파일 하나 더 만들어야 해!)
st.sidebar.info("설정 방법: GitHub에 app.py와 requirements.txt를 만드세요.")
