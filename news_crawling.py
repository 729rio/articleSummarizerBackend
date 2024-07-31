import requests
from bs4 import BeautifulSoup
import re
from transformers import pipeline

# 뉴스기사의 텍스트를 추출하는 함수
def get_article_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve article: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 뉴스 사이트마다 기사 본문을 포함하는 태그가 다를 수 있음
    article_body = soup.find_all('p')
    if not article_body:
        article_body = soup.find_all('div', {'class': 'article-content'})
        if not article_body:
            print("No article body found!")
            return None

    article_text = ' '.join([p.get_text() for p in article_body])
    return article_text

# 뉴스 데이터를 전처리하는 함수
def preprocess_text(text):
    # HTML 태그 제거
    text = BeautifulSoup(text, 'html.parser').get_text()

    # 추가 전처리 (불필요한 문자 제거, 텍스트 정규화 등)
    text = text.lower()  # 소문자 변환
    text = re.sub(r'\[[^]]*\]', '', text)  # 대괄호로 감싸진 텍스트 제거
    text = re.sub(r'http\S+', '', text)  # URL 제거
    text = re.sub(r'[^a-zA-Z0-9\s\.,]', '', text)  # Keep periods and commas for better sentence structure
    text = re.sub(r'\s+', ' ', text)  # 중복 공백 제거
    text = text.strip()  # 앞뒤 공백 제거

    return text

# URL 샘플
url = 'https://www.forbes.com/sites/tylerroush/2024/06/06/spacex-launching-starships-fourth-test-flight-heres-how-to-follow-along/?sh=5c472e41b879'
article_text = get_article_text(url)

if article_text:
    # 첫 500자만 출력
    print(f"Article Text: {article_text[:500]}...")
else:
    print("Failed to retrieve the article text")

# 텍스트 전처리
clean_text = preprocess_text(article_text)
print(f"Clean Text: {clean_text[:500]}...")


# 요약 모델 로드
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

# 요약 생성
#summary = summarizer(clean_text, max_length=130, min_length=30, #do_sample=False)
#print(f"Summary: {summary[0]['summary_text']}")

# 기사 요약 함수
def summarize_article(url):
    article_text = get_article_text(url)
    if article_text:
        clean_text = preprocess_text(article_text)
        summary = summarizer(clean_text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    else:
        return "Failed to retrieve the article text"
