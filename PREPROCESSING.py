
"""
Created on Sat Dec 19 23:30:36 2020

@author: oumaima
"""
import demoji
import re
from textblob import TextBlob
import string
from spellchecker import SpellChecker
import time


def convert_emojis(text):
    return demoji.replace_with_desc(text, " ")


def Find(str1):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, str1)
    y = [x[0] for x in url]
    for yy in y:
        str1 = str1.replace(yy, "")
    return str1


def orth_corr(text1):
    try:
        blob = TextBlob(text1)
        l = blob.detect_language()
        text = text1.split()
        exclude = set(string.punctuation)
        text = [ch for ch in text if ch not in exclude]
        spell = SpellChecker(language=str(l))
        spell.distance = 1
        misspelled = spell.unknown(text)
        t = ""
        for word in misspelled:
            t = " ".join(text)
            t = t.replace(word, spell.correction(word))
        return t
    except:
        return text1


def translate_comments(text):
    time.sleep(1)
    eng = text
    try:
        if len(text) >= 3:
            text1 = TextBlob(text)
            l = text1.detect_language()
            if not l == 'en' and len(text) >= 3:
                analysis = TextBlob(text)
                eng = analysis.translate(to='en')
            else:
                eng = text
    except:
        eng = text
    return eng
