from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Article, Comment, STATUS_ACTIVE


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at', 'status']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 10:
            raise ValidationError('This field value should be more than 10 symbols long.',
                                  code='too_short')
        return title

    def clean(self):
        super().clean()
        if self.cleaned_data.get('text') == self.cleaned_data.get('title'):
            raise ValidationError('Article text should not duplicate article title',
                                  code='title_text_duplicate')
        return self.cleaned_data.get('text')


class CommentForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['article'].queryset = Article.objects.filter(status=STATUS_ACTIVE)

    # article = forms.ModelChoiceField(queryset=Article.objects.filter(status=STATUS_ACTIVE), label='Статья')

    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label="По тексту")
    in_title = forms.BooleanField(initial=True, required=False, label="В заголовке")
    in_text = forms.BooleanField(initial=True, required=False, label="В тексте")
    in_tags = forms.BooleanField(initial=True, required=False, label="В тегах")
    in_comment_text = forms.BooleanField(initial=False, required=False, label="В комментариях")

    author = forms.CharField(max_length=100, required=False, label="По автору")
    article_author = forms.BooleanField(initial=True, required=False, label="Статьи")
    comment_author = forms.BooleanField(initial=False, required=False, label="Комментария")

    def clean(self):
        super().clean()
        data = self.cleaned_data
        text = data.get('text')
        author = data.get('author')
        if not (text or author):
            raise ValidationError('No search text or author provided',
                                  code='text_and_author_empty')
        errors = []
        if text:
            in_title = data.get('in_title')
            in_text = data.get('in_text')
            in_tags = data.get('in_tags')
            in_comment_text = data.get('in_comment_text')
            if not (in_title or in_text or in_tags or in_comment_text):
                errors.append(ValidationError(
                    'One of the following checkboxes should be checked: In title, In text, In tags, In comment text',
                    code='text_search_criteria_empty'
                ))
        if author:
            article_author = data.get('article_author')
            comment_author = data.get('comment_author')
            if not (article_author or comment_author):
                errors.append(ValidationError(
                    'One of the following checkboxes should be checked: Article Author, Comment Author',
                    code='author_search_criteria_empty'
                ))
        if errors:
            raise ValidationError(errors)
        return data