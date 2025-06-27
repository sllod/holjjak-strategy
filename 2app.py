
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="홀짝 전략 분석기", layout="centered")
st.markdown("""<style>
    .main { padding-top: 2rem; }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 0.6rem;
    }
    .stSelectbox > div { font-size: 1.1rem; }
    .highlight-box {
        background-color: #dff0d8;
        padding: 1rem;
        border-radius: 12px;
        font-size: 1.4rem;
        font-weight: bold;
        color: #3c763d;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        border: 1px solid #ccc;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background: #f9f9f9;
    }
</style>""", unsafe_allow_html=True)

st.title("🎯 홀짝 전략 추천기 (만두 전용)")
st.caption("입력한 결과로 다음 판 예측! 스마트폰에 최적화됨")

if "logs" not in st.session_state:
    st.session_state.logs = []
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "total_recommended" not in st.session_state:
    st.session_state.total_recommended = 0

user_input = st.text_input("최근 결과 입력 (쉼표로 구분, 홀/짝):", placeholder="홀, 짝, 홀, 짝, 짝")
real_result = st.selectbox("실제 다음 결과는?", ["선택 안함", "홀", "짝"])

def analyze_strategy(results):
    encoded = [0 if r.strip() == "홀" else 1 for r in results if r.strip() in ["홀", "짝"]]
    if len(encoded) < 5:
        return "데이터 부족 (최소 5판 필요)", "-", None

    scores = {0: 0, 1: 0}
    reasons = []

    # 연속 패턴
    streak_target = encoded[-1]
    streak_len = 1
    for i in range(len(encoded)-2, -1, -1):
        if encoded[i] == streak_target:
            streak_len += 1
        else:
            break
    if streak_len >= 3:
        rec = 0 if streak_target == 1 else 1
        scores[rec] += 3
        reasons.append(f"연속 {streak_len}회 → 반전 예상")

    # 교차 패턴
    if len(encoded) >= 4 and all(encoded[i] != encoded[i+1] for i in range(3)):
        rec = 0 if encoded[-1] == 1 else 1
        scores[rec] += 2
        reasons.append("교차패턴 감지")

    # 순환 패턴
    pattern_length = 3
    if len(encoded) >= 2 * pattern_length:
        current = encoded[-pattern_length:]
        for i in range(len(encoded) - 2*pattern_length):
            if encoded[i:i+pattern_length] == current:
                if i+pattern_length < len(encoded):
                    rec = encoded[i+pattern_length]
                    scores[rec] += 2
                    reasons.append("과거 패턴 반복 감지")
                    break

    # 빈도 편중
    recent = encoded[-15:] if len(encoded) >= 15 else encoded
    h = recent.count(0)
    j = recent.count(1)
    if abs(h - j) >= 5:
        rec = 0 if h < j else 1
        scores[rec] += 1
        reasons.append(f"최근 {len(recent)}판에 {'홀' if h < j else '짝'} 저빈도")

    if scores[0] == scores[1]:
        return "기댓값 우위 없음 → 비추천", "-", None

    rec_final = 0 if scores[0] > scores[1] else 1
    rec_label = "홀" if rec_final == 0 else "짝"
    return f"추천: {rec_label}", "; ".join(reasons), rec_final

if user_input:
    results = user_input.split(",")
    recommendation, reason, rec_value = analyze_strategy(results)

    st.session_state.logs.append({
        "시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "입력값": user_input,
        "추천": recommendation,
        "근거": reason,
        "정답 여부": "미입력" if real_result == "선택 안함" else (
            "정답" if (real_result == "홀" and rec_value == 0) or (real_result == "짝" and rec_value == 1) else "오답"
        )
    })

    if real_result != "선택 안함" and rec_value is not None:
        st.session_state.total_recommended += 1
        if (real_result == "홀" and rec_value == 0) or (real_result == "짝" and rec_value == 1):
            st.session_state.correct_count += 1

    st.markdown(f"<div class='highlight-box'>{recommendation}</div>", unsafe_allow_html=True)
    st.caption(f"판단 근거: {reason}")

    df_log = pd.DataFrame(st.session_state.logs)
    st.subheader("📘 입력 로그 기록")
    st.dataframe(df_log, use_container_width=True)

    st.subheader("📈 누적 추천 통계")
    st.markdown(f"""<div class='metric-card'>총 분석 횟수: <b>{len(df_log)}회</b></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='metric-card'>추천 참여 수: <b>{st.session_state.total_recommended}회</b></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='metric-card'>정답 수: <b>{st.session_state.correct_count}회</b></div>""", unsafe_allow_html=True)
    if st.session_state.total_recommended > 0:
        winrate = st.session_state.correct_count / st.session_state.total_recommended * 100
        st.markdown(f"""<div class='metric-card'>적중률: <b>{winrate:.2f}%</b></div>""", unsafe_allow_html=True)
else:
    st.info("위 입력창에 '홀, 짝, 홀, ...'처럼 입력하고 엔터를 눌러줘")

