import os
import requests
from datetime import datetime

def scrapy():
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


def tg_notify():
  # 从环境变量获取 Telegram Bot Token 和 Chat ID
  telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
  telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

  # 生成要发送的消息
  current_date = datetime.now().strftime('%Y-%m-%d')
  message = f"Scraping completed successfully on {current_date}"

  # Telegram API URL
  telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

  # 请求参数
  payload = {
      'chat_id': telegram_chat_id,
      'text': message
  }
  # 发送 POST 请求到 Telegram API
  response = requests.post(telegram_url, data=payload)

  # 检查请求是否成功
  if response.status_code == 200:
    print("Message sent successfully!")
  else:
    print(f"Failed to send message. Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
  scrapy()
  tg_notify()
