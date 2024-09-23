import requests
from datetime import datetime

# 获取当天日期，格式为 YYYYMMDD
today = datetime.today().strftime('%Y%m%d')

# 动态生成 URL，替换日期部分
url = f'https://clashgithub.com/wp-content/uploads/rss/{today}.txt'

# 发送 GET 请求获取内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
  content = response.text
  
  # 保存爬取到的内容
  with open('site', 'w', encoding='utf-8') as file:
    file.write(content)
    
  print("内容已成功保存")
else:
  print(f"无法获取内容，状态码: {response.status_code}")
