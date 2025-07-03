import streamlit as st

st.title(" 물류센터 직원용 걸음 수 & 동선 분석 도구")

st.header("기본 정보 입력")

steps = st.number_input("오늘 걸은 총 걸음 수", min_value=0, value=25000, step=500)
work_hours = st.number_input("하루 작업 시간 (시간 단위)", min_value=0.0, value=10.0, step=0.5)
speed = st.number_input("평균 걷는 속도 (km/h)", min_value=1.0, value=4.0, step=0.5)
commute_included = st.checkbox("출퇴근 포함 여부", value=False)
target_distance = st.number_input("줄이고 싶은 목표 거리 (km)", min_value=0.0, value=2.0, step=0.5)

if st.button("오늘 내 동선 분석하기"):
    # 기본 계산
    stride_length = 0.7  # 평균 보폭 (m)
    total_distance_km = steps * stride_length / 1000

    walking_time_hours = total_distance_km / speed
    kcal = int(total_distance_km * 60)  # 대략 1km당 60kcal 소비 기준

    # 절감 효과
    time_saved_min = int((target_distance / speed) * 60)
    yearly_saved_hours = int((time_saved_min / 60) * 300)  # 연간 300일 기준
    estimated_cost_saving = yearly_saved_hours * 10000  # 예: 시간당 1만원 비용 가정

    st.subheader("분석 결과")
    st.write(f"오늘 총 이동 거리: **{total_distance_km:.1f} km**")
    st.write(f"순수 걷는 시간: **{walking_time_hours:.1f} 시간**")
    st.write(f"예상 소모 칼로리: **{kcal} kcal**")

    st.subheader("목표 거리 줄였을 때 예상 절감 효과")
    st.write(f"- 목표 거리: **{target_distance:.1f} km**")
    st.write(f"- 예상 절약 시간: **{time_saved_min}분**")
    st.write(f"- 연간 절약 시간: **{yearly_saved_hours}시간 이상**")
    st.write(f"- 연간 비용 절감 효과 (참고): **약 {estimated_cost_saving:,}원**")

    st.subheader("개선 팁")
    st.write("✅ 자주 찾는 물건은 입구 가까이에!")
    st.write("✅ 동선 구역만 나눠도 큰 효과!")
    st.write("✅ 검수대 위치만 조정해도 최소 500m 절약!")

    st.success("분석이 완료되었습니다. PDF 리포트 기능은 추후 추가 예정입니다!")

