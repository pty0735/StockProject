import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_colwidth', None)  # 컬럼 내 전체 내용 출력
stock = input("주식 종목을 입력하세요: ")

# 검색 URL
url = f"https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query={stock}+뉴스"

# 요청 보내기
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 뉴스 제목과 채널 크롤링
data = []
articles = soup.select(".news_wrap")  # 네이버 뉴스 검색 페이지에서 기사 컨테이너 선택

for article in articles:
    title_tag = article.select_one(".news_tit")
    channel_tag = article.select_one(".info")
    link_tag = title_tag["href"] if title_tag else ""
    
    if title_tag and channel_tag:
        title = title_tag.text.strip()
        channel = channel_tag.text.replace(" 선정", "").strip()
        data.append([title, channel, link_tag])

# 데이터프레임 생성
df = pd.DataFrame(data, columns=["기사 제목", "뉴스 채널", "기사 링크"])

# 출력
print(df)