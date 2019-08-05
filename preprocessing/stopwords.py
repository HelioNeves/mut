import nltk
from urllib.request import urlopen
from unidecode import unidecode


class stopwords:
    def __init__(self, name):
        self.name = name

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

    # Quick download method
    def download(self, url):
        response = urlopen(url)
        data = response.read().decode(response.headers.get_content_charset())
        return data

    # Load stopwords and toxic words
    def get(self, toxicwords_file):
        content = self.download(
            "https://raw.githubusercontent.com/stopwords-iso/stopwords-pt/master/stopwords-pt.txt"
        ).split("\n")

        toxicwords = []
        for line in open(toxicwords_file, "r").readlines():
            toxicwords.append(line.strip())

        for word in range(len(toxicwords)):
            content.append(toxicwords[word])

        # Stopwords standardization
        stopwords_ptbr = []
        for word in range(len(content)):
            stopwords_ptbr.append(
                self.stemming(self.tokenize(unidecode(content[word])))
            )
        return stopwords_ptbr