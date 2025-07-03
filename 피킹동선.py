import streamlit as st

st.title("재고 배치 & 피킹 동선 시뮬레이터")

st.write("🚚 재고 배치와 피킹 동선에 따라 얼마나 걸음 수와 시간이 차이 나는지 직접 확인해보세요!")

# 기본 입력
zones = st.number_input("현재 작업 구역 개수 (예: 5)", min_value=1, value=5, step=1)
total_items = st.number_input("하루 처리해야 할 제품 개수", min_value=1, value=300, step=10)
current_steps = st.number_input("현재 하루 걸음 수 (보)", min_value=1000, value=25000, step=1000)

# 개선 시뮬레이션 입력
reduced_zones = st.number_input("구역 재배치 후 예상 구역 개수", min_value=1, value=3, step=1)
expected_steps = st.number_input("재배치 후 예상 걸음 수 (보)", min_value=1000, value=20000, step=1000)

if st.button("시뮬레이션 분석하기"):
    stride_length = 0.7  # 평균 보폭(m)
    before_distance_km = current_steps * stride_length / 1000
    after_distance_km = expected_steps * stride_length / 1000

    # 절감 효과
    saved_distance_km = before_distance_km - after_distance_km
    saved_steps = current_steps - expected_steps

    st.subheader("📊 분석 결과")
    st.write(f"현재 총 이동 거리: **{before_distance_km:.1f} km**")
    st.write(f"재배치 후 예상 이동 거리: **{after_distance_km:.1f} km**")
    st.write(f"예상 절감 거리: **{saved_distance_km:.1f} km**")
    st.write(f"예상 절감 걸음 수: **{saved_steps:,} 보**")

    st.subheader("💡 개선 효과")
    st.write("✅ 몸에 무리 줄이기")
    st.write("✅ 출고 속도 향상")
    st.write("✅ 사고 및 실수 감소")

    st.success("시뮬레이션 완료! 작은 변화가 큰 차이를 만든다는 걸 느껴보세요.")

