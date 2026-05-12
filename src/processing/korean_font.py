# 폰트 강제 지정
import matplotlib as mpl 
mpl.rc('font', family='Malgun Gothic')      # 한글 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지