import datetime
import os
import requests
from openai import OpenAI

# 讀取 GitHub Secret
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def generate_ai_content():
    try:
        # 初始化阿里雲百煉 Client（相容 OpenAI 規格）
        client = OpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        today_str = datetime.date.today().strftime("%Y-%m-%d")

        prompt = f"""
        請扮演一位對香港年輕人社群與本地 YouTube 圈子極度熟悉敏銳的潮流小編。
        整理過去一天 18-35 歲香港年輕人熱門討論的流行話題、網路熱門迷因與流行趨勢（LIHKG、Dcard、Threads、TikTok、Instagram），以及香港頭 30 位娛樂與資訊類 YouTuber 的最新影片主題與熱議話題。

        請嚴格按照以下 Markdown 格式輸出，直接輸出報告內文，不要有任何額外開場白：

        🔥 **【{today_str} 香港 Top 30 YouTuber 焦點 & 年輕人社群趨勢日報】**

        🎥 **今日香港 Top 30 娛樂與資訊類 YouTuber 最新影片與熱議主題**
        1. **[YouTuber 名稱 / 頻道]**：[最新影片亮點、企劃內容與網民反應]
        2. **[YouTuber 名稱 / 創作者動態]**：[熱門話題、合作企劃或討論爆點]

        💬 **今日 18-35 歲年輕人社群（LIHKG、Dcard、Threads、IG）熱門話題與迷因**
        3. **[話題 / 流行語]**：[簡短介紹爆紅原因]
        4. **[話題 / 迷因趨勢]**：[簡短介紹梗圖或最新短影音風潮]

        💡 *小編總結/抽水/使用建議*
        """

        print("🤖 正在呼叫阿里雲通義千問 API...")
        response = client.chat.completions.create(
            model="qwen-plus",  # 可選: qwen-plus, qwen-max, qwen-turbo
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ 阿里雲 API 錯誤: {e}")
        return None


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        if res.json().get("ok"):
            print("✅ 成功發送到 Telegram！")
        else:
            print(f"❌ Telegram 發送失敗: {res.json()}")
    except Exception as e:
        print(f"💥 發送錯誤: {e}")


if __name__ == "__main__":
    msg = generate_ai_content()
    if msg:
        send_telegram_message(msg)
