import streamlit as st
import random

# 1. 암기 데이터 (이미지 내용을 바탕으로 제가 직접 타이핑했습니다!)
QUIZ_DATA = [
    {"q": "무손실 선로의 감쇄정수(α)와 위상정수(β)를 표현하면?", "a": "α=0, β=ω√LC"},
    {"q": "무왜형 선로의 감쇄정수(α)와 위상정수(β)를 표현하면?", "a": "α=√RG, β=ω√LC"},
    {"q": "켈빈의 법칙이란?", "a": "가장 경제적인 전선의 굵기를 산정하는 방법"},
    {"q": "변압기 델타 결선의 장점은?", "a": "제3고조파를 제거할 수 있다"},
    {"q": "페란티 효과의 원인은?", "a": "정전용량 때문에 전압보다 위상이 앞선 충전전류가 클 때"},
    {"q": "직류기에서 정류를 개선하는 가장 효과적인 방법은?", "a": "보극 설치"},
    {"q": "동기기의 단락비가 크다는 것의 의미가 아닌 것은?", "a": "효율이 좋다 (실제론 효율이 나쁨)"},
    {"q": "KEC: 가공전선로 지표상 높이 규정 중 저압/고압 철도 횡단 시 높이는?", "a": "6.5m 이상"},
    {"q": "KEC: 지선(지지선)의 안전율은 얼마 이상인가?", "a": "2.5 이상"},
    {"q": "회로이론: 역률이란 무엇인가?", "a": "피상전력에 대한 유효전력의 비율"}
]

# 비밀번호 설정
MY_PASSWORD = "순두부" 

st.set_page_config(page_title="전기기사 객관식 마스터", page_icon="⚡")

# 로그인 로직
if 'login_success' not in st.session_state:
    st.session_state.login_success = False

if not st.session_state.login_success:
    st.title("🔐 전기기사 암기장 로그인")
    pw_input = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if pw_input == MY_PASSWORD:
            st.session_state.login_success = True
            st.rerun()
    st.stop()

# 앱 메인
st.title("⚡ 전기기사 핵심단답 객관식 퀴즈")
st.write("이미지 속 핵심 내용을 바탕으로 문제를 만듭니다.")

if 'current_idx' not in st.session_state:
    st.session_state.current_idx = random.randint(0, len(QUIZ_DATA)-1)
    st.session_state.options = []

def get_new_quiz():
    st.session_state.current_idx = random.randint(0, len(QUIZ_DATA)-1)
    correct = QUIZ_DATA[st.session_state.current_idx]['a']
    # 오답 생성
    others = [d['a'] for d in QUIZ_DATA if d['a'] != correct]
    wrong = random.sample(others, min(len(others), 3))
    options = wrong + [correct]
    random.shuffle(options)
    st.session_state.options = options

if not st.session_state.options:
    get_new_quiz()

# 퀴즈 출력
q_item = QUIZ_DATA[st.session_state.current_idx]
st.subheader(f"📝 문제: {q_item['q']}")

user_choice = st.radio("정답을 선택하세요:", st.session_state.options, key="quiz_radio")

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 정답 확인"):
        if user_choice == q_item['a']:
            st.balloons()
            st.success("정답입니다! 완벽해요!")
        else:
            st.error(f"오답입니다. 정답은: {q_item['a']}")
with col2:
    if st.button("➡️ 다음 문제"):
        get_new_quiz()
        st.rerun()

st.progress((st.session_state.current_idx + 1) / len(QUIZ_DATA))
