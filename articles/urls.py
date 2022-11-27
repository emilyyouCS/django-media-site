from django.urls import path
from . import views

urlpatterns = [
    path('',views.ArticleListView.as_view(), name="article_list"),
    path("search/", views.article_search, name="article_search"),
    path(
        "tag/<slug:tag_slug>/",
        views.ArticleListView.as_view(),
        name="article_list_by_tag",
    ),
    path("new/", views.ArticleCreateView.as_view(), name="article_create"),
    path(
        "<int:pk>", views.ArticleDetailView.as_view(), name="article_detail"
    ), 
    path("<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="article_update"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article_delete"),
    path("<int:pk>/comment/", views.post_comment, name="post_comment"),
    path("<int:pk>/share/", views.article_share, name="article_share"),
]
