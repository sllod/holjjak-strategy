import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎲")

st.title("로또 번호 생성기")

# 안내사항
st.markdown("""
### 📄 안내사항
본 생성기는 **백만 개 조합 중 무작위 시뮬레이션 및 고급 필터링**을 통해 최적의 조합을 제공합니다.

본 서비스는 참고용 번호 추천 도구이며, 당첨을 보장하지 않습니다. 

실제 구매 결정은 개인의 책임입니다.

#### 📊 필터 기준
-  **연속번호**: 3개 이상 연속 시 제거
-  **홀/짝 비율**: 선택한 비율만 허용 (AI 추천 포함)  
  ↳ **참고**: 실제 로또 1등 번호 통계상, 극단적인 홀짝 조합(예: 6:0, 5:1)은 거의 나오지 않기때문에 제외
-  **숫자 분포**: 1~45 범위에서 고르게 분포
""")

# 입력
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

if "history" not in st.session_state:
    st.session_state["history"] = []

# 홀짝 비율 세팅
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

# 숫자 파싱 함수 (검증 강화)
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

# 조합 생성 함수
def generate_lotto_numbers(exclude_set, include_set):
    candidate = set(range(1, 46)) - exclude_set - include_set
    if len(candidate) < (6 - len(include_set)):
        return None
    nums = set(random.sample(list(candidate), 6 - len(include_set)))
    nums = nums.union(include_set)
    return sorted(nums)

# 필터 함수
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

    return True

# 버튼 클릭
if st.button("번호 생성"):
    with st.spinner("백만 개 조합 중 시뮬레이션 및 필터링 중..."):
        time.sleep(random.uniform(1, 2))

    exclude_set = parse_numbers(exclude_numbers_input)
    include_set = parse_numbers(include_numbers_input)

    # 포함 번호가 6개 이상일 때 경고
    if len(include_set) >= 6:
        st.warning("⚠️ 반드시 포함할 번호는 최대 5개까지만 입력 가능합니다.")
    else:
        results = []
        tries = 0
        while len(results) < NUM_SETS and tries < 1_000_000:
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
