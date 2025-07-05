import streamlit as st

st.title("야근 & 체력 관리 시뮬레이터")

st.write("중소기업 근무시간과 체력 관리를 위한 간단한 시뮬레이터입니다.")

# 입력: 주간 근무시간
work_hours = st.slider("주간 총 근무 시간 (시간)", 40, 80, 52)

# 입력: 하루 평균 걸음수
steps = st.number_input("하루 평균 걸음수 (보)", min_value=0, value=15000, step=500)

# 입력: 야근 여부
overtime = st.checkbox("야근 포함")

# 입력: 연령
age = st.slider("나이", 20, 65, 30)

# 체력 점수 계산
base_score = 100
fatigue_penalty = (work_hours - 40) * 0.8
steps_bonus = (steps - 8000) * 0.001 if steps > 8000 else 0
age_penalty = (age - 30) * 0.5 if age > 30 else 0
overtime_penalty = 10 if overtime else 0

score = base_score - fatigue_penalty - age_penalty - overtime_penalty + steps_bonus
score = max(min(int(score), 100), 0)

# 결과 출력
st.subheader("🏋️ 체력 관리 점수")
st.metric(label="예상 점수", value=f"{score} / 100")

if score < 60:
    st.warning("체력 관리가 필요합니다! 스트레칭, 수분 섭취, 충분한 휴식을 꼭 챙기세요.")
elif score < 80:
    st.info("관리 중이지만 조금 더 신경 쓰면 좋습니다!")
else:
    st.success("좋습니다! 현재 체력 관리 상태가 양호합니다.")

# 추천 관리 팁
st.subheader("💡 추천 관리 팁")
st.write("""
- 출근 전 가벼운 스트레칭
- 근무 중 틈틈이 물 마시기
- 단백질, 견과류 등 간식 챙기기
- 퇴근 후 폼롤러나 간단한 홈트
- 주말엔 무조건 휴식 모드
""")

st.caption("※ 이 시뮬레이터는 참고용이며, 실제 건강 상태는 전문가와 상담하세요.")
