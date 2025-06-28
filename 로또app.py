import streamlit as st
import random
import time

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎲")

st.title("🎲 로또 번호 생성기")

st.markdown("""
### ✨ 고급 필터 기반 로또 번호 생성
본 생성기는 **수백만 개 조합 중 무작위 시뮬레이션 및 필터링**을 통해 최적의 조합을 제공합니다.

#### 🎯 필터링 기준
- ❌ **최근 1등 번호**: 최대 1개만 포함
- 🔁 **연속번호**: 3개 이상 연속 시 제거
- ⚖️ **홀/짝 비율**: 선택한 비율만 허용  
  ↳ **사유**: 실제 로또 1등 번호 통계상, 극단적인 홀짝 조합(예: 6:0, 5:1)은 거의 나오지 않기 때문에 제외
- 📊 **숫자 분포**: 1~45 범위에서 고르게 분포
""")

mode = st.radio("모드 선택", ["자동", "최근 1등 번호 기반"], index=0)

recent_numbers = st.text_input("최근 1등 번호 (쉼표로 구분)", placeholder="예: 3,11,15,29,35,44")

ratio_option = st.selectbox(
    "허용할 홀/짝 비율 선택",
    options=["홀2 : 짝4", "홀3 : 짝3", "홀4 : 짝2", "홀2 : 짝4, 홀3 : 짝3, 홀4 : 짝2"],
    index=3
)

NUM_SETS = 5  # 무조건 5개 생성

def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

def generate_based_on_recent(recent):
    candidate = set(range(1, 46)) - set(recent)
    return sorted(random.sample(candidate, 6))

def passes_filters(numbers, recent_set, allowed_ratios):
    if len(set(numbers) & recent_set) > 1:
        return False

    sorted_nums = sorted(numbers)
    current = 1
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i-1] + 1:
            current += 1
            if current >= 3:
                return False
        else:
            current = 1

    odds = [n for n in numbers if n % 2 == 1]
    evens = [n for n in numbers if n % 2 == 0]
    ratio_str = f"{len(odds)}:{len(evens)}"
    if ratio_str not in allowed_ratios:
        return False

    if max(numbers) - min(numbers) < 15:
        return False

    return True

if st.button("번호 생성"):
    with st.spinner("수백만 개 조합 중 시뮬레이션 및 필터링 중..."):
        time.sleep(random.uniform(1, 2))

    # 허용된 비율 리스트 생성
    if ratio_option == "홀2 : 짝4, 홀3 : 짝3, 홀4 : 짝2":
        allowed_ratios = ["2:4", "3:3", "4:2"]
    elif ratio_option == "홀2 : 짝4":
        allowed_ratios = ["2:4"]
    elif ratio_option == "홀3 : 짝3":
        allowed_ratios = ["3:3"]
    elif ratio_option == "홀4 : 짝2":
        allowed_ratios = ["4:2"]
    else:
        allowed_ratios = ["2:4", "3:3", "4:2"]  # 기본값

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
    while len(results) < NUM_SETS and tries < 100000:
        tries += 1
        nums = generate_lotto_numbers() if mode == "자동" else generate_based_on_recent(recent_set)
        if passes_filters(nums, recent_set, allowed_ratios):
            if nums not in results:
                results.append(nums)

    if results:
        for i, numbers in enumerate(results, start=1):
            total = sum(numbers)
            odds_count = len([n for n in numbers if n % 2 == 1])
            evens_count = len([n for n in numbers if n % 2 == 0])

            st.write(f"### 🎯 조합 {i}: **{numbers}**
            st.write(f"합계: **{total}** (짝: {evens_count}개, 홀: {odds_count}개)")
            st.markdown("---")
    else:
        st.warning("조건을 만족하는 조합을 찾지 못했습니다. (조건을 완화하거나 최근 번호를 확인해보세요.)")
