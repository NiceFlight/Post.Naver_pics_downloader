import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

# 用 selenium 建立目標網站連線
driver = webdriver.Chrome()
url = input(f"Enter link address:")
driver.get(url)
# 待網頁載入
time.sleep(3)

# 用 beautifulsoup 解析
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 建立資料夾
print(dir)
dir_name = f"images/{url.split("=")[-1]}"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    print(f"file created successed\n")
else:
    print(f"file existed\n")

# 找目標網址的標籤
imgs = soup.find_all("img")
allow_file_name = ["jpg", "png", "jpeg", "gif"]
for img in imgs:
    # 找目標網址
    src = img.get("src")
    if not src:
        continue

    # 尋找並建立圖片檔案名稱
    filename = quote(urlparse(src).path.split("/")[-1].split(".")[0])
    extension = src.split(".")[-1].split("?")[0]
    if extension in allow_file_name:
        print(f"file type：{extension}")
        print(f"url:{src}")
        
        # 建立下載連線
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36"
        }
        download = requests.get(src.split("?")[0], headers=headers, stream=True)
        if download.status_code == 200:
            # 儲存圖片
            with open(f"images/{url.split("=")[-1]}/{filename}.{extension}", 'wb') as file:
                file.write(download.content)
            print(f"{filename} downloading{"." * 20}\n")
            # time.sleep(3)
        else:
            print(f"No file founded\n")
driver.close()
