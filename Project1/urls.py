
from django.contrib import admin
from django.conf.urls import url
from calculator import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_page,name='login'),
    url(r'^cal/', views.calculate, name='calculator'),
    url(r'^signup/', views.sign_up,name='sign-up'),
    url(r'^signup/success/', views.signup_success,name='signup_success'),

# API-based view for mobile or external apps
    url(r'^api/calculate/', views.api_calculate, name='api_calculate'),  # API endpoint for calculation
    url(r'^api/users/', views.UserListCreateApiView.as_view(), name='api_user_list_create'),  # API endpoint for users
    url(r'^api/users/(?P<username>[^/]+)/$', views.UserRetrieveUpdateDestroyApiView.as_view(), name='api_user_detail'), # API endpoint to retrieve, update, delete user by username

]