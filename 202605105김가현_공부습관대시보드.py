import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 윈도우 기본 한글 폰트 설정 (맑은 고딕)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 2. 웹 앱 제목과 설명 표시
st.title("📚 공부 습관 분석 대시보드")
st.write("study.csv 데이터를 기반으로 요약 통계와 상관계수, 그리고 그래프를 확인하는 대시보드입니다.")

# 3. CSV 파일 읽기 (캐시 적용)
@st.cache_data
def load_data():
    return pd.read_csv('study.csv')

df = load_data()

# 4. 요약 통계 및 상관계수 출력 영역
st.subheader("📊 데이터 요약 통계")
st.write(df.describe())

# 상관계수 계산
corr_study_score = df['공부시간'].corr(df['점수'])
corr_phone_score = df['스마트폰'].corr(df['점수'])
corr_phone_study = df['스마트폰'].corr(df['공부시간'])

st.subheader("📈 상관계수 분석")
st.write(f"- **공부시간과 점수 상관계수:** {corr_study_score:.3f}")
st.write(f"- **스마트폰 사용시간과 점수 상관계수:** {corr_phone_score:.3f}")
st.write(f"- **스마트폰 사용시간과 공부시간 상관계수:** {corr_phone_study:.3f}")

st.markdown("---")

# 5. 맷플롯립 그래프 그리기 (서브플롯 + 추세선)
st.subheader("📉 공부 습관에 따른 점수 관계 (추세선 포함)")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 왼쪽 그래프: 공부시간 vs 점수 + 추세선
axes[0].scatter(df['공부시간'], df['점수'], color='royalblue', alpha=0.7, label='학생')
m1, b1 = np.polyfit(df['공부시간'], df['점수'], 1)
axes[0].plot(df['공부시간'], m1 * df['공부시간'] + b1, color='red', linestyle='--', label='추세선')
axes[0].set_title('공부시간과 점수의 관계')
axes[0].set_xlabel('공부시간 (시간)')
axes[0].set_ylabel('점수 (점)')
axes[0].legend()
axes[0].grid(True, linestyle=':', alpha=0.6)

# 오른쪽 그래프: 스마트폰사용시간 vs 점수 + 추세선
axes[1].scatter(df['스마트폰'], df['점수'], color='forestgreen', alpha=0.7, label='학생')
m2, b2 = np.polyfit(df['스마트폰'], df['점수'], 1)
axes[1].plot(df['스마트폰'], m2 * df['스마트폰'] + b2, color='orange', linestyle='--', label='추세선')
axes[1].set_title('스마트폰 사용시간과 점수의 관계')
axes[1].set_xlabel('스마트폰 사용시간 (시간)')
axes[1].set_ylabel('점수 (점)')
axes[1].legend()
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

# 6. Streamlit에 맷플롯립 그래프 출력 (plt.show() 대신 st.pyplot사용)
st.pyplot(fig)