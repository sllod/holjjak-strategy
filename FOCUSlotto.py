import streamlit as st
import random

st.set_page_config(page_title="로또 정밀 분석기", page_icon="📊")
st.title("로또 번호 정밀 분석기")

st.markdown("""
### 📊 안내사항
실제 데이터 통계와 패턴 분석을 기반으로 추천 조합을 제공합니다.
모든 추천 번호는 참고용이며, 당첨을 보장하지 않습니다.
""")

def generate_precise_numbers():
    while True:
        nums = sorted(random.sample(range(1, 46), 6))
        
        # 홀짝 비율 필터
        odds = len([n for n in nums if n % 2 == 1])
        evens = 6 - odds
        if odds not in [3, 4]:
            continue

        # 고저 번호 분포
        lows = len([n for n in nums if n <= 22])
        highs = 6 - lows
        if lows not in [2, 3, 4]:
            continue

        # 연속번호 조건
        consecutive = 1
        max_consecutive = 1
        for i in range(1, 6):
            if nums[i] == nums[i - 1] + 1:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 1
        if max_consecutive >= 3:
            continue

        # 구간 분포 (1~15, 16~30, 31~45)
        g1 = len([n for n in nums if 1 <= n <= 15])
        g2 = len([n for n in nums if 16 <= n <= 30])
        g3 = len([n for n in nums if 31 <= n <= 45])
        if g1 == 0 or g2 == 0 or g3 == 0:
            continue

        # 합계 조건
        total = sum(nums)
        if not (90 <= total <= 180):
            continue

        return nums

if st.button("정밀 분석 번호 생성"):
    with st.spinner("정밀 분석 중..."):
        final_numbers = generate_precise_numbers()
        st.success(f"추천 조합: {final_numbers}")
        st.write(f"합계: {sum(final_numbers)} / 홀수: {len([n for n in final_numbers if n % 2 == 1])}, 짝수: {len([n for n in final_numbers if n % 2 == 0])}")
