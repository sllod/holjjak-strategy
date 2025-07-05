import streamlit as st
from itertools import combinations
import numpy as np
import time
import random
import datetime

st.set_page_config(page_title="로또 정밀 분석기", page_icon="📊")
st.title("로또 번호 정밀 분석기")

st.markdown("""
### 📊 안내사항

본 서비스는 모든 가능한 조합(814만 개)을 전부 탐색하여,
패턴과 통계 기준으로 점수를 평가하고 상위 5개 조합을 추천합니다.

모든 번호는 참고용이며, 실제 당첨을 보장하지 않습니다.

번호 선택 및 구매는 전적으로 개인의 판단과 책임입니다.
""")

# 👉 한자릿수 포함 여부 옵션 추가
include_single_digits = st.checkbox("한자릿수 번호 포함하기", value=True)

def score_combination(numbers):
    score = 0

    # 구간 점수 (1~15, 16~30, 31~45)
    g1 = any(1 <= n <= 15 for n in numbers)
    g2 = any(16 <= n <= 30 for n in numbers)
    g3 = any(31 <= n <= 45 for n in numbers)

    # 각 구간 가점 방식으로 변경
    if g1:
        score += 10
    if g2:
        score += 5
    if g3:
        score += 5

    # 한자릿수 포함 여부 체크
    if include_single_digits and not any(n <= 9 for n in numbers):
        return -1

    # 합계 점수 (기준값 138 → 범위 확대)
    total = sum(numbers)
    if not (80 <= total <= 180):
        return -1
    score += max(0, 30 - abs(138 - total))

    # 표준편차 점수
    std = np.std(numbers)
    if 6 <= std <= 16:
        score += 20
    else:
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
    if max_consecutive < 3:
        score += 20
    else:
        return -1

    # 홀짝 점수
    odds = len([n for n in numbers if n % 2 == 1])
    if odds in [3, 4]:
        score += 10
    else:
        return -1

    # 고저 번호 (저번호: 1~22)
    lows = len([n for n in numbers if n <= 22])
    if lows in [2, 3, 4]:
        score += 10
    else:
        return -1

    return score

if st.button("추천 번호 탐색 시작"):
    with st.spinner("모든 조합을 탐색 중... (수 분 소요됩니다)"):
        start_time = time.time()

        best_combinations = []
        count = 0
        progress_text = st.empty()

        for comb in combinations(range(1, 46), 6):
            count += 1
            score = score_combination(comb)
            if score > 0:
                best_combinations.append((list(comb), score, sum(comb), np.std(comb)))

            if count % 500000 == 0:
                progress_text.info(f"진행 중... {count:,}개 평가 완료")

        # 점수, 합계, 표준편차 기준 정렬
        best_combinations.sort(key=lambda x: (-x[1], x[2], x[3]))

        today = datetime.date.today()
        random.seed(today.isocalendar()[1])

        top_candidates = best_combinations[:100]
        random.shuffle(top_candidates)

        selected = []
        used_sets = set()

        for combo_info in top_candidates:
            num_set = frozenset(combo_info[0])
            if num_set not in used_sets:
                selected.append(combo_info)
                used_sets.add(num_set)
            if len(selected) >= 5:
                break

        end_time = time.time()
        st.success(f"완전 탐색 완료! (총 소요 시간: {round(end_time - start_time, 2)}초)")

        for idx, (nums, score, total, std) in enumerate(selected, start=1):
            st.write(f"추천 조합 {idx}: {nums} / 종합 점수: {score} / 합계: {total} / 표준편차: {round(std, 2)}")


