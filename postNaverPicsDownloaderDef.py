import os
import re
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse


def downloader(picurl, savePath):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0.0.0 Safari/537.36"
    }
    download = requests.get(picurl.split("?")[0], headers=headers, stream=True)
    if download.status_code == 200:
        # 儲存圖片
        with open(savePath, 'wb') as file:
            file.write(download.content)
        # time.sleep(3)
    else:
        print(f"No file founded\n")


def main():
    # 確認網址符合規範
    url = input(f"Enter link address:")
    # https://post.naver.com/viewer/postView.naver?volumeNo=37653713
    pattern1 = r"https:\/\/post\.naver\.com\/viewer\/postView\.naver\?volumeNo=([0-9]{8})"
    # https://post.naver.com/viewer/postView.naver?volumeNo=36936404&memberNo=51071215
    pattern2 = r"https:\/\/post\.naver\.com\/viewer\/postView\.naver\?volumeNo=([0-9]{8})\&memberNo=([0-9]{8})"
    if not re.fullmatch(pattern1, url) and not re.fullmatch(pattern2, url):
        print(f"The link doesn't meet the criteria.")
    else:
        # 建立資料夾
        dirName = f"{url.split("=")[-1]}"
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            print(f"file created successful\n")
        else:
            print(f"file existed\n")

        # 用 selenium 建立目標網站連線
        driver = webdriver.Chrome()
        driver.get(url)

        # 待網頁載入
        time.sleep(3)

        # 用 beautifulsoup 解析
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup)

        # 找目標網址的標籤
        imgs = soup.find_all("img", class_="se_mediaImage __se_img_el")
        allowFileType = ["jpg", "png", "jpeg", "gif"]
        # print(len(imgs))
        for img in imgs:
            # 找目標網址
            src = img.get("src")
            # print(src)
            if not src:
                continue
            # 尋找並建立圖片檔案名稱
            fileName = unquote(urlparse(src).path.split("/")[-1].split(".")[0])
            # print(filename)
            extension = src.split(".")[-1].split("?")[0]
            # print(extension)
            if extension in allowFileType:
                # print(src)
                print(f"file type：{extension}")
                print(f"url:{src}")
                # 建立下載連線
                downloader(src, f"{dirName}/{fileName}.{extension}")
                print(f"{fileName} downloading{"." * 20}\n")
        driver.quit()


if __name__ == '__main__':
    main()
