## MUT
### Market Understanding Tool

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### About

This project is intended to make a pipeline of data analysis about opportunities for data science career announced at Indeed. However, this pipeline can classify job opportunities of whenever sector, beyond data science.

### Project Details
#### Folders
| Folder  | Description  |
| :------------: | :------------: |
| **db/**  |  Folder where your Scrapy database will be saved  |
| **output/**  | Folder where your graphs and results will be saved  |
---
#### Files
| ARGS  | USAGE  |
| :------------: | :------------: |
| **[db-title]**	| It is your Scrapy database title (e. g., datascience_db)  |
| **[urls-file]**	| It is your Indeed URL filename (take a look at sample.urls)  |
| **[toxicwords-file]**  | It is the filename of list of words for not use in the analysis  (take a look at sample.toxicwords)  |
| **[num-clusters]**  |  Number of clusters to identify, in a range (e. g., 2-8) or single (e. g., 8)  |
---

### Requirements

Paraphrasing The Beatles:
" All you need is [docker](https://docs.docker.com/install/ "docker") :whale: "

### Install

###### 1. Clone this repo :pizza:

```bash
git clone https://github.com/HelioNeves/mut.git
cd /mut
```

###### 2. Basic building :wrench:

```bash
docker build . -t mut
```
---
### Running this awesome docker image

###### 1. Load ubuntu layer :rainbow:
```bash
docker run -ti --name MUT-env mut /bin/bash
```
###### 2. Once inside ubuntu, run pipeline python scripts 
###### Scrapy
```bash
python3 scraper.py [db-title] [urls-file]
```
###### Analytics app
```bash
python3 app.py [db-title] [toxicwords-file] [num-clusters]
```