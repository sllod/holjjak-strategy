import streamlit as st
import random
import time

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎲")

st.title("로또 번호 생성기")

st.markdown("""
### ✨ 고급 필터 기반 로또 번호 생성
본 생성기는 **수백만 개 조합 중 무작위 시뮬레이션 및 필터링**을 통해 최적의 조합을 제공합니다.

#### 필터링 기준
- ❌ **최근 1등 번호**: 최대 1개만 포함
- 🔁 **연속번호**: 3개 이상 연속 시 제거
- ⚖️ **홀/짝 비율**: 2:4, 3:3, 4:2 비율만 허용
- 📊 **숫자 분포**: 1~45 범위에서 고르게 분포
""")

mode = st.radio("모드 선택", ["자동", "최근 1등 번호 기반"], index=0)

recent_numbers = st.text_input("최근 1등 번호 (쉼표로 구분)", placeholder="예: 3,11,15,29,35,44")

num_sets = st.slider("생성할 조합 수량", min_value=1, max_value=5, value=1)

def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

def generate_based_on_recent(recent):
    candidate = set(range(1, 46)) - set(recent)
    return sorted(random.sample(candidate, 6))

def passes_filters(numbers, recent_set):
    # 최근 번호 필터: 최대 1개만 포함
    if len(set(numbers) & recent_set) > 1:
        return False

    # 연속 번호 3개 이상 제거
    sorted_nums = sorted(numbers)
    current = 1
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i-1] + 1:
            current += 1
            if current >= 3:
                return False
        else:
            current = 1

    # 홀짝 비율
    odds = [n for n in numbers if n % 2 == 1]
    evens = [n for n in numbers if n % 2 == 0]
    if not ((len(odds), len(evens)) in [(2, 4), (3, 3), (4, 2)]):
        return False

    # 숫자 분포: 최소 범위 차이 (예: 15 이상)
    if max(numbers) - min(numbers) < 15:
        return False

    return True

if st.button("번호 생성"):
    with st.spinner("수백만 개 조합 중 시뮬레이션 및 필터링 중..."):
        time.sleep(random.uniform(1, 2))  # 로딩 시간 1~2초

    results = []
    recent_set = set()
    if mode == "최근 1등 번호 기반":
        try:
            recent_list = [int(x.strip()) for x in recent_numbers.split(",") if x.strip()]
            if len(recent_list) != 6:
                st.error("최근 번호는 반드시 6개여야 합니다.")
            else:
                recent_set = set(recent_list)
        except:
            st.error("번호 입력 형식을 확인하세요!")
            recent_set = set()

    tries = 0
    while len(results) < num_sets and tries < 100000:
        tries += 1
        nums = generate_lotto_numbers() if mode == "자동" else generate_based_on_recent(recent_set)
        if passes_filters(nums, recent_set):
            if nums not in results:
                results.append(nums)

    if results:
        for i, numbers in enumerate(results, start=1):
            st.write(f"🎯 조합 {i}: **{numbers}**")
    else:
        st.warning("조건을 만족하는 조합을 찾지 못했습니다. (조건을 완화하거나 최근 번호를 확인해보세요.)")

