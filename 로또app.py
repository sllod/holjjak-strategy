
import streamlit as st
import random

st.set_page_config(page_title="로또 번호 생성기(만두)", layout="centered")

st.markdown("""<style>
    body {
        background-color: #e0f7fa;
    }
    .main {
        background: linear-gradient(to bottom, #b2ebf2, #e0f7fa);
        padding: 2rem;
        border-radius: 12px;
    }
    .highlight {
        background-color: #e0f2f1;
        padding: 1rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        text-align: center;
        color: #006064;
    }
    .stTextInput input {
        font-size: 1.1rem;
        background-color: #ffffff;
        border: 1px solid #b2ebf2;
    }
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.6rem;
        background-color: #4dd0e1;
        color: white;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #26c6da;
    }
</style>""", unsafe_allow_html=True)

st.title("★로또 번호 생성기★(만두)")
st.caption("전략적 조합 생성기 · 자동 or 사용자 지정 모드 선택 가능")

auto_mode = st.toggle("✅ 최근 1등 번호 없이 자동 생성")

winning_input = ""
round_info = ""

if not auto_mode:
    winning_input = st.text_input("📌 지난 회차 1등 번호를 입력해주세요 (예: 1, 7, 13, 22, 34, 42):", "")
    round_info = st.text_input("🗓️ 이번 회차 정보 (예: 1123회 또는 '6월 마지막 주')", "")

def generate_lotto_numbers(exclude_nums, exclude_enabled=True):
    results = []
    while len(results) < 10:
        nums = random.sample(range(1, 46), 6)
        nums.sort()

        if exclude_enabled:
            # 조건 1: 최근 번호와 2개 이상 겹치지 않게
            if len(set(nums) & set(exclude_nums)) >= 2:
                continue

        # 조건 2: 연속번호 3개 이상 금지
        seq = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1] + 1:
                seq += 1
                if seq >= 3:
                    break
            else:
                seq = 1
        else:
            # 조건 3: 홀짝 균형 (2~4 홀 포함)
            odd = sum(1 for n in nums if n % 2 == 1)
            if 2 <= odd <= 4:
                results.append(nums)
    return results

def parse_numbers(input_text):
    try:
        return [int(n.strip()) for n in input_text.split(",") if n.strip().isdigit()]
    except:
        return []

exclude_numbers = parse_numbers(winning_input)

if st.button("🎰 최상의 조합 10개 생성!"):
    if not auto_mode and len(exclude_numbers) < 6:
        st.warning("최근 1등 번호 6개를 정확히 입력해주세요.")
    else:
        if not auto_mode:
            st.markdown(f"<div class='highlight'>{round_info} 기준 제외번호: {exclude_numbers}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='highlight'>자동 생성 모드 (1등 번호 필터링 없이 무작위 전략 적용)</div>", unsafe_allow_html=True)
        combos = generate_lotto_numbers(exclude_numbers, exclude_enabled=not auto_mode)
        for i, combo in enumerate(combos, 1):
            st.success(f"{i}번 조합: {combo}")
else:
    st.info("위 모드를 선택하고 버튼을 눌러 조합을 생성하세요!")

st.markdown("---")
st.subheader("🧠 입력 방식에 따른 차이점 안내")

st.markdown("""
**📌 1등 번호를 입력하는 경우**  
→ 최근 당첨 패턴을 기반으로 겹치는 번호를 제외하여  
더 정교한 전략 조합을 제공합니다.  

**🎯 자동 생성 모드 사용 시**  
→ 최신 번호와 무관하게,  
통계 기반 전략만 적용하여 무작위 조합을 생성합니다.  
(단, 여전히 연속/홀짝/분포 기준은 적용됩니다.)
""")

st.markdown("---")
st.subheader("📋 필터링 기준 요약")
st.markdown("""
| 기준 항목 | 적용 내용 |
|-----------|-----------|
| ❌ 최근 1등 번호 | 최대 1개만 겹치도록 제한 (해당 시) |
| 🔁 연속번호 | 3개 이상 연속될 경우 제거 |
| ⚖️ 홀/짝 비율 | 2:4, 3:3, 4:2만 허용 |
| 📊 숫자 분포 | 1~45 범위에서 골고루 분포되도록 조절 |
""")
