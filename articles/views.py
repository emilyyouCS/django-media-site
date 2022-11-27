from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.core.mail import send_mail


from taggit.models import Tag
from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Article


class ArticleListView(ListView):
    context_object_name = "articles"
    template_name = "articles/article_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = Article.objects.filter(status=Article.Status.PUBLISHED)
        tag = None
        tag_slug = self.kwargs.get("tag_slug", None)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            return queryset.filter(tags__in=[tag])
        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = super().get_object()
        comments = article.comments.filter(active=True)
        form = CommentForm()
        context["comments"] = comments
        context["form"] = form
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "articles/article_create.html"
    fields = ["title", "body", "status", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "articles/article_update.html"
    fields = ["title", "body", "status", "tags"]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/article_delete.html"

    success_url = reverse_lazy("home")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


@require_POST
def post_comment(request, pk):
    article = get_object_or_404(Article, id=pk, status=Article.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
    return render(
        request,
        "articles/comment.html",
        {"article": article, "form": form, "comment": comment},
    )


def article_share(request, pk):

    article = get_object_or_404(Article, id=pk, status=Article.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{article.title}"
            message = (
                f"Read {article.title} at {article_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "articles/share.html", {"article": article, "form": form, "sent": sent}
    )


def article_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Article.published.annotate(
                search=SearchVector("title", "body"),
            ).filter(search=query)

        else:
            form = SearchForm()

    return render(
        request,
        "articles/search_results.html",
        {"form": form, "query": query, "results": results},
    )
