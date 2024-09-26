import json
import time
from datetime import datetime

serviceKey = "Z0JXdBE%2Fev7ojVtIqRLe0IwBCtNVMWSqysA0DLbPlI9NYSNnYJrRWUbWPciZpDqhiWVdF9VQqJGFI2LxP46d4Q%3D%3D" # 본인의 서비스 키 입력
# --> 날씨를 알고 싶은 시간 입력
base_date = datetime.now().strftime("%Y%m%d")
base_time = '0830' # 발표 시간
nx = '101' # 예보 지점 x좌표
ny = '84' # 예보 지점 y좌표

# url
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={serviceKey}&numOfRows=60&pageNo=1&dataType=json&base_date={base_date}&base_time=0830&nx=101&ny=84"

# url로 API return값 요청
import requests
response = requests.get(url, verify=False)
print(response.text)
#RN1 강수량24
#T1H 온도12

