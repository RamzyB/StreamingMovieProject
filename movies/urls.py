from django.urls import path, include
from . import views
from .views import RegisterAPI, LoginAPI
from knox import views as knox_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.MovieListView)

urlpatterns = [
    # path('movie/', views.MovieListView.as_view(),

    path('movie/', include(router.urls)),

    path('movie/<int:pk>', views.MovieDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorListView.as_view()),
    path('actors/<int:pk>', views.ActorDetailView.as_view()),

    path('register/', RegisterAPI.as_view(), name='register'),

    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_video, name='video'),
    path('', views.get_list_video, name='home'),

]
