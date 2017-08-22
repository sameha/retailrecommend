import os, sys

proj_path = "."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retailrecommend.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
import csv
with open('../Resources/Datasets/AmazonCSV/users_first100k_reviews.csv','rU') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        user = User.objects.create_user(row[0], 'a@e.com', 'userpass')

