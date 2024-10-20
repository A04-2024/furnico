from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from article.forms import ArticleForm, CommentForm
from article.models import Article, Comment

def show_article(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }

    return render(request, "article.html", context)

def create_article(request):
    form = ArticleForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('article:show_article')

    context = {'form': form}
    return render(request, "create_article.html", context)

def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    comments = article.comments.all()
    
    # Handle comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article:article_detail', id=article.id)
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'article_detail.html', context)

def edit_article(request, id):
    article = Article.objects.get(pk = id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('article:show_article'))

    context = {'form': form}
    return render(request, "edit_article.html", context)

def delete_article(request, id):
    article = Article.objects.get(pk = id)
    article.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('article:show_article'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article_id = comment.article.id  # Get the related article ID before deleting
    comment.delete()
    return redirect('article:article_detail', id=article_id)


# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
    
#     # Allow only the comment author or a superuser to delete the comment
#     if request.user == comment.author or request.user.is_superuser:
#         article_id = comment.article.id
#         comment.delete()
#         return redirect('article:article_detail', id=article_id)
#     else:
#         return redirect('article:article_detail', id=comment.article.id)
