import streamlit as st
from itertools import combinations
import numpy as np
import time

st.set_page_config(page_title="로또 정밀 분석기", page_icon="📊")
st.title("로또 번호 정밀 분석기")

st.markdown("""
### 📊 안내사항
본 서비스는 모든 가능한 조합(814만 개)을 전부 탐색하여, 
패턴과 통계 기준으로 점수를 평가하고 상위 5개 조합을 추천합니다.
모든 번호는 참고용이며, 실제 당첨을 보장하지 않습니다.
번호 선택 및 구매는 전적으로 개인의 판단과 책임입니다.
""")

def score_combination(numbers):
    g1 = any(1 <= n <= 15 for n in numbers)
    g2 = any(16 <= n <= 30 for n in numbers)
    g3 = any(31 <= n <= 45 for n in numbers)
    if not (g1 and g2 and g3):
        return -1

    total = sum(numbers)
    if not (90 <= total <= 180):
        return -1

    std = np.std(numbers)
    if std < 6 or std > 16:
        return -1

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

    odds = len([n for n in numbers if n % 2 == 1])
    if odds not in [3, 4]:
        return -1

    lows = len([n for n in numbers if n <= 22])
    if lows not in [2, 3, 4]:
        return -1

    return 100 - abs(138 - total)

if st.button("완전 탐색 시작"):
    with st.spinner("모든 조합을 탐색 중... (수 분 소요됩니다)"):
        start_time = time.time()

        best_combinations = []

        count = 0
        for comb in combinations(range(1, 46), 6):
            count += 1
            score = score_combination(comb)
            if score > 0:
                best_combinations.append((list(comb), score))

            if count % 500000 == 0:
                st.info(f"진행 중... {count}개 평가 완료")

        best_combinations.sort(key=lambda x: x[1], reverse=True)

        top_5 = best_combinations[:5]

        end_time = time.time()
        st.success(f"완전 탐색 완료! (총 소요 시간: {round(end_time - start_time, 2)}초)")

        for idx, (nums, score) in enumerate(top_5, start=1):
            st.write(f"추천 조합 {idx}: {nums} / 점수: {score} / 합계: {sum(nums)} / 표준편차: {round(np.std(nums), 2)}")
