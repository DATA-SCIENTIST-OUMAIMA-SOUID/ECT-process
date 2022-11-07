
"""
Created on Sat Dec 19 23:46:14 2020

@author: oumaima
"""
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re
import string
import random


class SentimentalAnalysis:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.positive_tweet_tokens = twitter_samples.tokenized(
            'positive_tweets.json')
        self.negative_tweet_tokens = twitter_samples.tokenized(
            'negative_tweets.json')
        self.positive_cleaned_tokens_list = []
        self.negative_cleaned_tokens_list = []
        self.dataset = None
        self.classifier = None

    def cleaning(self):
        for tokens in self.positive_tweet_tokens:
            self.positive_cleaned_tokens_list.append(
                remove_noise(tokens, self.stop_words))
        for tokens in self.negative_tweet_tokens:
            self.negative_cleaned_tokens_list.append(
                remove_noise(tokens, self.stop_words))

    def generateClassifer(self):
        positive_tokens_for_model = get_tweets_for_model(
            self.positive_cleaned_tokens_list)
        negative_tokens_for_model = get_tweets_for_model(
            self.negative_cleaned_tokens_list)
        positive_dataset = [(tweet_dict, "Positive")
                            for tweet_dict in positive_tokens_for_model]
        negative_dataset = [(tweet_dict, "Negative")
                            for tweet_dict in negative_tokens_for_model]
        self.dataset = positive_dataset + negative_dataset
        random.shuffle(self.dataset)
        train_data = self.dataset[:7000]
        #test_data = self.dataset[7000:]
        self.classifier = NaiveBayesClassifier.train(train_data)


def classification(classifier, text):
    custom_tokens = remove_noise(word_tokenize(text))
    return classifier.classify(dict([token, True] for token in custom_tokens))




def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()  # traja3ha li asel
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
