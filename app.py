#   HOW RUN IT
# python3 app.py [db-title] [toxicwords-file] [num-clusters]
import sys
import numpy as np
import pandas as pd

# PREPROCESSING
from preprocessing.preprocessor import preprocessor
from preprocessing.stopwords import stopwords

# ANALYZING
from analyzing.analytics import analytics

# ARGS
title = sys.argv[1] + ".csv"
toxicwords_file = sys.argv[2]
num_clusters = sys.argv[3].split("-")

# Preprocessing
print("\n>Preprocessing...\n")
pd = preprocessor(title).run()
print("\n>Preprocessing done!")

# Analytics
print("\n>Analytics...")
print("Processing clusters:")
model = analytics(pd, stopwords("PTBR").get(toxicwords_file))

if len(num_clusters) > 1:
    for r in range(int(num_clusters[0]), (int(num_clusters[1]) + 1)):
        model.run(r, title)
else:
    model.run(int(num_clusters[0]), title)

print("\n>Analytics done!")
