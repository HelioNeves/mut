# Use an official Ubuntu runtime as a parent image
FROM ubuntu

# Ensure that all is up-to-date
RUN apt-get update
RUN apt-get install -qy python3.6 python3-pip
RUN pip3 install --upgrade pip

#DATA
RUN pip3 install numpy && \
    pip3 install Scrapy && \
    pip3 install sklearn-pandas

#PREPROCESSING
RUN pip3 install jellyfish && \
    pip3 install langdetect && \
    pip3 install unidecode

#LEARNING
RUN pip3 install scipy && \
    pip3 install nltk && \
    pip3 install scikit-learn

#GRAPHING
RUN pip3 install altair && \
    pip3 install vega_datasets && \
    pip3 install jupyterlab

#NLP PACKAGES
RUN python3 -c "import nltk; nltk.download('punkt')"
RUN python3 -c "import nltk; nltk.download('rslp')"


# Set the working directory to /app
WORKDIR /opportunity-scraper

# Copy the current directory contents into the container at /app
ADD . /opportunity-scraper

# Define environment variable
ENV NAME World

# Enabling command-line args
CMD []
