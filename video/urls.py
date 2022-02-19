from django.urls import path
from video import views

app_name = 'video'

urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('video/index/', views.IndexView.as_view(), name='index'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('video/new/', views.CreatePostView.as_view(), name='post_new'),
    path('video/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('video/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('video/login/', views.Login.as_view(), name='login'),
    path('video/logout/', views.Logout.as_view(), name='logout'),
    path('video/signup/', views.SignUp.as_view(), name='signup'),
    path('video/add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('video/category/<str:category>/', views.CategoryView, name='category'),
    path('search', views.search, name='search'),
]
