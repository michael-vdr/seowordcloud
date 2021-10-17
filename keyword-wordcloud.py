import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
st.set_option('deprecation.showPyplotGlobalUse', False)
st.header("Word Cloud Generator")
st.markdown("""
This app generates Word Clouds for the top 10 results for a certain keywords in Google. 
* **
Enter the search settings in the left sidebar to get started. 
* You can make a custom search engine on [cse.google.com](https://cse.google.com)
* **Python libraries:** streamlit, pandas, request, beautifulesoup, re, wordclud, matplotlib, googleapiclient
* **Created by: ** Michael Van Den Reym [Twitter](https://www.twitter.com/vdrweb) - [Linkedin](https://www.linkedin.com/in/michaelvdr).
""")

st.sidebar.header("Google Search Settings")

keyword = st.sidebar.text_input(label='Enter the keyword')
apikey = st.sidebar.text_input(label='Enter custom search engine API key')
searchengineid = st.sidebar.text_input(label='Enter Custom Search Engine ID')

st.sidebar.header("How many words in the word cloud?")
words = st.sidebar.selectbox("Number of words",range(10,1000,10))
#with st.form("top10"):
#	submit_button = st.form_submit_button(label='Get top 10 results')
#with st.form("wordcloud"):
#	URL = st.text_input(label="Enter URL")
#	submit_button = st.form_submit_button(label='Make wordcloud')

if keyword is not None and len(apikey)==39 and len(searchengineid)==33:
	API_KEY = apikey
	# get your Search Engine ID on your CSE control panel
	SEARCH_ENGINE_ID = searchengineid
	query = keyword
	# using the first page
	page = 1
	start = (page - 1) * 10 + 1
	url = f"https://www.googleapis.com/customsearch/v2?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
	service = build("customsearch", "v1",developerKey=API_KEY)
	res = service.cse().list(
        q=keyword,
        cx=SEARCH_ENGINE_ID,
	).execute()
	for item in res["items"]:
		link = item["link"]
		st.write(link)
		try:
			r = requests.get(link)
			if r.status_code == 200:
				soup = BeautifulSoup(r.content,'html.parser')
				#table = soup.find('div',attrs={"id":"main-content"})
				text = soup.text.strip()
				cleaned_text = re.split('\t',text)
				cleaned_text= " ".join(cleaned_text)
				cleaned_texts = re.split('\n',str(cleaned_text))	
				cleaned_textss = " ".join(cleaned_texts)
				stopwords = set(STOPWORDS)
				stopwords.add('N')
				stopwords.add('n')
				wordcloud = WordCloud(background_color="white",max_words=words,stopwords=stopwords).generate(cleaned_textss)
				plt.imshow(wordcloud,interpolation='bilinear')
				plt.axis("off")
				plt.show()
				st.pyplot()
			else:
				st.write("Bad Status code")
		except:
			st.write("Website not accessible for bots")

#if URL is not None:
#	r = requests.get(URL)
#	soup = BeautifulSoup(r.content,'html.parser')
#	#table = soup.find('div',attrs={"id":"main-content"})
#	text = soup.text
#	cleaned_text = re.split('\t',text)
#	cleaned_texts = re.split('\n',str(cleaned_text))	
#	cleaned_textss = "".join(cleaned_texts)
#	st.write("Your word cloud")
#	stopwords = set(STOPWORDS)
#	wordcloud = WordCloud(background_color="white",max_words=words,stopwords=stopwords).generate(cleaned_textss)
#	plt.imshow(wordcloud,interpolation='bilinear')
#	plt.axis("off")
#	plt.show()
#	st.pyplot()