import streamlit as st
import pandas as pd
import koreanize_matplotlib  # 한글 폰트 지원
import matplotlib.pyplot as plt

# 데이터 경로
DATA_PATH = "colon cancer"

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(path):
    try:
        # 데이터 로드
        data = pd.read_csv(path)
        return data
    except Exception as e:
        st.error(f"데이터를 로드하는 데 문제가 발생했습니다: {e}")
        return None

# 데이터 로드
data = load_data(DATA_PATH)

if data is not None:
    st.title("대장암 수진율 분석")
    st.write("2010년, 2012년, 2014년 데이터를 기반으로 교육수준, 직업, 지역별로 대장암 수진율 평균을 비교합니다.")

    # 연도 선택
    selected_years = [2010, 2012, 2014]
    filtered_data = data[data["year"].isin(selected_years)]

    # 교육수준별 수진율 비교
    st.subheader("교육수준별 대장암 수진율 평균")
    education_mean = (
        filtered_data.groupby(["education_level", "year"])["screening_rate"].mean().reset_index()
    )
    st.write(education_mean)
    fig, ax = plt.subplots(figsize=(10, 6))
    for level in education_mean["education_level"].unique():
        subset = education_mean[education_mean["education_level"] == level]
        ax.plot(
            subset["year"],
            subset["screening_rate"],
            marker="o",
            label=f"교육수준: {level}",
        )
    ax.set_title("교육수준별 대장암 수진율 평균 변화")
    ax.set_xlabel("연도")
    ax.set_ylabel("수진율 평균")
    ax.legend()
    st.pyplot(fig)

    # 직업별 수진율 비교
    st.subheader("직업별 대장암 수진율 평균")
    occupation_mean = (
        filtered_data.groupby(["occupation", "year"])["screening_rate"].mean().reset_index()
    )
    st.write(occupation_mean)
    fig, ax = plt.subplots(figsize=(10, 6))
    for job in occupation_mean["occupation"].unique():
        subset = occupation_mean[occupation_mean["occupation"] == job]
        ax.plot(
            subset["year"],
            subset["screening_rate"],
            marker="o",
            label=f"직업: {job}",
        )
    ax.set_title("직업별 대장암 수진율 평균 변화")
    ax.set_xlabel("연도")
    ax.set_ylabel("수진율 평균")
    ax.legend()
    st.pyplot(fig)

    # 지역별 수진율 비교
    st.subheader("지역별 대장암 수진율 평균")
    region_mean = (
        filtered_data.groupby(["region", "year"])["screening_rate"].mean().reset_index()
    )
    st.write(region_mean)
    fig, ax = plt.subplots(figsize=(10, 6))
    for region in region_mean["region"].unique():
        subset = region_mean[region_mean["region"] == region]
        ax.plot(
            subset["year"],
            subset["screening_rate"],
            marker="o",
            label=f"지역: {region}",
        )
    ax.set_title("지역별 대장암 수진율 평균 변화")
    ax.set_xlabel("연도")
    ax.set_ylabel("수진율 평균")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("데이터를 로드할 수 없습니다. 데이터 경로를 확인해주세요.")
