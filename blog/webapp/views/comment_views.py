from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from webapp.forms import CommentForm
from webapp.models import Comment


class CommentView(ListView):
    template_name = 'comment/comment.html'
    context_object_name = 'comments'
    model = Comment
    ordering = '-created_at'
    paginate_by = 5
    paginate_orphans = 1


class CommentCreateView(CreateView):
    template_name = 'comment/comment_create.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('comment_view')


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_update.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('comment_view')


class CommentDeleteView(DeleteView):
    template_name = 'comment/comment_delete.html'
    model = Comment
    context_object_name = 'comment'
    success_url = reverse_lazy('comment_view')

