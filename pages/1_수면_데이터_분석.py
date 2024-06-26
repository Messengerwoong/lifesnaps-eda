# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import seaborn as sns
from datetime import * 
from functools import reduce
import matplotlib.pyplot as plt
import streamlit as st
from 데이터_수집 import daily_sema

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# 필요한 컬럼 선택
df_subset = daily_sema[['id', 'sleep_duration', 'sleep_efficiency', 'sleep_points_percentage', 'sleep_deep_ratio', 'sleep_wake_ratio',
                        'sleep_light_ratio', 'sleep_rem_ratio']]

# 결측값 제거
df_subset = df_subset.dropna(subset=['sleep_duration'])

# 밀리초를 시간으로 변환하는 함수
def milliseconds_to_hours(milliseconds):
    hours = milliseconds / (1000 * 60 * 60)
    return hours

# 'sleep_duration' 컬럼의 값을 변환하여 새로운 컬럼에 저장
df_subset['sleep_duration_hours'] = df_subset['sleep_duration'].apply(milliseconds_to_hours)

# sleep_points_percentage 값을 100배하여 퍼센트로 표시
df_subset['sleep_points_percentage'] = df_subset['sleep_points_percentage'] * 100

# ID 별로 그룹화하여 평균값 계산
grouped_mean = df_subset.groupby('id').mean()

st.markdown(
    "<h1 style='text-align: center;'>Kaggle Fitbit Sleep EDA Project</h1><br><br>", 
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center;'>수면 데이터 분석</h2>", 
    unsafe_allow_html=True
)

st.markdown(
    "<h3>ID별 수면 평균 시간 통계치</h3>", 
    unsafe_allow_html=True
)

@st.cache_resource
def plot_graph(_x_data, y_data, title='그래프 제목', xlabel='X 축', ylabel='Y 축'):
    plt.figure(figsize=(10, 5))
    plt.plot(_x_data, y_data, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    
    # BytesIO 객체 생성
    plot_image = io.BytesIO()
    
    # 그래프를 이미지 파일로 저장
    plt.savefig(plot_image, format='png')
    
    # BytesIO 객체의 파일 포인터를 처음으로 되돌림
    plot_image.seek(0)
    
    # BytesIO 객체의 내용 반환
    return plot_image.getvalue()

# 그래프를 플로팅
plot_image = plot_graph(grouped_mean.index, grouped_mean['sleep_duration_hours'], title='Average Sleep Duration by ID', xlabel='ID', ylabel='Average Sleep Duration (hours)')

# Streamlit에 그래프를 표시
st.image(plot_image, use_column_width=True)


st.markdown("""**ID 별로 그룹화하여 평균 수면 시간 시각화**  
            → 대체적으로 **6~8시간**이 제일 많으며 몇몇 ID에서 **이상치**가 발견됨   
            → 이상치가 보인 ID(16, 39, 41, 49, 68, 69)는 **데이터 집계 10개 미만**으로 나옴""")

st.markdown(
    "<h2>평균 수면 시간별 수면 단계 비율성 비교</h2>", 
    unsafe_allow_html=True
)

# 수면 평균 시간과 각 수면 단계의 비율 추출
sleep_duration = grouped_mean['sleep_duration_hours']
deep_sleep_ratio = grouped_mean['sleep_deep_ratio']
light_sleep_ratio = grouped_mean['sleep_light_ratio']
rem_sleep_ratio = grouped_mean['sleep_rem_ratio']
wake_sleep_ratio = grouped_mean['sleep_wake_ratio']

@st.cache_resource
def plot_scatter(sleep_duration, deep_sleep_ratio, light_sleep_ratio, rem_sleep_ratio, wake_sleep_ratio):
    plt.figure(figsize=(12, 10))

    # 깊은 잠의 비율
    plt.subplot(2, 2, 1)
    plt.scatter(sleep_duration, deep_sleep_ratio, alpha=0.5)
    plt.title('Average Sleep Duration vs. Deep Sleep Ratio')
    plt.xlabel('Average Sleep Duration (hours)')
    plt.ylabel('Deep Sleep Ratio')
    plt.xlim(5, 10)
    plt.ylim(0.85, 1.25)
    plt.grid(True)

    # 얕은 잠의 비율
    plt.subplot(2, 2, 2)
    plt.scatter(sleep_duration, light_sleep_ratio, alpha=0.5)
    plt.title('Average Sleep Duration vs. Light Sleep Ratio')
    plt.xlabel('Average Light Duration (hours)')
    plt.ylabel('Light Sleep Ratio')
    plt.xlim(5, 10)
    plt.ylim(0.85, 1.25)
    plt.grid(True)

    # 렘수면의 비율
    plt.subplot(2, 2, 3)
    plt.scatter(sleep_duration, rem_sleep_ratio, alpha=0.5)
    plt.title('Average Sleep Duration vs. REM Sleep Ratio')
    plt.xlabel('Average Sleep Duration (hours)')
    plt.ylabel('REM Sleep Ratio')
    plt.xlim(5, 10)
    plt.ylim(0.85, 1.25)
    plt.grid(True)

    # 수면 뒤척임 비율
    plt.subplot(2, 2, 4)
    plt.scatter(sleep_duration, wake_sleep_ratio, alpha=0.5)
    plt.title('Average Sleep Duration vs. Wake Sleep Ratio')
    plt.xlabel('Average Sleep Duration (hours)')
    plt.ylabel('Wake Sleep Ratio')
    plt.xlim(5, 10)
    plt.ylim(0.85, 1.25)
    plt.grid(True)

    plt.tight_layout()
    
    # BytesIO 객체 생성
    plot_image = io.BytesIO()
    
    # 그래프를 이미지 파일로 저장
    plt.savefig(plot_image, format='png')
    
    # BytesIO 객체의 파일 포인터를 처음으로 되돌림
    plot_image.seek(0)
    
    # BytesIO 객체의 내용 반환
    return plot_image.getvalue()

# 그래프를 플로팅
scatter_plot_image = plot_scatter(sleep_duration, deep_sleep_ratio, light_sleep_ratio, rem_sleep_ratio, wake_sleep_ratio)

# Streamlit에 그래프를 표시
st.image(scatter_plot_image, use_column_width=True)

st.markdown("""**수면 평균 시간과 수면 단계 비율성 비교**    
            → 해당 분석에서는 **수면 단계를 4단계**로 나타냄(얕은 수면, 깊은 수면, 렘 수면, 뒤척임)  
            → 수면 시간이 **높을수록 모두 높음**    
            → 단계별 수면 비율 중 **렘 수면, 깊은 수면의 비율이 상대적으로 높음** BUT **수면 단계별 차이는 미미함**""")

st.markdown(
    "<h2>수면 평균 시간과 수면 효율성 비교</h2>", 
    unsafe_allow_html=True
)

@st.cache_resource
def plot_regression():
    plt.figure(figsize=(12, 10))

    # Sleep Duration vs. Sleep Efficiency
    plt.subplot(2, 2, 1)
    sns.regplot(data=grouped_mean, x='sleep_duration_hours', y='sleep_efficiency')
    plt.xlim(6, 10)
    plt.ylim(85, 100)
    plt.title('Sleep Duration vs. Sleep Efficiency (Regression Plot)')
    plt.xlabel('Sleep Duration (hours)')
    plt.ylabel('Sleep Efficiency')

    # Sleep Duration vs. Sleep Points Percentage
    plt.subplot(2, 2, 2)
    sns.regplot(data=grouped_mean, x='sleep_duration_hours', y='sleep_points_percentage')
    plt.xlim(6, 10)
    plt.title('Sleep Duration vs. Sleep Points Percentage (Regression Plot)')
    plt.xlabel('Sleep Duration (hours)')
    plt.ylabel('Sleep Points Percentage')

    # Sleep Efficiency vs. Sleep Points Percentage
    plt.subplot(2, 2, 3)
    sns.regplot(data=grouped_mean, x='sleep_efficiency', y='sleep_points_percentage')
    plt.xlim(90, 97)
    plt.title('Scatter Plot of Sleep Efficiency and Sleep Points Percentage')
    plt.xlabel('Sleep Efficiency')
    plt.ylabel('Sleep Points Percentage')

    plt.tight_layout()

    # BytesIO 객체 생성
    plot_image = io.BytesIO()
    
    # 그래프를 이미지 파일로 저장
    plt.savefig(plot_image, format='png')
    
    # BytesIO 객체의 파일 포인터를 처음으로 되돌림
    plot_image.seek(0)
    
    # BytesIO 객체의 내용 반환
    return plot_image.getvalue()

# 그래프를 플로팅
regression_plot_image = plot_regression()

# Streamlit에 그래프를 표시
st.image(regression_plot_image, use_column_width=True)

st.markdown("""**수면 시간과 수면 효율의 관계성 비교**   
            → 수면 시간은 **6~8시간**으로 분포함  
            → 수면 효율은 **90~98퍼센트**로 분포함  
            → **음의 상관성**을 보임 BUT 분포도로 봤을때 **6~8시간**에서 제일 **높은 수면 효율성**을 보임""")