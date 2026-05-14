import pandas as pd
import matplotlib.pyplot as plt
import korean_font  # 한글 폰트 설정 모듈

# CSV 불러오기
df = pd.read_csv('data/반환상태크롤링.csv')

# 등록번호 존재 여부를 True/False로 변환
df['등록여부'] = df['등록번호'].notna()

# True/False 개수 세기
counts = df['등록여부'].value_counts()

# 원형 차트 그리기
plt.figure(figsize=(6,6))
counts.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    colors=['skyblue','salmon'],
    labels=['등록', '미등록']
)
plt.title("반환된 반려동물 중 등록/미등록 비율")
plt.ylabel("") 
plt.legend()
plt.show()
plt.savefig('./src/chart/save_chart1.png')
