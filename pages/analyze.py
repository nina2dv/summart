import streamlit as st
import newspaper
import nltk
nltk.download('punkt')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
# NLP Pkgs
import spacy_streamlit
import spacy
spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
from spacytextblob.spacytextblob import SpacyTextBlob
nlp.add_pipe("spacytextblob")

import openai

openai.api_key = st.secrets['openai_KEY']

def open_summarize(prompt):
    augmented_prompt = f"summarize this text: {prompt}"
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=augmented_prompt,
        temperature=.5,
        max_tokens=1500,
    ).choices[0].text

st.set_page_config(page_title="Summarticle", page_icon="📰", layout="wide")

st.title('Article Analyzer')
url = st.text_input("", placeholder='Paste URL and Enter')

if url:
    article = newspaper.Article(url)

    article.download()
    article.parse()
    article.nlp()
    try:
        top_image = article.top_image

        st.image(top_image, width=400)
    except:
        st.write("No Image :(")

    st.write('Article Title: ' + article.title)
    authors = article.authors
    st.write("Author(s): " + ', '.join(authors))
    st.write('Published Date: ' + str(article.publish_date))
    st.write('Article Source: ' + article.source_url)

    st.subheader("Keywords")
    key = article.keywords
    st.write(", ".join(key))

    parser = PlaintextParser.from_string(article.text, Tokenizer("english"))

    art_sum = article.summary

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Full Text', 'Summary', 'Extra Summarizers', 'NER', 'Sentiment', 'Images'])
    with tab1:
        article.text
    with tab2:
        st.subheader("OpenAI Summary: ")
        try:
            open_text = open_summarize(article.text)
            st.write(open_text)
        except openai.error.InvalidRequestError:
            st.write("_Exceed this model's maximum context length (limit is around 1125 words) :(_")
        st.markdown("""---""")
        st.subheader("Newspaper3k Summary: ")
        st.write(art_sum)
    with tab3:
        sentences_count = st.slider('Max sentences per summary:', min_value=1,
                                            max_value=10,
                                            value=3)
        st.subheader("Lexrank: Unsupervised approach to text summarization based on graph-based centrality scoring of sentences")
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count)
        summary_list = [str(sentence) for sentence in summary]
        result = ' '.join(summary_list)
        st.write(result)

        st.markdown("""---""")
        st.subheader("Luhn: Based on frequency of most important words")
        summarizer_luhn = LuhnSummarizer()
        summary_1 = summarizer_luhn(parser.document, sentences_count)
        summary_list = [str(sentence) for sentence in summary_1]
        result = ' '.join(summary_list)
        st.write(result)

        st.markdown("""---""")
        st.subheader("Lsa: Based on term frequency techniques with singular value decomposition to summarize texts")
        summarizer_lsa = LsaSummarizer()
        summary_2 = summarizer_lsa(parser.document, sentences_count)
        summary_list = [str(sentence) for sentence in summary_2]
        result = ' '.join(summary_list)
        st.write(result)

        st.markdown("""---""")
        st.subheader("Text rank: Graph-based summarization technique with keyword extractions in from document")
        summarizer_text_rank = TextRankSummarizer()
        summary_3 = summarizer_text_rank(parser.document, sentences_count)
        summary_list = [str(sentence) for sentence in summary_3]
        result = ' '.join(summary_list)
        st.write(result)
        
    with tab4:
        if art_sum != "":
            docx = nlp(art_sum)
            spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe('ner').labels)
       
    with tab5:
         if art_sum != "":
            left_column, right_column = st.columns(2)
            with left_column:
                st.subheader(f"Polarity: {docx._.blob.polarity}")
            with right_column:
                st.subheader(f"Subjectivity: {docx._.blob.subjectivity}")

            senti = docx._.blob.sentiment_assessments.assessments
            for x in senti:
                st.text(x)
        
    with tab6:
        all_images = article.images
        for image in all_images:
            st.image(image, width=400)

