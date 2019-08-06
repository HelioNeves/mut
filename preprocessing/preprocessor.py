import numpy as np
import pandas as pd
import nltk
import jellyfish as jf
from langdetect import detect
from unidecode import unidecode


class preprocessor:
    def __init__(self, path):
        self.path = "db/" + path
        self.data = pd.read_csv(self.path)

    # Remove duplications with Jellyfish and his hamming distance method
    def remove_duplications(self):
        print("\nRemoving duplications...")
        duplications = []

        for ix in range(len(self.data)):
            for yx in range(ix, len(self.data)):
                if ix != yx:
                    if (
                        jf.hamming_distance(
                            str(self.data.summary[ix])[0:200], str(self.data.summary[yx])[0:200]
                        )
                        <= 20
                    ):
                        duplications.append(yx)

        duplications = list(set(duplications))
        self.data = self.data[~self.data.index.isin(duplications)].reset_index(
            drop=True
        )

    # Remove non-portuguese entries with langdetect package
    def remove_nonpt(self):
        print("\nRemoving non portuguese entries...")
        nonpt_ix = []

        for ix in range(len(self.data)):
            if detect(str(self.data.summary[ix])) != "pt":
                nonpt_ix.append(ix)

        self.data = self.data[~self.data.index.isin(nonpt_ix)].reset_index(drop=True)

    # Sentence tokenization
    def tokenize(self, sentence):
        sentence = sentence.lower()
        sentence = nltk.word_tokenize(sentence)
        return sentence

    # Quick stemming method
    def stemming(self, sentence):
        stemmer = nltk.stem.RSLPStemmer()
        phrase = []
        for word in sentence:
            phrase.append(stemmer.stem(word.lower()))
        return " ".join(phrase)

    # Remove formatation on dataset's title, company and sumary
    # And stem sentences from dataset's summary
    def standardization(self):
        print("\nApplying dataset standardization...")
        for ix in range(len(self.data)):
            # Title: formatation, accent
            self.data.at[ix, "title"] = (
                str(self.data.title[ix])
                .lower()
                .replace("\n", "")
                .replace("\t", "")
                .replace(",", " ")
            )
            self.data.at[ix, "title"] = unidecode(self.data.at[ix, "title"])

            # Company: formatation, accent
            self.data.at[ix, "company"] = (
                str(self.data.company[ix])
                .lower()
                .replace("\n", "")
                .replace("\t", "")
                .replace(",", " ")
            )
            self.data.at[ix, "company"] = unidecode(self.data.at[ix, "company"])

            # Summary: formatation, accent, number digits and stem
            self.data.at[ix, "summary"] = (
                str(self.data.summary[ix])
                .lower()
                .replace("\n", "")
                .replace("\t", "")
                .replace(",", " ")
            )
            self.data.at[ix, "summary"] = unidecode(self.data.at[ix, "summary"])
            self.data.at[ix, "summary"] = "".join(
                filter(lambda x: not x.isdigit(), self.data.at[ix, "summary"])
            )
            self.data.at[ix, "summary"] = self.stemming(
                self.tokenize(self.data.at[ix, "summary"])
            )

    def run(self):
        print("\tDataset's size: " + str(len(self.data.summary)))
        self.remove_duplications()
        print("\tDataset's size: " + str(len(self.data.summary)))
        self.remove_nonpt()
        print("\tDataset's size: " + str(len(self.data.summary)))
        self.standardization()
        print("\tDone!")
        return self.data