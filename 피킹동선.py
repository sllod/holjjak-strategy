import streamlit as st

st.title("재고 배치 & 피킹 동선 시뮬레이터")

st.write("🚚 담당 구역이 없거나 출고 수량이 기억 안 나도 쉽게 입력할 수 있도록 만든 버전입니다!")

# 구역 관련 간단 입력
zones = st.number_input("오늘 이동한 구역 수 (예: 5)", min_value=1, value=5, step=1)
avg_visits = st.number_input("한 구역당 대략 몇 번씩 갔나요?", min_value=1, value=3, step=1)

# 오늘 작업량 느낌 선택
workload = st.radio(
    "오늘 작업량은 평소보다 어땠나요?",
    ("많이 적었다", "평소와 비슷했다", "매우 많았다")
)

# 현재 걸음 수 (대략)
current_steps = st.number_input("오늘 대략 걸은 총 걸음 수 (보)", min_value=1000, value=25000, step=1000)

# 시뮬레이션용 개선 입력
expected_steps = st.number_input("재배치 또는 동선 개선 후 예상 걸음 수 (보)", min_value=1000, value=20000, step=1000)

if st.button("시뮬레이션 분석하기"):
    stride_length = 0.7  # 평균 보폭(m)
    before_distance_km = current_steps * stride_length / 1000
    after_distance_km = expected_steps * stride_length / 1000

    saved_distance_km = before_distance_km - after_distance_km
    saved_steps = current_steps - expected_steps

    st.subheader("📊 분석 결과")
    st.write(f"오늘 이동한 구역 수: **{zones}개**, 평균 방문 횟수: **{avg_visits}회**")
    st.write(f"작업 느낌: **{workload}**")
    st.write(f"현재 총 이동 거리: **{before_distance_km:.1f} km**")
    st.write(f"개선 후 예상 이동 거리: **{after_distance_km:.1f} km**")
    st.write(f"예상 절감 거리: **{saved_distance_km:.1f} km**")
    st.write(f"예상 절감 걸음 수: **{saved_steps:,} 보**")

    st.subheader("💡 개선 효과")
    st.write("✅ 몸에 무리 줄이기")
    st.write("✅ 출고 속도 향상")
    st.write("✅ 사고 및 실수 감소")

    st.success("시뮬레이션 완료! 대략적인 느낌만으로도 충분히 개선 효과를 확인할 수 있습니다.")


