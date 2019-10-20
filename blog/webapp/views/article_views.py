from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleForm
from webapp.models import Article


class IndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    model = Article
    ordering = '-created_at'
    paginate_by = 5
    paginate_orphans = 1

class ArticleView(DetailView):
    template_name = 'article/article.html'
    pk_url_kwarg = 'pk'
    model = Article


class ArticleCreateView(CreateView):
    template_name = 'article/create.html'
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


