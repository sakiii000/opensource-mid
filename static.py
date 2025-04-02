import requests
import csv

url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=9b651a1b-0732-418e-b4e9-e784417cadef&limit=1000&sort=ImportDate%20desc&format=JSON'

# 發送請求
response = requests.get(url)

if response.status_code == 200:
    try:
        data_json = response.json()
        records = data_json.get("records", [])

        if not records:
            print(" API 沒有返回任何資料！")
        else:
            print(f" API 取得 {len(records)} 筆資料，開始寫入 CSV...")

            # 寫入 CSV
            with open('static.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                csv_write = csv.writer(csvfile)
                csv_write.writerow(['county', 'sitename', 'aqi', '空氣品質'])  # 寫入標題

                for i in records:
                    csv_write.writerow([i.get('county', 'N/A'), i.get('sitename', 'N/A'),
                                        i.get('aqi', 'N/A'), i.get('status', 'N/A')])

            print(" CSV 檔案寫入完成！")

    except ValueError:
        print("❌ API 回傳的 JSON 格式錯誤！")
else:
    print(f"❌ API 請求失敗，HTTP 狀態碼: {response.status_code}")
