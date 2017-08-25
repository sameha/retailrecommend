# Recommendation System
### Sameh Awaida
### Project Presentation for Toptal 

In this project, I am working for an internet company that would like to add a recommendation system to their website. The proposed task is to create a web-service that will enable the “You would also be interested in…” feature on the website.

**Important note**: This is a creative project. As such we get to choose what is the subject matter of the website in question. 

In this project, I have chosen to build a recommendation system for an e-commerce shop. Predict what the user would like to buy given his previous purchases.

In addition to several endpoints, my web service have the following specific endpoints:

- `add_review(request, electronic_id)`: adds a reviews of this item by a user and indicates if that user was previously interested in electronic_id or not.
- `user_recommendation_list(request)`: returns a list of 5 electronic_id that may be interesting to this user

In addition, you can add additional features to users and items (for instance, users can have a location, movies can have genres, and products can have categories).

This taks include:

- Writing the web service
- Create modeled sample data (or scrape it online) to populate the web service and your predictor
- Write a metric that will quantify how better your predictor is from a baseline of your choice
- Produce a script that will run your service on sample data, calculate the metric and create a report on the performance of your model.


### Approach

In this project, we have created a  collaborative filtering recommender system that can help users to come across interesting items. It uses data mining and information filtering techniques. The collaborative filtering creates suggestions for users based on their neighbors' preferences. It uses k-means clustering algorithm to categorize users based on their interests. 

I have used a subset of the [Amazon product data]('http://jmcauley.ucsd.edu/data/amazon/links.html') for my data. Specifically, I have used about 100,000 products from their electronic section, as well as about 60,000 users who made reviews on these products.

The project uses [Django]('https://www.djangoproject.com/') for the web-based services, [Bootstrap]('getbootstrap.com') for developing a responsive web project with a better user experince, and the [scikit-learn Python]('http://scikit-learn.org/stable/') library for K-Means Clustering.

### Demo

- You can check my [demo website]('http://sameh.pythonanywhere.com/reviews/') to see the project works in more details.

- Click on the [Electronic List]('http://sameh.pythonanywhere.com/reviews/electronic') to see the full list of the electronics in the project (Might take a while to load).

- Click on [Login]('http://sameh.pythonanywhere.com/accounts/login/') to check some of the recommendations. You can try any username, for example:
    - AOV5BX24NBV29
    - ARL3CPERF67ZL
    - ACSX5AIZE3MJ9
    - A2541BCFAIQ7TY
    - A17JE4HESSQ1NA
They all have the same password, which is 'userpass'.

- Then click on the [Electronic Suggestions]('http://sameh.pythonanywhere.com/reviews/recommendation/') button to check 5 recommendations for that user.

