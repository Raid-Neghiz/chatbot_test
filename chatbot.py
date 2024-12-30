import nltk

nltk.data.path.append('/Users/raidneghiz/nltk_data')

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)



from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st

with open('/Users/raidneghiz/Documents/Simple_Chatbot/text.txt', 'r') as file:
    data = file.read().replace('\n', ' ')

sentences = sent_tokenize(data)

def preprocess(sentence):
    words = word_tokenize(sentence)

    stop_words = stopwords.words('english')
    words = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return words

vocab_list = [preprocess(sentence) for sentence in sentences]

def most_relevant_sentence(query):
    query = preprocess(query)

    max_similarity = 0
    relevant_sentence = " "

    for sentence in vocab_list:
        intersection = set(query).intersection(sentence)
        union = set(query).union(sentence)
        similarity = len(intersection) / len(union)
        if similarity > max_similarity:
            max_similarity = similarity
            relevant_sentence = " ".join(sentence)
    return relevant_sentence

def main():
    st.sidebar.title('Chatter')
    st.title('Chatbot')
    st.write("<h3 style='text-align: center; color: #4CAF50;'>Ask me Anything</h3>", unsafe_allow_html=True)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.write("<div style='background-color: #f1f1f1; padding: 10px; border-radius: 10px;'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"<div style='background-color: #d1ecf1; color: #0c5460; padding: 10px; margin-bottom: 10px; border-radius: 10px;'>You: {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 10px; margin-bottom: 10px; border-radius: 10px;'>Chatbot: {message['content']}</div>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)

    with st.container():
        st.write("-------")
        query = st.text_input('Your Input', placeholder='Type your input here...')
        
        if st.button("Submit"):
            if query:
                st.session_state.messages.append({"role": "user", "content": query})

                response = most_relevant_sentence(query)
                st.session_state.messages.append({"role": "chatbot", "content": response})

if __name__ == '__main__':
    main()
