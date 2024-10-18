from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from article.forms import ArticleForm
from article.models import Article

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
    article = get_object_or_404(Article, pk=id)  # Fetch the article by UUID
    context = {'article': article}
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