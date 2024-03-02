import streamlit as st
import pandas as pd
import nltk
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
import datetime

nltk.download('punkt')
nltk.download('stopwords')

class JournalAI:
    def __init__(self):
        self.journal_df = pd.DataFrame(columns=['date', 'title', 'content'])

    def add_entry(self, title, content):
        if title.strip() and content.strip():
            today = datetime.date.today()
            new_entry = pd.DataFrame([[today.strftime("%Y-%m-%d"), title, content]], columns=['date', 'title', 'content'])
            self.journal_df = pd.concat([self.journal_df, new_entry], ignore_index=True)
            self.journal_df.to_csv('journals.csv', index=False)  # Save to CSV file
            st.success("Journal entry added successfully!")
        else:
            st.error("Title and content cannot be empty!")

    def view_entries(self):
        if not self.journal_df.empty:
            st.subheader("Past Journal Entries")
            st.write(self.journal_df)
        else:
            st.warning("No journal entries found.")

    def analyze_sentiment(self, content):
        if content.strip():
            blob = TextBlob(content)
            sentiment_score = blob.sentiment.polarity
            if sentiment_score > 0:
                st.write("Sentiment: Positive")
            elif sentiment_score == 0:
                st.write("Sentiment: Neutral")
            else:
                st.write("Sentiment: Negative")
        else:
            st.error("Content for sentiment analysis cannot be empty!")

    def extract_keywords(self, content):
        if content.strip():
            content = content.lower()
            words = word_tokenize(content)
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word.isalnum() and word not in stop_words and word not in string.punctuation]
            word_freq = Counter(words)
            keywords = [word[0] for word in word_freq.most_common(5)]
            st.write("Keywords:", keywords)
        else:
            st.error("Content for keyword extraction cannot be empty!")

def main():
    st.title("Journal AI")

    journal_ai = JournalAI()

    # Load existing journals if available
    try:
        journal_ai.journal_df = pd.read_csv('journals.csv')
    except FileNotFoundError:
        pass

    menu = ["Add a new journal entry", "View past journal entries", "Analyze sentiment of a journal entry", "Extract keywords from a journal entry"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a new journal entry":
        st.subheader("Add a new journal entry")
        title = st.text_input("Enter title for the journal entry:")
        content = st.text_area("Enter content for the journal entry:")
        if st.button("Add Entry"):
            journal_ai.add_entry(title, content)

    elif choice == "View past journal entries":
        st.subheader("View past journal entries")
        journal_ai.view_entries()

    elif choice == "Analyze sentiment of a journal entry":
        st.subheader("Analyze sentiment of a journal entry")
        selected_entry = st.selectbox("Select a journal entry:", journal_ai.journal_df['title'].tolist())
        content = journal_ai.journal_df.loc[journal_ai.journal_df['title'] == selected_entry, 'content'].iloc[0]
        if st.button("Analyze Sentiment"):
            journal_ai.analyze_sentiment(content)

    elif choice == "Extract keywords from a journal entry":
        st.subheader("Extract keywords from a journal entry")
        selected_entry = st.selectbox("Select a journal entry:", journal_ai.journal_df['title'].tolist())
        content = journal_ai.journal_df.loc[journal_ai.journal_df['title'] == selected_entry, 'content'].iloc[0]
        if st.button("Extract Keywords"):
            journal_ai.extract_keywords(content)

if __name__ == "__main__":
    main()
