import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html',
    'https://ip.164746.xyz'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36'
}

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=False)  # verify=False 忽略SSL（仅测试用）
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 根据网站的不同结构找到包含IP地址的元素
            if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                elements = soup.find_all('tr')
            elif url == 'https://ip.164746.xyz':
                elements = soup.find_all('tr')
            else:
                elements = soup.find_all('li')

            # 遍历所有元素,查找IP地址
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                for ip in ip_matches:
                    file.write(ip + '\n')
        except requests.exceptions.SSLError as e:
            print(f"SSL错误，无法访问 {url} ：{e}")
        except Exception as e:
            print(f"访问 {url} 出现异常：{e}")

print('IP地址已保存到ip.txt文件中。')
