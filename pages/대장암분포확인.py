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
