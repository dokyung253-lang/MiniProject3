# [*] 차트내 한글 깨짐 방지 코드    , 항상 사용하는 파일 상단에 복붙
import matplotlib as mpl
mpl.rc('font', family='Malgun Gothic') # 또는 'Noto Sans CJK JP'
mpl.rcParams['axes.unicode_minus'] = False