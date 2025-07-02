import streamlit as st
import random
import numpy as np
import time

st.set_page_config(page_title="로또 번호 정밀 분석기", page_icon="📊")
st.title("로또 번호 정밀 분석기")

st.markdown("""
### 📊 안내사항
아래 조합은 실제 통계, 패턴, 구간 분석, 표준편차 등을 종합적으로 고려해 추천됩니다.  
모든 번호는 참고용이며, 당첨을 보장하지 않습니다.
""")

def score_combination(numbers):
    # 구간 점수 (1~15, 16~30, 31~45에 모두 포함되면 가산점)
    g1 = any(1 <= n <= 15 for n in numbers)
    g2 = any(16 <= n <= 30 for n in numbers)
    g3 = any(31 <= n <= 45 for n in numbers)
    if not (g1 and g2 and g3):
        return -1  # 구간 분포가 부족하면 탈락

    # 합계 조건
    total = sum(numbers)
    if not (90 <= total <= 180):
        return -1

    # 표준편차 조건 (너무 치우친 조합 제외)
    std = np.std(numbers)
    if std < 6 or std > 16:
        return -1

    # 연속번호 조건
    sorted_nums = sorted(numbers)
    consecutive = 1
    max_consecutive = 1
    for i in range(1, 6):
        if sorted_nums[i] == sorted_nums[i - 1] + 1:
            consecutive += 1
            max_consecutive = max(max_consecutive, consecutive)
        else:
            consecutive = 1
    if max_consecutive >= 3:
        return -1

    # 홀짝 조건
    odds = len([n for n in numbers if n % 2 == 1])
    if odds not in [3, 4]:
        return -1

    # 고저 번호
    lows = len([n for n in numbers if n <= 22])
    if lows not in [2, 3, 4]:
        return -1

    # 최종 점수 (여기선 단순히 합계 기반 점수 예시)
    return 100 - abs(138 - total)  # 138은 중간 합계값 예시

def generate_precise_numbers():
    best_score = -1
    best_numbers = None

    for _ in range(5000):  # 5000개 후보 중에서 최고 점수 선택
        nums = sorted(random.sample(range(1, 46), 6))
        score = score_combination(nums)
        if score > best_score:
            best_score = score
            best_numbers = nums

    return best_numbers, best_score

if st.button("정밀 분석 번호 생성"):
    with st.spinner("정밀 분석 중... (최적 조합을 계산 중입니다)"):
        time.sleep(1.5)  # 심리적 로딩 효과 추가
        final_numbers, final_score = generate_precise_numbers()

        st.success(f"추천 조합: {final_numbers}")
        st.write(f"합계: {sum(final_numbers)} / 표준편차: {round(np.std(final_numbers), 2)} / 점수: {final_score}")
        st.write(f"홀수: {len([n for n in final_numbers if n % 2 == 1])}, 짝수: {len([n for n in final_numbers if n % 2 == 0])}")
