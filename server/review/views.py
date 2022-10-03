from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.views import View, generic
from rest_framework import generics, status
from .models import Review, Store, Customer, MessageLog
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
    CustomerSerializer, ResetPasswordSerializer, SocialApplicationSerializer, AddCustomerStoreSerializer, MessageLogSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .apps.sendmess import send_mess
from pathlib import Path
import os
import environ
from threading import Thread
import threading

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Create your views here.
def Home(request):
    value = request.COOKIES.get('store_id')
    print('store', value)

    return render(request, 'review/Home.html', {})

class ReviewPage(View):
    def get(self, request, store_slug):
        customer_id = request.GET.get('props', None)
        print('get', customer_id)
        store = Store.objects.get(store_slug=store_slug)
        form = ReviewForm(initial={'review_score': 0})
        form2 = ReviewFormGoogle(initial={'review_score': 0})
        data = {
            'store': store,
            'form': form,
            'form2': form2,
            'customer_id': customer_id
        }

        return render(request, 'review/Review.html', data)

    def post(self, request, store_slug):
        customer_id = request.GET.get('props', None)
        print('post', customer_id)
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
                if (customer_id != 'None'):
                    try:
                        customer = Customer.objects.get(id=customer_id)
                        review.customer_name = customer.full_name
                        review.review_email = customer.email
                        review.phone_number = customer.phone
                        review.save()
                        store.customer.add(customer)
                        store.save()
                        data['form'] = form
                        data['message'] = "Thanks you for review!"
                    except:
                        data['error'] = "Customer isn't valid!"
                else:
                    customer = store.customer.filter(phone=obj.phone_number)
                    if not customer:
                        customer = Customer.objects.create(phone=obj.phone_number)
                    else:
                        customer = customer[0]
                        review.customer_name = customer.full_name
                        review.review_email = customer.email
                        review.save()

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
                response.set_cookie('store_id', store.id)
                response.set_cookie('review_score', obj.review_score)
                response.set_cookie('customer_id', customer_id)
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
    store_id = request.COOKIES.get('store_id')
    review_score = request.COOKIES.get('review_score')
    customer_id = request.COOKIES.get('customer_id')
    store = Store.objects.get(id=store_id)
    
    if (customer_id != 'None'):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.email = data.get('email')
            customer.save()
            store.customer.add(customer)
            store.save()
        except:
            pass

    else:
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

class StoreAddCustomer(generics.CreateAPIView):
    queryset = Customer
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        store_slug=self.kwargs['store_slug']
        store = Store.objects.get(store_slug=store_slug)
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            customer = store.customer.get(phone=serializer.data['phone'])
            customer.full_name = serializer.data['full_name']
            customer.email = serializer.data['email']
            customer.save()
        except:
            customer = Customer.objects.create(phone=serializer.data['phone'], full_name=serializer.data['full_name'], email=serializer.data['email'])
            store.customer.add(customer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

class SendAllMessage(generics.CreateAPIView):
    queryset = MessageLog
    serializer_class = MessageLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        store_slug=self.kwargs['store_slug']
        store = Store.objects.get(store_slug=store_slug)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        def send_mess_thread(customer):
            content = serializer.data['content']
            content = content.replace('{{review_link}}', str(store.domain) + store_slug + '?params=' + str(customer.id))
            content = content.replace('{{full_name}}', str(customer.full_name))

            try:
                sid = send_mess(content, customer.phone)
                message_log = MessageLog.objects.create(store=store)
                message_log.from_phone = env('FROM_PHONE')
                message_log.to_phone = customer.phone
                message_log.content = content
                message_log.status = 0
                message_log.sid = sid
                message_log.save()
            except:
                message_log = MessageLog.objects.create(store=store)
                message_log.from_phone = env('FROM_PHONE')
                message_log.to_phone = customer.phone
                message_log.content = content
                message_log.status = 1
                message_log.save()

        for customer in store.customer.all():
            thread = threading.Thread(target=send_mess_thread, args=(customer,))
            thread.start()

        return Response({'result': 'ok'}, status=status.HTTP_200_OK)
    
class SendMessage(generics.CreateAPIView):
    queryset = MessageLog
    serializer_class = MessageLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        store_slug = self.kwargs['store_slug']
        customer_id = self.kwargs['customer_id']
        store = Store.objects.get(store_slug=store_slug)
        customer = store.customer.get(id=customer_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        content = serializer.data['content']
        content = content.replace('{{review_link}}', str(store.domain) + store_slug + '?params=' + str(customer.id))
        content = content.replace('{{full_name}}', str(customer.full_name))

        try:
            sid = send_mess(content, customer.phone)
            message_log = MessageLog.objects.create(store=store)
            message_log.from_phone = env('FROM_PHONE')
            message_log.to_phone = customer.phone
            message_log.content = content
            message_log.status = 0
            message_log.sid = sid
            message_log.save()
        except:
            message_log = MessageLog.objects.create(store=store)
            message_log.from_phone = env('FROM_PHONE')
            message_log.to_phone = customer.phone
            message_log.content = content
            message_log.status = 1
            message_log.save()

        return Response({'result': 'ok'}, status=status.HTTP_200_OK)
 