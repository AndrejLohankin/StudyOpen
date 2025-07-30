import requests
from bs4 import BeautifulSoup


url = "https://habr.com/ru/articles/"
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Ошибка загрузки страницы:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all(class_='tm-articles-list__item')
print("Подходящие статьи:\n")
keywords_lower = [kw.lower() for kw in KEYWORDS]

for article in articles:
    time_tag = article.find('a', class_='tm-article-datetime-published')
    time_tag2 = time_tag.find('time')
    raw_date = time_tag2['title']
    title_tag = article.find(class_='tm-title__link')
    title = title_tag.get_text(strip=True)
    link = "https://habr.com" + title_tag['href']
    article_response = requests.get(link, headers=headers, timeout=5)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    content = article_soup.find('div', class_='tm-article-body')
    full_text = content.get_text(strip=True).lower()
    if any(keyword in full_text for keyword in keywords_lower):
        print(f"{raw_date} – {title} – {link}")