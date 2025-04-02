import requests
import csv
from bs4 import BeautifulSoup

# 取得網頁內容
url = 'https://rate.bot.com.tw/xrt'
response = requests.get(url, cookies={'over18': '1'})

# 確保請求成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有幣別與匯率資料
    rows = soup.find("table", class_="table").find("tbody").find_all("tr")

    # 準備寫入 CSV
    with open("api.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        csv_writer = csv.writer(csvfile)

        # 寫入標題列
        csv_writer.writerow(["幣別", "即期買入", "即期賣出"])

        # 提取並寫入數據
        for row in rows:
            currency_name = row.find("div", class_="visible-phone").get_text(strip=True)  # 幣別名稱
            rates = row.find_all("td", class_="rate-content-sight")  # 匯率 (即期買入 & 即期賣出)

            buy_rate = rates[0].get_text(strip=True)  # 即期買入
            sell_rate = rates[1].get_text(strip=True)  # 即期賣出

            # 寫入 CSV
            csv_writer.writerow([currency_name, buy_rate, sell_rate])

    print("✅ 匯率資料已成功寫入 exchange_rates.csv！")

else:
    print("❌ 無法取得網頁內容")
