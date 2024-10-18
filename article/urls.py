from django.urls import path
from article.views import show_article, create_article, article_detail, edit_article, delete_article

app_name = 'article'

urlpatterns = [
    path('', show_article, name='show_article'),
    path('create-article', create_article, name='create_article'),
    path('<uuid:id>/', article_detail, name='article_detail'),
    path('edit-article/<uuid:id>', edit_article, name='edit_article'),
    path('delete/<uuid:id>', delete_article, name='delete_article'),
]