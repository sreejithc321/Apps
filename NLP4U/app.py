"""
NLP4U

App to demonstrate various Natural Language Processing (NLP) capabilities.

- nltk for textual processing
- streamlit framework for UI

Author : Sreejith C
Find me @ https://sites.google.com/site/sreejithc321/

"""
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk import pos_tag
from nltk import ne_chunk
from nltk.util import ngrams
 

class NLP(object):
    '''
    Text analysis class
    '''

    def __init__(self, text):
        self.text = text

    def tokenizer(self):
        '''
        Function to extract tokens
        '''
        return word_tokenize(self.text)

    def lemmatizer(self):
        '''
        Function to extract Lemma
        '''
        lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(self.text)
        return [('Token :{}, Lemma :{}'.format(t, lemmatizer.lemmatize(t))) for t in tokens]

    def stemming(self, stemmer):
        '''
        Function to extract stems : Porter and Lancaster Stemmer
        '''
        tokens = word_tokenize(self.text)
        if stemmer == 'PorterStemmer':
            stemmer = PorterStemmer()
        elif stemmer == 'LancasterStemmer':
            stemmer = LancasterStemmer()
        return [('Token :{}, Stem :{}'.format(t, stemmer.stem(t))) for t in tokens]

    def extract_ngrams(self, num):
        '''
        Function to generate n-grams from sentences.
        '''
        n_grams = ngrams(word_tokenize(self.text), int(num))
        return [ ' '.join(grams) for grams in n_grams]
    
    def pos_tagging(self):
        '''
        Part of speech tagger
        '''
        tokens = word_tokenize(self.text)
        tags = pos_tag(tokens)
        return tags

    def ner_tagging(self):
        '''
        Named entity tagger
        '''
        named_entities = []
        for chunk in ne_chunk(pos_tag(word_tokenize(self.text))):
            if hasattr(chunk, 'label'):
                named_entities.append(
                    (chunk.label(), ' '.join(c[0] for c in chunk)))
        return named_entities


def main():
    '''
    NLP with NLTK, streamlit
    '''
    try:
   
        st.title("NLP4U ")
        st.subheader('Your Guide to Natural Language Processing (NLP) !')
        st.markdown('Put in raw text, and get back linguistic knowledge and other useful information.')
 
        sample_text = 'London is the capital and most populous city of England.  Bill Gates is looking at buying fintech startup for $1 billion.'
        text = st.text_area("Enter Your Text : ",
                            sample_text, key='text_analyzer')
        nlp = NLP(text)
        st.markdown('Click on the checkboxes to view the results.')
   

        # Tokenization
        if st.checkbox("Tokenization"):
            st.text(
                "Tokenization is the process of segmenting running text into sentences and words.")
            if st.button('Run', key='Tokenization'):
                result = nlp.tokenizer()
                st.json(body=result)

        # Lemmatization
        if st.checkbox("Lemmatization"):
            st.text("Lemmatization reduce a word to its base form.")
            if st.button('Run', key='Lemmatization'):
                result = nlp.lemmatizer()
                st.json(body=result)

        # Stemming
        if st.checkbox("Stemming"):
            st.text("Stemming link all the words into their root word.")
            stemming_options = st.selectbox(
                "Choose Stemmer", ['PorterStemmer', 'LancasterStemmer'])
            if st.button('Run', key='Stemming'):
                if stemming_options == 'PorterStemmer':
                    result = nlp.stemming('PorterStemmer')
                    st.json(body=result)
                elif stemming_options == 'LancasterStemmer':
                    result = nlp.stemming('LancasterStemmer')
                    st.json(body=result)

        # N-Grams
        if st.checkbox("N-Grams"):
            st.markdown("N-grams are a set of co-occurring or continuous sequence of n items from a sequence of large text or sentence.")
            stemming_options = st.selectbox(
                "Choose N", ['2','3','4'])
            if st.button('Run', key='ngram'):
                if stemming_options == '2':
                    result = nlp.extract_ngrams('2')
                    st.json(body=result)
                elif stemming_options == '3':
                    result = nlp.extract_ngrams('3')
                    st.json(body=result)
                elif stemming_options == '4':
                    result = nlp.extract_ngrams('4')
                    st.json(body=result)
                    
        # Tagging
        if st.checkbox("POS Tagging"):
            st.markdown("POS Tagging is the process of marking up a word in a text as corresponding to a particular part of speech.")
            if st.button('Run', key='pos'):
                result = nlp.pos_tagging()
                st.json(body=result)

        # NER
        if st.checkbox("NER Tagging"):
            st.markdown("NER seeks to locate and classify named entities in text into pre-defined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.")
            if st.button('Run', key='ner'):
                result = nlp.ner_tagging()
                st.json(body=result)

        # About
        st.sidebar.header("About")
        st.sidebar.subheader("NLP4U")
        st.sidebar.markdown("App to demonstrate various Natural Language Processing (NLP) capabilities.")
        st.sidebar.text("Created with NLTK and Streamlit")
        st.sidebar.header("By :")
        st.sidebar.text("Sreejith C")
        st.sidebar.markdown("[Profile](https://sites.google.com/site/sreejithc321/)")
        
         
    except Exception as error:
        st.exception(error)


if __name__ == '__main__':
    main()
