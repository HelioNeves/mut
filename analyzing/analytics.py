import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import altair as alt

class analytics():
    def __init__(self, data, stopwords):
        self.data = data
        self.stopwords = stopwords

    def run(self, num_clusters, title):
        # 10% of data
        minimal_df = int(len(self.data.summary)*10/100)

        tfidf = TfidfVectorizer(
            min_df = minimal_df,
            max_df = 0.95,
            max_features = 3000,
            stop_words = self.stopwords
        )

        tfidf_matrix = tfidf.fit_transform(self.data.summary)
        terms = tfidf.get_feature_names()

        from sklearn.metrics.pairwise import cosine_similarity
        dist = 1 - cosine_similarity(tfidf_matrix)

        km = KMeans(n_clusters=num_clusters).fit(tfidf_matrix)
        clusters = km.labels_.tolist()

        opportunities = { 'title': self.data.title.to_list(), 'summary': self.data.summary.to_list(), 'cluster': clusters}
        frame = pd.DataFrame(opportunities, index = [clusters] , columns = ['title', 'cluster'])
        frame['cluster'].value_counts()

        MDS()
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
        xs, ys = pos[:, 0], pos[:, 1]

        #set up cluster description using a dict
        cluster_description = {}
        for i in range(num_clusters):
            cluster_description[i] = terms[km.cluster_centers_.argsort()[:, ::-1][i][0]]+" | "+terms[km.cluster_centers_.argsort()[:, ::-1][i][1]]+" ["+str(frame['cluster'].value_counts()[i])+" jobs]"


        view = pd.DataFrame(dict(x=xs, y=ys, cluster=clusters, title=self.data.title.to_list())) 

        view['description'] = view['cluster'].map(cluster_description)

        scales = alt.selection_interval(bind='scales')

        selection = alt.selection_multi(fields=['description'])

        color = alt.condition(selection,
                            alt.Color('description:N', scale=alt.Scale(scheme='category10'), legend=None),
                            alt.value('lightgray'))

        scatter = alt.Chart(view).mark_point().encode(
            x='x:Q',
            y='y:Q',
            color=color,
            tooltip='title',
            shape=alt.Shape('description:N', legend=None)
        ).properties(width=600, height=600).add_selection(
            scales
        )



        legend = alt.Chart(view).mark_point().encode(
            y=alt.Y('description:N', axis=alt.Axis(orient='right')),
            color=color,
            shape=alt.Shape('description:N', legend=None)
        ).add_selection(
            selection
        )

        #show the scatter!
        chart = (scatter | legend).configure(background='white'
        ).configure_axisLeft(
            grid=False,
            labels=False,
            domain=False,
            ticks=False,
            title=None
        ).configure_axisX(
            grid=False,
            labels=False,
            domain=False,
            ticks=False,    
            title=None
        ).properties(title="Jobs Clusters"
        ).configure_title(fontSize=20, offset=5, orient='top', anchor='middle'
        )
        
        # salvando dentro do docker, hehe, ideal era trabalhar numa solucao tipo tensorboard
        save_url = "output/"+title+"-"+str(num_clusters)+".html"
        chart.save(save_url)

        print("\nDone! Output saved at:\n\t"+save_url)