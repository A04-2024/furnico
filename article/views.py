from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from article.forms import ArticleForm, CommentForm
from article.models import Article, Comment
from django.contrib.auth.decorators import user_passes_test, login_required

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

def show_article(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }

    return render(request, "article.html", context)

@user_passes_test(is_admin)
@login_required
def create_article(request):
    form = ArticleForm(request.POST or None, request.FILES or None)  # Include request.FILES

    if form.is_valid() and request.method == "POST":
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        return redirect('article:show_article')

    context = {'form': form}
    return render(request, 'create_article.html', context)

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()  # Retrieve all comments associated with this article

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article  # Link comment to the article
            comment.user = request.user  # Ensure the logged-in user is assigned as the comment author
            comment.save()  
            return redirect('article:article_detail', id=article.id)  # Redirect to avoid re-submitting form on refresh
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'article_detail.html', context)


@user_passes_test(is_admin)
@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)  

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('article:article_detail', id=article.id)

    context = {'form': form}
    return render(request, 'edit_article.html', context)

@user_passes_test(is_admin)
def delete_article(request, id):
    article = Article.objects.get(pk = id)
    article.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('article:show_article'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        article_id = comment.article.id  
        return redirect('article:article_detail', id=article_id)
    else:
        return redirect('article:article_detail', id=comment.article.id)