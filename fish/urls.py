from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('home/', views.home, name = 'home'),
    path('fish_list/', views.fish_list, name = 'fish_list'),
    path('fish_details/<int:id>/', views.fish_details, name = 'fish_details'),
    path('recommend/<int:h_id>/<int:id>', views.recommend, name = 'recommend'),
    path('profile/', views.profile, name = 'profile'),
    path('save-request/<int:h_id>/<int:fish_id>/', views.save_and_req, name='save_and_req'),
    path('request-log/', views.request_log, name = 'request_log'),
    path('request-cancel/', views.request_cancel, name = 'request_cancel'),
    path('admin_dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('approve/<int:id>/', views.approve, name='approve'),
    path('add_fish/', views.add_fish, name='add_fish'),
    path('edit_fish/<int:id>', views.edit_fish, name='edit_fish'),
    path('user_profiles/', views.user_profiles, name='user_profiles'),
    path('user_activation/<int:id>', views.user_activation, name='user_activation')
]