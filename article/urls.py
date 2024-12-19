from django.urls import path
from article.views import show_article, create_article, article_detail, edit_article, delete_article, delete_comment, add_comment
from article.views import show_json, show_json_comment, create_article_flutter, create_comment_flutter, check_admin_status, delete_comment_flutter

app_name = 'article'

urlpatterns = [
    path('', show_article, name='show_article'),
    path('create-article', create_article, name='create_article'),
    path('<uuid:id>/', article_detail, name='article_detail'),
    path('edit-article/<uuid:id>', edit_article, name='edit_article'),
    path('delete/<uuid:id>', delete_article, name='delete_article'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('add-comment/<uuid:article_id>/', add_comment, name='add_comment'),
    path('json-article/', show_json, name='show_json'),
    path('json-article-comment/<uuid:article_id>/', show_json_comment, name='show_json_comment'),
    path('create-article-flutter/', create_article_flutter, name='create_article_flutter'),
    path('create-comment-flutter/<uuid:article_id>/', create_comment_flutter, name='create_comment_flutter'),
    path('check-admin-status/<str:username>/', check_admin_status, name="admin_status"),
    path('delete-comment-flutter/<int:comment_id>/', delete_comment_flutter, name="delete_comment_flutter")
]