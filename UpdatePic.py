import requests
import json
import os
import sys
from bs4 import BeautifulSoup

with open("./characters2code.json", "r", encoding="utf-8") as file:
    data = json.load(file)

url = "https://bbs-api.miyoushe.com/post/wapi/getPostFull?gids=6&post_id=51078000&read=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Referer": "https://www.miyoushe.com/"
}

response = requests.get(url, headers=headers)
html_content = json.loads(response.text)
html = html_content['data']["post"]["post"]["content"]

soup = BeautifulSoup(str(html_content), 'html.parser')

headers = soup.find_all('h2', class_='ql-align-center')
images = soup.find_all('img')

for header, image in zip(headers, images):
    key = header.text.strip()
    value = image['src']
    retry_count = 0
    while retry_count < 3:
        try:
            response = requests.get(value, timeout=10)
            if response.status_code == 200:
                for codename_key, codename_value in data['codename'].items():
                    if isinstance(codename_value, list) and key in codename_value:
                        filename = codename_key + ".png"
                        break
                    elif codename_value == key:
                        filename = codename_key + ".png"
                        break
                else:
                    filename = key + ".png"  # 如果未匹配到，则使用原始键作为文件名

                save_path = os.path.join("./guide/Nwflower/character_overview", filename)
                with open(save_path, "wb") as file:
                    file.write(response.content)
                    print(f"已下载并保存图片：{os.path.abspath(save_path)}")
                    sys.stdout.flush()
                break
        except requests.exceptions.Timeout:
            print(f"下载超时，正在进行第{retry_count + 1}次重试...")
            sys.stdout.flush()
            retry_count += 1
        except requests.exceptions.RequestException as e:
            print("下载发生异常:", e)
            sys.stdout.flush()
            break

