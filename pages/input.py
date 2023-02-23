import streamlit as st
import openai
openai.api_key = st.secrets['openai_KEY']
# prompt="Please find the key insights from the below text in maximum of 5 bullet points list format and also the summary in maximum of 3 sentences:\n" + text,


def extract_key_findings(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please find the key insights from the below text in maximum of 5 bullet points list format:\n" + text,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text


def extract_summary(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please create a summary from the below text  in maximum of 3 sentences:\n" + text,
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
        temperature=0.6,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text


def sentiment(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please classify the sentiment of the below text between 'Positive', 'Neutral' or 'Negative':\n" + text,
        temperature=0.6,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text


def most_positive_words(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please extract the most positive keywords from the below text\n" + text,
        temperature=0.45,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text


def most_negative_words(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please extract the most negative keywords from the below text\n" + text,
        temperature=0.45,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response.choices[0].text


# Main Page
st.title("Input Analyzer :page_with_curl:")


form = st.form(key='my_form')
input_text = form.text_area(label='Enter your text to analyze', height=450)
submit_button = form.form_submit_button(label='Analyze Text')

if input_text is not None and submit_button:
    col1, col2 = st.columns(2)
    with col1:
        try: 
            st.markdown("**Key Findings**")
            st.info(extract_key_findings(input_text))

            st.markdown("""---""")

            st.markdown("**Summary**")
            st.info(extract_summary(input_text))
        except openai.error.InvalidRequestError:
            st.warning("**Error**")
    with col2:
        try:
            st.markdown("**Sentiment Classification**")
            st.info(sentiment(input_text))

            st.markdown("""---""")

            st.markdown("**Keywords**")
            st.info(key_words(input_text))

            st.markdown("""---""")

            st.markdown("**Most Positive Words**")
            st.success(most_positive_words(input_text))

            st.markdown("""---""")

            st.markdown("**Most Negative Words**")
            st.error(most_negative_words(input_text))
        
        except openai.error.InvalidRequestError:
            st.warning("**Error**")
    image_resp = openai.Image.create(prompt=input_text, n=1, size="512x512")
    st.image(image_resp["data"][0]["url"])

    
