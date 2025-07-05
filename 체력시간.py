import streamlit as st

st.title("야근 & 체력 관리 시뮬레이터")

st.write("중소기업 근무시간과 체력 관리를 위한 현실 기반 시뮬레이터입니다.")

# 입력
work_hours = st.slider("주간 총 근무 시간 (시간)", 40, 80, 52)
steps = st.number_input("하루 평균 걸음수 (보)", min_value=0, value=12000, step=500)
overtime = st.checkbox("야근 포함")
age = st.slider("나이", 20, 65, 33)
rest_hours = st.slider("주간 휴식 시간 (시간)", 0, 20, 8)
stress = st.slider("스트레스 지수 (0=없음, 100=최고)", 0, 100, 70)

# 점수 계산
base_score = 80
fatigue_penalty = (work_hours - 40) * 1.2
age_penalty = (age - 30) * 1 if age > 30 else 0
overtime_penalty = 15 if overtime else 0
steps_bonus = (steps - 8000) * 0.0005 if steps > 8000 else 0

# 휴식시간 보너스/패널티
if rest_hours >= 10:
    rest_bonus = 5
elif rest_hours < 5:
    rest_bonus = -5
else:
    rest_bonus = 0

# 스트레스 패널티
if stress >= 80:
    stress_penalty = 15
elif stress >= 40:
    stress_penalty = 7
else:
    stress_penalty = 0

score = base_score - fatigue_penalty - age_penalty - overtime_penalty + steps_bonus + rest_bonus - stress_penalty
score = max(min(int(score), 100), 0)

# 출력
st.subheader("🏋️ 체력 관리 점수")
st.metric(label="예상 점수", value=f"{score} / 100")

if score < 50:
    st.error("체력 관리가 시급합니다! 휴식과 스트레스 관리가 꼭 필요합니다.")
elif score < 70:
    st.warning("주의가 필요합니다. 관리에 더 신경 써주세요!")
else:
    st.success("좋습니다! 현재 상태가 양호합니다. 꾸준히 관리하세요.")

# 추천 팁
st.subheader("💡 추천 관리 팁")
st.write("""
- 출근 전 가벼운 스트레칭
- 근무 중 틈틈이 물 마시기
- 단백질, 견과류 등 간식 챙기기
- 퇴근 후 폼롤러나 간단한 홈트
- 주말엔 무조건 휴식 모드
- 스트레스 관리 (취미, 명상, 가벼운 산책 등)
""")

st.caption("※ 참고용이며, 실제 건강 상태는 전문가와 상담하세요.")
