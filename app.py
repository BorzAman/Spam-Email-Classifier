# print('Hello')
import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load model + vectorizer
model = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))

ps = PorterStemmer()

def preprocess(text):
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    text = text.lower()
    words = text.split()
    
    words = [ps.stem(word) for word in words if word not in stopwords.words('english')]
    
    return ' '.join(words)

# UI
st.title("📧 Spam Email Classifier")

st.write("Enter a message below to check whether it is Spam or Not")

user_input = st.text_area("Type your message here:")

if st.button("Predict"):
    cleaned = preprocess(user_input)
    vector = tfidf.transform([cleaned]).toarray()
    result = model.predict(vector)

    if result[0] == 1:
        st.error("🚨 This is Spam!")
    else:
        st.success("✅ This is Not Spam")