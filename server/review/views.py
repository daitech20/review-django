from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.views import View, generic
from rest_framework import generics, status
from .models import Review, Store, Customer
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from .form import ReviewForm, ReviewFormGoogle
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from .serializer import CustomJWTSerializer, ReviewSerializer, StoreSerializer, RegisterSerializer,\
    UpdateStoreSerializer, DetailStoreSerializer, UserSerializer, ChangePasswordSerializer,\
    CustomerSerializer, ResetPasswordSerializer, SocialApplicationSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly


# Create your views here.
def Home(request):
    value = request.COOKIES.get('store_name')
    print('store', value)

    return render(request, 'review/Home.html', {})

class ReviewPage(View):
    def get(self, request, store_slug):
        store = Store.objects.get(store_slug=store_slug)
        form = ReviewForm(initial={'review_score': 0})
        form2 = ReviewFormGoogle(initial={'review_score': 0})
        data = {
            'store': store,
            'form': form,
            'form2': form2
        }

        return render(request, 'review/Review.html', data)

    def post(self, request, store_slug):
        store = Store.objects.get(store_slug=store_slug)
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
                customer = store.customer.filter(phone=obj.phone_number)
                if not customer:
                    customer = Customer.objects.create(phone=obj.phone_number)
                else:
                    customer = customer[0]
                store.customer.add(customer)
                store.save()

                data['form'] = form
                data['message'] = "Thanks you for review!"
            else:
                form = ReviewForm(initial={'review_score': 0})
        elif 'btnform2' in request.POST:
            form2 = ReviewFormGoogle(request.POST)
            if form2.is_valid():
                obj = form2.save(commit=False)
                data['form2'] = form2
                response = redirect('/accounts/google/login/')
                response.set_cookie('store_name', store.store_name)
                response.set_cookie('review_score', obj.review_score)
                return response
            else:
                form2 = ReviewForm(initial={'review_score': 0})
        
        return render(request, 'review/Review.html', data)


def Dashboard(request, any):
    return render(request, 'DashboardClient.html')

def LoginSuccess(request):
    data = SocialAccount.objects.filter(user=request.user)[0].extra_data
    social_account = User.objects.filter(email=data.get('email')).last()
    social_account.delete()
    store_name = request.COOKIES.get('store_name')
    review_score = request.COOKIES.get('review_score')
    store = Store.objects.get(store_name=store_name)
    customer = store.customer.filter(email=data.get('email'))
    if not customer:
        customer = Customer.objects.create(full_name=data.get('name'), email=data.get('email'))
    else:
        customer = customer[0]

    store.customer.add(customer)
    store.save()
    review = Review.objects.create(store=store, review_score=review_score, customer_name=data.get('name'), review_email=data.get('email'))
    review.save()

    return HttpResponseRedirect(store.url_map_store)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer

class StoreList(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Store.objects.all()

        return Store.objects.filter(user=user)

class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        store_slug = self.kwargs['store_slug']
        store = Store.objects.get(store_slug=store_slug)

        return qs.filter(store=store).order_by('-created_at')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class StoreCreate(generics.CreateAPIView):
    queryset = Store
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StoreDetail(generics.RetrieveAPIView):
    queryset = Store
    serializer_class = DetailStoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'store_slug'

class StoreUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store
    serializer_class = UpdateStoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'store_slug'

	
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
	
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    lookup_field = 'username'

# array[
#     'userDetail': {
#         view: (user, extrasData) {
#             return user.is_superuser || user.username = etraxData
#         }
#     }
# ]


# class Permission (user):
#
#     def getPerssionDeifination(self, resouceName):
#         return find resouceName in array
#
#     def canEdit(self, resource):
#         return true
#
#     def canView(self, resource):
#         permisisonDefiniation = getPerssionDeifination(resouce.name)
#         return permisisonDefiniation ? permissions.hasPermission(user, resource.extradaa) : false
#
#     def canDelete(self, resource):
#         return true
#
#     def canCreate(self, resource):

class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ChangePasswordSerializer
    lookup_field = 'username'

class ResetPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ResetPasswordSerializer
    lookup_field = 'username'

class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        store = Store.objects.get(store_slug=self.kwargs['store_slug'])
        customers = store.customer.all().order_by('-id')
        return customers

class CustomerUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class SocialApplicationUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialApp.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = SocialApplicationSerializer
    lookup_field = 'pk'