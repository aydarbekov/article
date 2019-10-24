from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleForm, SimpleSearchForm
from webapp.models import Article, Tag


class IndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    model = Article
    ordering = '-created_at'
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(tags__name__iexact=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ArticleView(DetailView):
    template_name = 'article/article.html'
    pk_url_kwarg = 'pk'
    model = Article


class ArticleCreateView(CreateView):
    template_name = 'article/create.html'
    model = Article
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.parser()
        return redirect(self.get_success_url())

    def parser(self):
        tags = self.request.POST.get('tags')
        tag_list = tags.split(',')
        for tag in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(tag)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.parser()
        return redirect(self.get_success_url())

    def parser(self):
        tags = self.request.POST.get('tags')
        tag_list = tags.split(',')
        for tag in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.object.tags.clear()
            self.object.tags.add(tag)

class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('webapp:index')


