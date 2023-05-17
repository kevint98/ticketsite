from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('create-ticket/', views.createTicket, name='create-ticket'),
    path('ticket/<int:pk>', views.viewTicket, name='view-ticket'),
    path('chart/filter-options', views.get_filter_options,
         name='chart-filter-options'),
    path('chart/projects/<int:year>', views.get_projects_chart,
         name='chart-projects'),
]
