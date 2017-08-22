from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Review, Electronic, Cluster
from .suggestions import update_clusters
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ReviewForm
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def electronic_list(request):
    electronic_list = Electronic.objects.order_by('-name')
    context = {'electronic_list':electronic_list}
    return render(request, 'reviews/electronic_list.html', context)


def electronic_detail(request, electronic_id):
    electronic = get_object_or_404(Electronic, pk=electronic_id)
    form = ReviewForm()
    return render(request, 'reviews/electronic_detail.html', {'electronic': electronic, 'form': form})

@login_required
def add_review(request, electronic_id):
    electronic = get_object_or_404(Electronic, pk=electronic_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.electronic = electronic
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:electronic_detail', args=(electronic.id,)))

    return render(request, 'reviews/electronic_detail.html', {'electronic': electronic, 'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    # get this user reviews
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('electronic')
    # from the reviews, get a set of electronic IDs
    user_reviews_electronic_ids = set(map(lambda x: x.electronic.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:  # if no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other members of the cluster
    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()[:20]
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))


    # get reviews by those users, excluding electronics reviewed by the request user
    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(electronic__id__in=user_reviews_electronic_ids)
    other_users_reviews_electronic_ids = set(map(lambda x: x.electronic.id, other_users_reviews))

    # then get an electronic list including the previous IDs, order by rating
    electronic_list = sorted(
        list(Electronic.objects.filter(id__in=other_users_reviews_electronic_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    print (electronic_list[0].average_rating())
    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username,'electronic_list': electronic_list}
    )