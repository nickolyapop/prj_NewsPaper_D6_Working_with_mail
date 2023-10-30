from django.urls import path, include
from .views import PostList, PostDetail, News, PostCreateView, PostUpdateView, PostDeleteView, PostCategoryView, \
    subscribe_to_category, unsubscribe_from_category

app_name = 'news'
urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='new_detail'),
    path('search/', News.as_view(), name='search'),
    path('new/create/', PostCreateView.as_view(), name='new_create'),
    path('new/update/<int:pk>/', PostUpdateView.as_view(), name='new_update'),
    path('new/delete/<int:pk>/', PostDeleteView.as_view(), name='new_delete'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
]
