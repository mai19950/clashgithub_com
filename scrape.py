import aiohttp
import asyncio
import aiofiles
import os
from datetime import datetime, timedelta

# 从环境变量中获取 Telegram Bot Token 和 Chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
  raise ValueError("TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 环境变量未设置")


async def scrape():
  # 获取当天日期，格式为 YYYYMMDD
  today = datetime.today().strftime('%Y%m%d')

  # 动态生成 URL，替换日期部分
  url = f'https://clashgithub.com/wp-content/uploads/rss/{today}.txt'

  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      if response.status == 200:
        content = await response.text()
        async with aiofiles.open('site', 'w', encoding="utf-8") as file:
          await file.write(content)
        print("节点已成功保存")
        return True
      else:
        print(f"无法获取内容，状态码：{response.status}")
        return False


async def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'  # 使 Telegram 解析 Markdown 格式
  }
  async with aiohttp.ClientSession() as session:
    async with session.post(url, json=payload) as response:
      if response.status == 200:
        print("Message sent successfully!")
      else:
        print(f"Failed to send message. Error: {response.status}, {await response.text()}")


async def main():
  scrape_success = await scrape()
  
  if scrape_success:
    # 获取当前时间
    current_time = datetime.now()
    # 北京时间是 UTC+8，所以加上8小时
    beijing_time = current_time + timedelta(hours=8)
    current_datetime = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    message = (
      f"更新成功\n"
      f"Time: {current_datetime}\n"
      f"origin: clashgithub.com\n"
      f"订阅地址: `https://raw.githubusercontent.com/mai19950/clashgithub_com/main/site`"
    )
    await send_telegram_message(message)


if __name__ == '__main__':
  asyncio.run(main())
