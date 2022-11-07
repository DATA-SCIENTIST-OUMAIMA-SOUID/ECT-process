import os
import pandas as pd
import numpy as np
from pretraitement import *
from sentimental import *


# getting only comments
print("Importing data from csv file")
df_final = pd.read_csv("export_dataframe.csv", error_bad_lines=False, sep=";")

print("Creation of the data frame")
new = df_final['comment'][:200]
new = pd.DataFrame(new)

print("Replacing emojis with a text description")
new['rv_emoji'] = new['comment'].apply(lambda x: convert_emojis(x))

print("Removal of urls")
new['find_url'] = new['rv_emoji'].apply(lambda x: Find(x))

# print("Suppression des lignes vides")
# new = new.replace(np.nan, '-', regex=True)

print("Translation all comments in English")
new["translated"] = new['find_url'].apply(lambda x: translate_comments(x))

print("Spelling correction")
new['correction'] = new['translated'].apply(lambda x: orth_corr(x))


print("------------sentimental analysis----------------")
print("Recovery of stop words in English, as well as positive and negative terms")
analyseur = SentimentalAnalysis()

print("Data cleaning")
analyseur.cleaning()

print("Generating the dataset and creating a classification object")
analyseur.generateClassifer()
classifier = analyseur.classifier

print("Adding a sentiment column to the dataframe")
new["sentiment"] = new['translated'].apply(
    lambda x: classification(classifier, str(x)))

print("Saving the result data frame in a csv file")
new.to_csv("./out25.csv", sep=";", index=False)


