
from django.contrib import admin
from django.conf.urls import url
from calculator import views
from django.urls import path, include
from calculator.views  import UserListCreateApiView,UserRetrieveUpdateDestroyApiView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_page,name='login'),
    url(r'^cal/', views.calculate, name='calculator'),
    url(r'^signup/', views.sign_up,name='sign-up'),
    url(r'^signup/success/', views.signup_success,name='signup_success'),
    url(r'^logout/', views.logout_view,name='logout'),

# API-based view for mobile or external apps
    path(r'^api/calculate/', views.api_calculate, name='api_calculate'),  # API endpoint for calculation
    path('', UserListCreateApiView.as_view(), name='api_user_list_create'),  # API endpoint for users
    path('<int:pk>/', UserRetrieveUpdateDestroyApiView.as_view(), name='api_user_detail'), # API endpoint to retrieve, update, delete user by username

]