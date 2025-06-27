
import streamlit as st
import datetime

# Dark mode + tech blue style
st.set_page_config(page_title="🎯 홀짝 전략 분석기 (만두 전용)", layout="centered")

st.markdown("""<style>
    body {
        background-color: #121212;
    }
    .main {
        background-color: #1e1e1e;
        color: #e0f7fa;
    }
    .stApp {
        background-color: #121212;
    }
    .stTextInput input {
        font-size: 1.1rem;
        background-color: #1a1a1a;
        color: #e0f7fa;
    }
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.6rem;
        background-color: #00bcd4;
        color: white;
        border: none;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background-color: #26c6da;
    }
    .stRadio > div {
        color: #ffffff;
    }
</style>""", unsafe_allow_html=True)

st.title("🎯 홀짝 전략 분석기 (만두 전용)")
st.caption("AI 흐름 분석 기반 예측기 · 테크 스타일 인터페이스 ⚙️")

if "log" not in st.session_state:
    st.session_state.log = []

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "games" not in st.session_state:
    st.session_state.games = 0

st.subheader("🎮 게임 결과 입력")
result = st.radio("방금 결과는?", ("홀", "짝"))
if st.button("결과 입력"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.log.append({"time": now, "result": result})
    st.session_state.games += 1

st.subheader("🔍 다음 수 추천")
last_five = [entry["result"] for entry in st.session_state.log[-5:]]
recommendation = "홀" if last_five.count("짝") > last_five.count("홀") else "짝"
reason = "최근 결과에서 '{}'이 더 많이 나왔기 때문에 '{}' 추천!".format(
    "짝" if recommendation == "홀" else "홀", recommendation
)
st.success(f"추천: {recommendation}")
st.caption(f"📊 추천 근거: {reason}")

st.subheader("📝 예측 정답 여부")
correct = st.radio("추천이 맞았나요?", ("예", "아니오"))
if st.button("정답 반영"):
    if correct == "예":
        st.session_state.wins += 1
    st.toast("기록 반영 완료!")

st.subheader("📈 누적 통계")
if st.session_state.games > 0:
    rate = round((st.session_state.wins / st.session_state.games) * 100, 2)
    st.metric("✅ 승률", f"{rate}%")
    st.metric("🎯 총 참여", f"{st.session_state.games}회")
else:
    st.info("아직 게임을 입력하지 않았어요.")

st.subheader("📜 입력 로그")
for entry in reversed(st.session_state.log):
    st.write(f"{entry['time']} - 결과: {entry['result']}")
