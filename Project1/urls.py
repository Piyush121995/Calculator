
from django.contrib import admin
from django.conf.urls import url
from calculator import views
from django.urls import path
from django.views.generic.base import RedirectView  # Import RedirectView
from calculator.views  import UserListCreateApiView,UserRetrieveUpdateDestroyApiView,upload_file_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_page,name='login'),
    url(r'^cal/', views.calculate, name='calculator'),
    url(r'^signup/', views.sign_up,name='sign-up'),
    url(r'^signup/success/', views.signup_success,name='signup_success'),
    url(r'^logout/', views.logout_view,name='logout'),
    path('upload/', views.upload_file_view, name='upload'),
    
# API-based view for mobile or external apps
    path('',RedirectView.as_view(url='/login/', permanent=False), name='base_redirect'),
    path(r'^api/calculate/', views.api_calculate, name='api_calculate'),  # API endpoint for calculation
    path('', UserListCreateApiView.as_view(), name='api_user_list_create'),  # API endpoint for users
    path('<int:pk>/', UserRetrieveUpdateDestroyApiView.as_view(), name='api_user_detail'), # API endpoint to retrieve, update, delete user by username

]