import requests
from bs4 import BeautifulSoup
import re
from transformers import pipeline

# get_article_text(url): 뉴스기사의 텍스트를 추출하는 함수
def get_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve article: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # 뉴스 사이트마다 기사 본문을 포함하는 태그가 다를 수 있음
    # 일반적인 예시 (다양한 태그 시도)
    article_body = soup.find_all('p')
    if not article_body:
        article_body = soup.find_all('div', {'class': 'article-content'})
        if not article_body:
            print("No article body found!")
            return None

    article_text = ' '.join([p.get_text() for p in article_body])
    return article_text

# preprocess_text(text): 뉴스 데이터를 전처리하는 함수
def preprocess_text(text):
    # HTML 태그 제거
    text = BeautifulSoup(text, 'html.parser').get_text()

    # 추가 전처리 (불필요한 문자 제거, 텍스트 정규화 등)
    text = text.lower()  # 소문자 변환
    text = re.sub(r'\[[^]]*\]', '', text)  # 대괄호로 감싸진 텍스트 제거
    text = re.sub(r'http\S+', '', text)  # URL 제거
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # 특수문자 제거
    text = re.sub(r'\s+', ' ', text)  # 중복 공백 제거

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
summary = summarizer(clean_text, max_length=130, min_length=30, do_sample=False)
print(f"Summary: {summary[0]['summary_text']}")



'''

# 감정 분석 모델 로드
sentiment_analyzer = pipeline('sentiment-analysis')

# 감정 분석 수행
sentiment = sentiment_analyzer(clean_text)
print(f"Sentiment: {sentiment[0]}")

# 신뢰성 평가 (예시)
def evaluate_reliability(article_text):
    unreliable_keywords = ['rumor', 'allegation', 'unverified']
    score = 100
    for keyword in unreliable_keywords:
        if keyword in article_text.lower():
            score -= 20
    return max(score, 0)

reliability_score = evaluate_reliability(clean_text)
print(f"Reliability Score: {reliability_score}/100")

'''