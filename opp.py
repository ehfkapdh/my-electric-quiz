import streamlit as st
import random

# --- 1. 암기 데이터 (해설 내용 추가!) ---
QUIZ_DATA = [
    {
        "q": "무손실 선로의 감쇄정수(α)와 위상정수(β)를 표현하면?", 
        "a": "α=0, β=ω√LC",
        "desc": "무손실 선로는 R=0, G=0인 선로를 말해! 그래서 감쇄가 없으니 α=0이고, 속도는 일정하게 유지되는 상태야."
    },
    {
        "q": "무왜형 선로의 감쇄정수(α)와 위상정수(β)를 표현하면?", 
        "a": "α=√RG, β=ω√LC",
        "desc": "무왜형 조건은 RC=LG일 때야. 이때 감쇄정수 α는 √RG로 최소가 되고, 위상정수는 무손실과 같아져!"
    },
    {
        "q": "켈빈의 법칙(Kelvin's Law)이란 무엇인가?", 
        "a": "가장 경제적인 전선의 굵기를 산정하는 방법",
        "desc": "전선 한 가닥의 연간 이자 및 감가상각비와 연간 전력 손실량의 요금이 같아지는 굵기가 가장 경제적이라는 법칙이야."
    },
    {
        "q": "변압기 델타(Δ) 결선의 가장 큰 장점은?", 
        "a": "제3고조파를 제거할 수 있다",
        "desc": "Δ 결선 내부에 제3고조파가 순환하므로 선로에 나타나지 않아. 통신선 유도장해를 방지하는 데 유리해!"
    },
    {
        "q": "KEC: 가공전선로 지표상 높이 규정 중 철도 횡단 시 높이는?", 
        "a": "6.5m 이상",
        "desc": "철도를 횡단하는 경우 저압, 고압, 특고압 상관없이 레일면상 6.5m 이상을 유지해야 해!"
    },
    {
        "q": "KEC: 지선(지지선)의 안전율은 얼마 이상으로 해야 하는가?", 
        "a": "2.5 이상",
        "desc": "지선의 안전율은 2.5 이상, 인장하중은 최소 4.31kN 이상이어야 해. 그리고 지선은 철탑의 강도를 보강하기 위해 사용해."
    },
    {
        "q": "동기기에서 단락비가 크다는 것의 특징으로 틀린 것은?", 
        "a": "효율이 좋다",
        "desc": "단락비가 크면 안정도는 높고 전압 변동률은 작지만, 기계가 크고 무거워지며 손실이 많아 효율은 나빠져!"
    }
]

# 비밀번호 설정
MY_PASSWORD = "순두부" 

st.set_page_config(page_title="전기기사 퀴즈 & 해설", page_icon="⚡")

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

# --- 앱 메인 기능 ---
st.title("⚡ 전기기사 핵심단답 마스터")
st.caption("문제를 풀고 상세 해설로 복습하세요!")

# 상태 관리
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = random.randint(0, len(QUIZ_DATA)-1)
    st.session_state.options = []
    st.session_state.show_ans = False

def get_new_quiz():
    st.session_state.current_idx = random.randint(0, len(QUIZ_DATA)-1)
    st.session_state.show_ans = False
    correct = QUIZ_DATA[st.session_state.current_idx]['a']
    others = [d['a'] for d in QUIZ_DATA if d['a'] != correct]
    wrong = random.sample(others, min(len(others), 3))
    options = wrong + [correct]
    random.shuffle(options)
    st.session_state.options = options

if not st.session_state.options:
    get_new_quiz()

# 문제 화면
q_item = QUIZ_DATA[st.session_state.current_idx]
st.info(f"📝 **문제**: {q_item['q']}")

# 정답 선택
user_choice = st.radio("보기 중에서 골라보세요:", st.session_state.options, key="quiz_radio")

if st.button("🔔 정답 및 해설 확인"):
    st.session_state.show_ans = True

# 정답 확인 및 해설 출력
if st.session_state.show_ans:
    if user_choice == q_item['a']:
        st.success("🎯 **정답입니다!**")
    else:
        st.error(f"❌ **틀렸습니다!** 정답은 **[{q_item['a']}]** 입니다.")
    
    # 상세 해설 박스
    st.markdown("---")
    st.markdown("🔍 **상세 해설**")
    st.write(q_item['desc'])
    
    if st.button("➡️ 다음 문제 풀기"):
        get_new_quiz()
        st.rerun()
