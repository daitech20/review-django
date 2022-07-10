from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.views import View, generic
from .models import Review, Store
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .form import ReviewForm, ReviewFormGoogle
from django.http import HttpResponse, HttpResponseRedirect
import time
from django.shortcuts import redirect
from django.urls import reverse


# Create your views here.
def Home(request):
    value = request.COOKIES.get('store_name')
    print('store', value)

    return render(request, 'review/Home.html', {})

class ReviewPage(View):
    def get(self, request, store_name):
        store = Store.objects.get(store_name=store_name)
        form = ReviewForm(initial={'review_score': 0})
        form2 = ReviewFormGoogle(initial={'review_score': 0})
        data = {
            'store': store,
            'form': form,
            'form2': form2
        }

        return render(request, 'review/Review.html', data)

    def post(self, request, store_name):
        store = Store.objects.get(store_name=store_name)
        form = ReviewForm(initial={'review_score': 0})
        form2 = ReviewFormGoogle(initial={'review_score': 0})
        data = {
            'store': store,
            'form': form,
            'form2': form2
        }

        if 'btnform' in request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                review = Review.objects.create(store=store, review_content=obj.review_content, phone_number=obj.phone_number, review_score=obj.review_score)
                review.save()
                print('bt')
                data['form'] = form
            else:
                form = ReviewForm(initial={'review_score': 0})
        elif 'btnform2' in request.POST:
            form2 = ReviewFormGoogle(request.POST)
            if form2.is_valid():
                obj = form2.save(commit=False)
                review = Review.objects.create(store=store, review_score=obj.review_score)
                review.save()
                print('google')
                data['form2'] = form2
                response = redirect('/accounts/google/login/')
                response.set_cookie('store_name', store_name)
                response.set_cookie('review_score', obj.review_score)
                # return render(request, 'review/Home.html', {})
                return response


            else:
                form2 = ReviewForm(initial={'review_score': 0})
        
        return render(request, 'review/Review.html', data)

# class ReviewPageGoogle(View):
#     def get(self, request, store_name):
#         store = Store.objects.get(store_name=store_name)
#         form = ReviewFormGoogle(initial={'review_score': 0})
#         data = {
#             'store': store,
#             'form2': form
#         }
#
#         return render(request, 'review/Review.html', data)

# fb_id = SocialAccount.objects.filter(user=user)


def Dashboard(request, any):
    return render(request, 'DashboardClient.html')

def LoginSuccess(request):
    # value = request.COOKIES.get('store_name')
    # print('store', value)
    google_user = SocialAccount.objects.filter(user=request.user)
    print(request.COOKIES.get('store_name'))
    print(request.COOKIES.get('review_score'))
    return render(request, 'review/Home.html', {})
