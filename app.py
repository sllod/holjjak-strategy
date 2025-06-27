
import streamlit as st
import pandas as pd
import datetime

# --- 타이틀 ---
st.title("🎯 홀짝 기댓값 전략 추천기 (동근 전용)")
st.write("네가 직접 참여한 홀/짝 결과만 입력하면, 다음 수에 참여해야 할지 알려줄게!")

# --- 세션 상태 초기화 ---
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- 입력창 ---
user_input = st.text_input("최근 참여한 결과 입력 (쉼표로 구분):", placeholder="홀, 짝, 짝, 홀, 홀")

# --- 분석 함수 ---
def analyze_strategy(results):
    encoded = [0 if r.strip() == "홀" else 1 for r in results if r.strip() in ["홀", "짝"]]
    if len(encoded) < 5:
        return "데이터 부족 (최소 5판 필요)", "-", None

    recent = encoded[-5:]
    hol_count = recent.count(0)
    jjak_count = recent.count(1)

    # 연속 분석
    streak_target = encoded[-1]
    streak_len = 1
    for i in range(len(encoded) - 2, -1, -1):
        if encoded[i] == streak_target:
            streak_len += 1
        else:
            break

    # 판단 로직
    if streak_len >= 3:
        recommended = 0 if streak_target == 1 else 1
        reason = f"{['홀','짝'][streak_target]} {streak_len}연속 → 반전 예상"
        return f"추천: {['홀','짝'][recommended]}", reason, recommended
    elif abs(hol_count - jjak_count) >= 3:
        recommended = 0 if hol_count < jjak_count else 1
        reason = f"최근 5판에 {'홀' if hol_count < jjak_count else '짝'} 편중"
        return f"추천: {['홀','짝'][recommended]}", reason, recommended
    else:
        return "기댓값 우위 없음 → 베팅 비추천", "-", None

# --- 실행 ---
if user_input:
    results = user_input.split(',')
    recommendation, reason, rec_value = analyze_strategy(results)

    # 로그 저장
    st.session_state.logs.append({
        "시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "입력값": user_input,
        "추천": recommendation,
        "근거": reason
    })

    st.subheader("📊 분석 결과")
    st.write(f"**{recommendation}**")
    st.caption(f"판단 근거: {reason}")

    # --- 누적 로그 표시 ---
    if st.session_state.logs:
        df_log = pd.DataFrame(st.session_state.logs)
        st.subheader("📘 입력 로그 기록")
        st.dataframe(df_log, use_container_width=True)

        # --- 승률 및 통계 ---
        total = len(df_log)
        recommend_count = df_log[~df_log["추천"].str.contains("비추천")].shape[0]
        rec_hol = df_log[df_log["추천"].str.contains("홀")].shape[0]
        rec_jjak = df_log[df_log["추천"].str.contains("짝")].shape[0]

        st.subheader("📈 누적 추천 통계")
        st.markdown(f"- 총 분석 횟수: **{total}회**")
        st.markdown(f"- 참여 추천 횟수: **{recommend_count}회**")
        st.markdown(f"  - 그중 홀 추천: **{rec_hol}회**")
        st.markdown(f"  - 그중 짝 추천: **{rec_jjak}회**")
else:
    st.info("위 입력창에 '홀, 짝, 홀, ...'처럼 입력하고 엔터를 눌러줘")
