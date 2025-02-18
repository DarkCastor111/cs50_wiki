from django.urls import path

from . import views

app_name = "ns_encyclo"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:article>", views.vue_article, name="page_article"),
]
