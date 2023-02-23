import streamlit as st
import requests
import nltk
nltk.download('punkt')
import newspaper
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

st.set_page_config(page_title="Summarticle", page_icon="📰", layout="wide")
st.sidebar.success("Select a page above: ")

st.title('News Search + Summary')

form = st.form(key='my_form')
search = form.text_input(label='Search')
submit_button = form.form_submit_button(label='Enter')

apiKEY = st.secrets['API_KEY']

@st.experimental_memo
def lsa_sum(arti):
    parser = PlaintextParser.from_string(arti.text, Tokenizer("english"))
    summarizer_lsa = LsaSummarizer()
    summary_2 = summarizer_lsa(parser.document, 5)
    summary_list = [str(sentence) for sentence in summary_2]
    result = ' '.join(summary_list)
    return result

if submit_button:
    url = f"https://newsapi.org/v2/top-headlines?q={search}&apiKey={apiKEY}"
    r = requests.get(url)
    r = r.json()
    articles = r['articles']
    for article in articles:
        left_column, right_column = st.columns(2)
        with left_column:
            st.header(f"{[article['title']]}({article['url']})")
        with right_column:
            try:
                st.image(article['urlToImage'], width=400)
            except:
                st.write("_No Image :(_")
        st.markdown(f"<span style = 'background-color:#FF4B4B; padding:10px; border-radius:20px'> Published at: {article['publishedAt']}</span>", unsafe_allow_html=True)
        # st.write("Published at: " + article['publishedAt'])
        # st.write("URL: " + article['url'])

        left_col, right_col = st.columns(2)
        with left_col:
            if article['author']:
                st.markdown("### Author(s): " + article['author'])
        with right_col:
            st.markdown(f"### Source: {article['source']['name']}")

        try:
            arti = newspaper.Article(article['url'])
            arti.download()
            arti.parse()
            arti.nlp()
            key = arti.keywords
            st.markdown("##### Keywords: " + ", ".join(key))
            st.write("Summary: " + arti.summary)

            # result = lsa_sum(arti)
            # st.write(result)

        except:
            st.write("_No Summary :(_")

        try:
            st.write("Description: " + article['description'])
        except:
            st.write("_No Description :(_")
        # st.write(article['content'])

        st.markdown("""---""")

