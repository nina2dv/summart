import streamlit as st
import openai

openai.api_key = st.secrets['openai_KEY']

def extract_key_findings(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please find the key insights from the below text in maximum of 5 bullet points list format and also the summary in maximum of 3 sentences:\n" + text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text

def key_words(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please extract the important keywords from the below text\n" + text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text

def most_positive_words(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please extract the most positive keywords from the below text\n" + text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text

def most_negative_words(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please extract the most negative keywords from the below text\n" + text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text

# Main Page

st.title("Input Analyzer :page_with_curl:")

input_text = st.text_area("Enter your text to analyze")

if input_text is not None:
    if st.button("Analyze Text"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Key Findings based on your Text**")
            st.success(extract_key_findings(input_text))
        with col2:
            st.markdown("**Keywords**")
            st.info(key_words(input_text))
            st.markdown("""---""")
            st.markdown("**Most Positive Words**")
            st.success(most_positive_words(input_text))
            st.markdown("""---""")
            st.markdown("**Most Negative Words**")
            st.error(most_negative_words(input_text))
