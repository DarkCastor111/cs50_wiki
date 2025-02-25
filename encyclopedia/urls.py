from django.urls import path

from . import views

app_name = "ns_encyclo"
urlpatterns = [
    path("", views.index, name="index"),
    path("ajouter", views.vue_ajout_article, name="page_ajout"),
    path("modifier/<str:article>", views.vue_modif_article, name="page_modif"),
    path("article/<str:article>", views.vue_article, name="page_article"),
    path("hasard", views.vue_article_hasard, name="page_hasard")
]
