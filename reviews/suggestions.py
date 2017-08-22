from .models import Review, Electronic, Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np


def update_clusters():
    print('Updating Clusters')
    num_reviews = Review.objects.count()
    print (num_reviews)
    update_step = int(((num_reviews / 100) + 1) * 5)
    print (update_step)
    if num_reviews % update_step == 0:  # using some magic numbers here, sorry...
        # Create a sparse matrix from user reviews
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_electronic_ids = set(map(lambda x: x.electronic.id, Review.objects.only("electronic")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_electronic_ids) + 1), dtype=np.float32)
        for i in range(num_users):  # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i, user_review.electronic.id] = user_review.rating

        # Perform kmeans clustering
        #k = int(num_users / 10) + 2
        k = 100
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        print ('New Clusters')
        for cluster in new_clusters.values():  # clusters need to be saved before referring to users
            cluster.save()
        for i, cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))