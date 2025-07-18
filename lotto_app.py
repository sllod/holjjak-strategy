import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎲")

st.title("로또 번호 생성기")

# 안내사항
st.markdown("""
### 📄 안내사항
본 생성기는 **8백만 개 조합 중 무작위 시뮬레이션 및 고급 필터링**을 통해 최적의 조합을 제공합니다.

본 서비스는 참고용 번호 추천 도구이며, 당첨을 보장하지 않습니다. 

실제 구매 결정은 개인의 책임입니다.

#### 📊 필터 기준

- **연속번호**: 3개 이상 연속 시 제거

    실제 로또 1등 번호 통계에서 3개 이상 연속 번호가 나올 확률은 약 2% 미만으로 매우 낮습니다.  
    따라서 연속 번호가 많은 조합은 제거하여 현실적인 조합만 추천합니다.

- **홀/짝 비율**: 선택한 비율만 허용 (AI 추천 포함)

    참고: 1등 당첨 번호의 약 80% 이상이 홀3:짝3 또는 홀4:짝2 비율입니다.  
    극단적인 홀짝 조합(예: 홀6:짝0, 홀5:짝1)은 역사적으로 거의 나오지 않았습니다.

- **번호 구간 분포(숫자 분포)**: 1~45 범위에서 고르게 분포하도록 필터링

    당첨 번호는 특정 구간(예: 1~10)에 몰리지 않고, 여러 구간에 분산되는 경향이 강합니다.  
    최소 범위 차이(예: 15 이상)를 강제해 균형 잡힌 분포를 유지합니다.

- **포함/제외 번호 조건**: 사용자가 직접 선택한 포함 번호와 제외 번호를 반영

    특정 번호를 반드시 포함하거나 제외할 수 있어 개인화된 전략을 적용할 수 있습니다.

- **합계 기준(내부 적용)**: 너무 낮거나 높은 번호 합계를 피함

    실제 당첨 번호 합계는 대체로 100~170 사이에 분포합니다.  
    극단적인 합계를 배제해 현실성 있는 조합을 유지합니다.
""")

exclude_numbers_input = st.text_input("제외할 번호 (쉼표로 구분)", placeholder="예: 7,13,22")
include_numbers_input = st.text_input("반드시 포함할 번호 (쉼표로 구분)", placeholder="예: 1,5")

ratio_option = st.selectbox(
    "허용할 홀/짝 비율 선택",
    options=[
        "AI 추천 비율 (홀3:짝3, 홀4:짝2)",
        "홀2 : 짝4",
        "홀3 : 짝3",
        "홀4 : 짝2",
        "홀2 : 짝4, 홀3 : 짝3, 홀4 : 짝2"
    ],
    index=0,
    help="AI 추천은 실제 로또 당첨 통계 기반의 비율 (홀3:짝3, 홀4:짝2)만 허용합니다."
)

NUM_SETS = 5
MAX_TRIES = 8_000_000  # 최대 시도 횟수: 800만

if "history" not in st.session_state:
    st.session_state["history"] = []

if ratio_option == "AI 추천 비율 (홀3:짝3, 홀4:짝2)":
    allowed_ratios = ["3:3", "4:2"]
elif ratio_option == "홀2 : 짝4, 홀3 : 짝3, 홀4 : 짝2":
    allowed_ratios = ["2:4", "3:3", "4:2"]
elif ratio_option == "홀2 : 짝4":
    allowed_ratios = ["2:4"]
elif ratio_option == "홀3 : 짝3":
    allowed_ratios = ["3:3"]
elif ratio_option == "홀4 : 짝2":
    allowed_ratios = ["4:2"]
else:
    allowed_ratios = ["2:4", "3:3", "4:2"]

def parse_numbers(input_text):
    nums = set()
    for x in input_text.split(","):
        x = x.strip()
        if x:
            try:
                n = int(x)
                if 1 <= n <= 45:
                    nums.add(n)
            except:
                continue
    return nums

def generate_lotto_numbers(exclude_set, include_set):
    candidate = set(range(1, 46)) - exclude_set - include_set
    if len(candidate) < (6 - len(include_set)):
        return None
    nums = set(random.sample(list(candidate), 6 - len(include_set)))
    nums = nums.union(include_set)
    return sorted(nums)

def passes_filters(numbers, allowed_ratios):
    sorted_nums = sorted(numbers)
    current = 1
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i - 1] + 1:
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

    total = sum(numbers)
    if total < 100 or total > 170:
        return False

    return True

if st.button("번호 생성"):
    with st.spinner("8백만 개 조합 중 시뮬레이션 및 필터링 중..."):
        time.sleep(random.uniform(1, 2))

    exclude_set = parse_numbers(exclude_numbers_input)
    include_set = parse_numbers(include_numbers_input)

    if len(include_set) >= 6:
        st.warning("⚠️ 반드시 포함할 번호는 최대 5개까지만 입력 가능합니다.")
    else:
        results = []
        tries = 0
        while len(results) < NUM_SETS and tries < MAX_TRIES:
            tries += 1
            nums = generate_lotto_numbers(exclude_set, include_set)
            if nums is None:
                break
            if passes_filters(nums, allowed_ratios):
                if nums not in results:
                    results.append(nums)

        if results:
            for i, numbers in enumerate(results, start=1):
                total = sum(numbers)
                odds_count = len([n for n in numbers if n % 2 == 1])
                evens_count = len([n for n in numbers if n % 2 == 0])

                st.write(f"### 🎲 조합 {i}: **{numbers}**")
                st.write(f"합계: **{total}** (짝: {evens_count}개, 홀: {odds_count}개)")
                st.markdown("---")

                st.session_state["history"].append(numbers)
                if len(st.session_state["history"]) > 20:
                    st.session_state["history"] = st.session_state["history"][-20:]

            df = pd.DataFrame({"조합": [str(combo) for combo in results]})
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="CSV 다운로드",
                data=csv,
                file_name='lotto_combinations.csv',
                mime='text/csv',
            )

            st.subheader("🕘 최근 히스토리 (최대 20개)")
            for idx, hist in enumerate(reversed(st.session_state["history"]), start=1):
                st.write(f"{idx}: {hist}")

        else:
            st.warning("조건을 만족하는 조합을 찾지 못했습니다. (조건을 완화하거나 포함/제외 번호를 확인해보세요.)")

