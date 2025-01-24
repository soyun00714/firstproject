import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 지원

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
    st.title("연도별 남녀 대장암 수진율 평균 비교")
    st.write("남성과 여성의 연도별 대장암 수진율 평균을 비교합니다.")

    # 남성/여성별 평균 계산
    gender_mean = data.groupby(["year", "gender"])["screening_rate"].mean().reset_index()

    # 데이터프레임 표시
    st.write("연도별 남녀 대장암 수진율 평균:")
    st.dataframe(gender_mean)

    # 연도별 남성/여성 수진율 평균 비교 그래프
    st.subheader("연도별 남녀 대장암 수진율 평균 비교 그래프")
    fig, ax = plt.subplots(figsize=(10, 6))
    for gender in gender_mean["gender"].unique():
        subset = gender_mean[gender_mean["gender"] == gender]
        ax.plot(
            subset["year"],
            subset["screening_rate"],
            marker="o",
            label=f"성별: {gender}",
        )
    ax.set_title("연도별 남녀 대장암 수진율 평균 비교")
    ax.set_xlabel("연도")
    ax.set_ylabel("수진율 평균")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("데이터를 로드할 수 없습니다. 데이터 경로를 확인해주세요.")
