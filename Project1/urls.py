
from django.contrib import admin
from django.conf.urls import url
from calculator import views
from django.urls import path
from django.views.generic.base import RedirectView  # Import RedirectView
from calculator.views import UserListCreateApiView, UserRetrieveUpdateDestroyApiView, upload_file_view, HistoryListView, \
    HistoryCRUDView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_page,name='login'),
    url(r'^cal/', views.calculate, name='calculator'),
    url(r'^signup/', views.sign_up,name='sign-up'),
    url(r'^signup/success/', views.signup_success,name='signup_success'),
    url(r'^logout/', views.logout_view,name='logout'),
    path('upload/', views.upload_file_view, name='upload'),
    
# API-based view for mobile or external apps
    path('', RedirectView.as_view(url='/login/', permanent=False), name='base_redirect'),
    path('api/calculate/', views.api_calculate, name='api_calculate'),  # API endpoint for calculation
    path('api/users/', UserListCreateApiView.as_view(), name='api_user_list_create'),  # Unique API endpoint for users
    path('api/users/<int:id>/', UserRetrieveUpdateDestroyApiView.as_view(), name='api_user_detail'),

    path('api/users/history/', HistoryListView.as_view(), name='api_user_history_list_create'),

    path('api/userss/<int:user>/history/<int:id>/',HistoryCRUDView.as_view(), name='api_user_history_CRUD')
]