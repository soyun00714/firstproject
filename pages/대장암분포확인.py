import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 지원

# 데이터 로드 및 변환 함수
@st.cache_data
def load_and_transform_data():
    # 주어진 데이터를 DataFrame으로 생성 (예제 데이터)
    raw_data = {
        "year": ["2010", "2010", "2010", "2012", "2012", "2012", "2014", "2014", "2014"],
        "gender": ["total", "male", "female", "total", "male", "female", "total", "male", "female"],
        "50~64": [36.7, 41.1, 32.8, 46.5, 49.6, 43.7, 49.9, 53.4, 46.8],
        "65 이상": [28.9, 37.1, 22.3, 40.4, 46.6, 35.4, 47.2, 54.5, 41.2],
    }

    # 데이터프레임 생성
    df = pd.DataFrame(raw_data)

    # 데이터 변환: wide -> long
    df_long = pd.melt(
        df,
        id_vars=["year", "gender"],
        value_vars=["50~64", "65 이상"],
        var_name="age_group",
        value_name="screening_rate",
    )

    # total 삭제
    df_long = df_long[df_long["gender"] != "total"]

    # 나이대 이름을 변경 (추가적으로 명확히 표시)
    df_long["age_group"] = df_long["age_group"].replace({
        "50~64": "50-64세",
        "65 이상": "65세 이상"
    })

    return df_long

# 데이터 로드 및 변환
data = load_and_transform_data()

# Streamlit 앱
st.title("연도별 남녀 나이대별 대장암 수진율 평균 비교")
st.write("연도별, 성별, 나이대별 대장암 수진율 평균을 비교합니다.")

# 성별 및 연도별 평균 계산
gender_age_mean = data.groupby(["year", "gender", "age_group"])["screening_rate"].mean().reset_index()

# 데이터프레임 출력
st.write("연도별 남녀 나이대별 대장암 수진율 평균:")
st.dataframe(gender_age_mean)

# 그래프 출력
st.subheader("연도별 남녀 나이대별 대장암 수진율 평균 비교 그래프")
fig, ax = plt.subplots(figsize=(14, 8))  # 그래프 크기 조정

# 나이대별, 성별로 데이터 시각화
for age_group in gender_age_mean["age_group"].unique():
    for gender in gender_age_mean["gender"].unique():
        subset = gender_age_mean[(gender_age_mean["age_group"] == age_group) & (gender_age_mean["gender"] == gender)]
        ax.plot(
            subset["year"],
            subset["screening_rate"],
            marker="o",
            markersize=10,  # 점 크기 확대
            linewidth=2,  # 선 굵기 확대
            label=f"{age_group} - {gender}",
        )

# 그래프 설정
ax.set_title("연도별 남녀 나이대별 대장암 수진율 평균 비교", fontsize=20, weight='bold')
ax.set_xlabel("연도", fontsize=16, weight='bold')
ax.set_ylabel("수진율 평균 (%)", fontsize=16, weight='bold')
ax.tick_params(axis='both', which='major', labelsize=14)  # 축 눈금 크기 조정
ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1), title="나이대 - 성별", fontsize=12)  # 범례 크기 조정
plt.grid(True, linestyle='--', alpha=0.6)  # 격자 추가

# 그래프 출력
st.pyplot(fig)

import pandas as pd
from scipy.stats import f_oneway

# Define the raw data
raw_data = {
    "year": ["2010", "2010", "2010", "2012", "2012", "2012", "2014", "2014", "2014"],
    "gender": ["total", "male", "female", "total", "male", "female", "total", "male", "female"],
    "50~64": [36.7, 41.1, 32.8, 46.5, 49.6, 43.7, 49.9, 53.4, 46.8],
    "65 이상": [28.9, 37.1, 22.3, 40.4, 46.6, 35.4, 47.2, 54.5, 41.2],
}

# Create a DataFrame
df = pd.DataFrame(raw_data)

# Transform data to long format
df_long = pd.melt(
    df,
    id_vars=["year", "gender"],
    value_vars=["50~64", "65 이상"],
    var_name="age_group",
    value_name="screening_rate",
)

# Remove "total" from gender
df_long = df_long[df_long["gender"] != "total"]

# Rename age groups for clarity
df_long["age_group"] = df_long["age_group"].replace({"50~64": "50-64세", "65 이상": "65세 이상"})

# --- PART 1: Analyze differences between years ---
# Group data by year and extract screening rates for ANOVA
year_groups = [df_long[df_long["year"] == year]["screening_rate"] for year in df_long["year"].unique()]

# Perform ANOVA across years
anova_year_result = f_oneway(*year_groups)
print(f"ANOVA p-value for differences across years: {anova_year_result.pvalue}")

# --- PART 2: Analyze differences between the 4 groups within each year ---
group_results = {}
for year in df_long["year"].unique():
    group_50_64_male = df_long[(df_long["year"] == year) & (df_long["age_group"] == "50-64세") & (df_long["gender"] == "male")]["screening_rate"]
    group_50_64_female = df_long[(df_long["year"] == year) & (df_long["age_group"] == "50-64세") & (df_long["gender"] == "female")]["screening_rate"]
    group_65_male = df_long[(df_long["year"] == year) & (df_long["age_group"] == "65세 이상") & (df_long["gender"] == "male")]["screening_rate"]
    group_65_female = df_long[(df_long["year"] == year) & (df_long["age_group"] == "65세 이상") & (df_long["gender"] == "female")]["screening_rate"]
    
    # Perform ANOVA for the 4 groups within the year
    anova_group_result = f_oneway(group_50_64_male, group_50_64_female, group_65_male, group_65_female)
    group_results[year] = anova_group_result.pvalue

# Print group results
for year, pvalue in group_results.items():
    print(f"ANOVA p-value for 4 groups in year {year}: {pvalue}")

