from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from articles.models import Article


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Article.objects.filter(status=Article.Status.PUBLISHED, author=self.request.user)
        drafts = Article.objects.filter(status=Article.Status.DRAFT, author=self.request.user)
        context["published"] = published
        context["drafts"] = drafts
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["photo", "bio"]
    template_name = "accounts/update_profile.html"


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "accounts/delete_profile.html"
    success_url = reverse_lazy("home")
