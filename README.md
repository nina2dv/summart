# summarticle
## Inspiration
Inspired by [Hugging Face Summarization](https://huggingface.co/tasks/summarization), I wanted some app that would output the important details of an article. Having a brief overview of a long body of text would aid students in finding appropriate sources for research assignments and save them time. 

## What it does
Summarticle provides a summary for news articles from the user input (search bar) or category. There is also a page where the user can insert a URL of some text online and it would try to analyze (summarize, name-entity-recognition, sentiment) it. 

## How we built it
Used Streamlit for the web app, NewsAPI, and NLP (Spacy, newspaper, sumy, OpenAI). 

## Challenges we ran into
There were a lot of HTTP Error from requests.exceptions.HTTPError. 

## Accomplishments that we're proud of
Integrating NewsAPI with Streamlit and NLP.

## What's next for Summarticle
Optimizing the application to reduce the load/wait time. I could also implement the approximate wait time for the site to load and process.
