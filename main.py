# app.py (Step 1 초안)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="화장품 성분 분석기", page_icon="🧴", layout="wide")

st.title("🧴 화장품 성분 규제 상태 분석기")
st.subheader("1단계: 기초 데이터 개요 (`ingredients.csv`)")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_base_data():
    try:
        df = pd.read_csv("ingredients.csv", sep="|")
        return df
    except FileNotFoundError:
        return None

df_ing = load_base_data()

if df_ing is not None:
    # 핵심 지표 카드 (KPI)
    total_rows, total_cols = df_ing.shape
    c1, c2, c3 = st.columns(3)
    c1.metric("전체 성분 수 (Rows)", f"{total_rows:,}개")
    c2.metric("성분 속성 수 (Columns)", f"{total_cols}개")
    c3.metric("코싱 매칭 완료 성분", f"{(df_ing['cosing_matched'] == 1).sum():,}개")

    st.markdown("---")
    
    # 데이터 미리보기
    st.markdown("### 📋 성분 데이터 원본 미리보기")
    st.dataframe(df_ing.head(10), use_container_width=True)

    # 결측치 요약 정보
    st.markdown("### 🔍 열별 결측치(Null) 현황")
    null_df = pd.DataFrame({
        "결측치 수": df_ing.isnull().sum(),
        "결측치 비율 (%)": (df_ing.isnull().mean() * 100).round(2)
    })
    st.dataframe(null_df[null_df["결측치 수"] > 0], use_container_width=True)

else:
    st.error("⚠️ 'ingredients.csv' 파일을 찾을 수 없습니다. 같은 폴더에 파일을 위치시켜 주세요.")
