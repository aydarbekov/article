from django.urls import path
from accounts.views import login_view, logout_view

from webapp.views import IndexView, ArticleView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, CommentView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('comment/', CommentView.as_view(), name='comment_view'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]

app_name = 'webapp'