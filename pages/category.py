import streamlit as st
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import requests
import newspaper
import nltk
nltk.download('punkt')

flag = True
error_dict = {400: "Bad Request", 403: "Forbidden", 404: "Not Found", 500: "Internal Server Error", 502: "Bad Gateway", 503: "Service Unavailable"}

def summarize_html(url: str, sentences_count: int, language: str = 'english') -> str:
    try:
        parser = HtmlParser.from_url(url, Tokenizer(language))
    except requests.exceptions.HTTPError as e:
        st.markdown(f"## {e.response.status_code} - {error_dict[e.response.status_code]}")
        st.write("--Check out a different category in the meantime--")
        st.code(e.response.text, language='http')
        global flag 
        flag = False
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    summary = ''
    if flag:
        for sentence in summarizer(parser.document, sentences_count):
            if not summary:
                summary += str(sentence)
            else:
                summary += ' ' + str(sentence)

    return summary


def news_api_request(url: str, **kwargs) -> list:
    params = kwargs
    res = requests.get(url, params=params)
    articles = res.json().get('articles')
    return articles


def summarize_news_api(articles: list, sentences_count: int) -> list:
    for article in articles:
        if flag: 
            summary = summarize_html(article.get('url'), sentences_count)
            article.update({'summary': summary})
        else:
            articles = []

    return articles

def search_articles(sentences_count: int, **kwargs) -> list:
    url = 'https://newsapi.org/v2/everything/'
    articles = news_api_request(url, **kwargs)
    return summarize_news_api(articles, sentences_count)


def get_top_headlines(sentences_count: int, **kwargs) -> list:
    url = 'https://newsapi.org/v2/top-headlines/'
    articles = news_api_request(url, **kwargs)
    return summarize_news_api(articles, sentences_count)


API_KEY = st.secrets['API_KEY']

st.title('News Summarizer by Category')

sentences_count = st.sidebar.slider('Max sentences per summary:', min_value=1,
                                    max_value=10,
                                    value=3)

category = st.sidebar.selectbox('Search Top Headlines by Category:', options=['business',
                                                                'entertainment',
                                                                'general',
                                                                'health',
                                                                'science',
                                                                'sports',
                                                                'technology'], index=1)

summaries = get_top_headlines(sentences_count, apiKey=API_KEY,
                              sortBy='publishedAt',
                                  country='ca',
                                  category=category)

for i in range(len(summaries)):
    left_column, right_column = st.columns(2)
    with left_column:
        st.header(f"{[summaries[i]['title']]}({summaries[i]['url']})")
    with right_column:
        try:
            st.image(summaries[i]['urlToImage'], width=400)
        except:
            st.write("_No Image :(_")
    st.markdown(
        f"<span style = 'background-color:#FF4B4B; padding:10px; border-radius:20px'> Published at: {summaries[i]['publishedAt']}</span>",
        unsafe_allow_html=True)
    # st.write("URL: " + summaries[i]['url'])

    left_col, right_col = st.columns(2)
    with left_col:
        if summaries[i]['author']:
            st.markdown("### Author(s): " + summaries[i]['author'])
    with right_col:
        st.markdown(f"### Source: {summaries[i]['source']['name']}")

    arti = newspaper.Article(summaries[i]['url'])

    try:
        arti.download()
        arti.parse()
        arti.nlp()
        key = arti.keywords
        st.markdown("##### Keywords: " + ", ".join(key))
        # st.write("Summary: " + arti.summary)
    except:
        st.write("_No Keywords :(_")

    if summaries[i]['summary']:
        st.write("Summary: " + summaries[i]['summary'])
    else:
        st.write("_No Summary :(_")

    try:
        st.write("Description: " + summaries[i]['description'])
    except:
        st.write("_No Description :(_")

    st.markdown("""---""")

