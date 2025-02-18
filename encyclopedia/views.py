import markdown2 # type: ignore

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class FormRecherche(forms.Form):
    a_chercher = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}))

def index(request):
    if request.method == "POST":
        form_recu = FormRecherche(request.POST)
        if form_recu.is_valid():
            article_a_trouver = form_recu.cleaned_data["a_chercher"]
            liste_articles = []
            article_trouve = False
            for article in util.list_entries():
                if article_a_trouver.upper() == article.upper():
                    article_trouve = True
                    break
                elif article_a_trouver.upper() in article.upper():
                    liste_articles.append(article)
            if article_trouve:
                return render(request, "encyclopedia/article.html", {
                    "nom_article": article_a_trouver.capitalize(),
                    "contenu_article": markdown2.markdown(util.get_entry(article_a_trouver)),
                    "form_recherche": FormRecherche()
                })
            if len(liste_articles) > 0:
                return render(request, "encyclopedia/index.html", {
                    "titre": f"Pages correspondant a '{article_a_trouver}'",
                    "entries": liste_articles,
                    "form_recherche": form_recu
                })
            else:
                return render(request, "encyclopedia/erreur.html", {
                "msg_warning": f"Pas d'article contenant '{article_a_trouver}'.",
                "form_recherche": FormRecherche()
            })
    return render(request, "encyclopedia/index.html", {
        "titre": "Liste des pages du wiki",
        "entries": util.list_entries(),
        "form_recherche": FormRecherche()
    })

def vue_article(request, article):
    contenu_article = util.get_entry(article)
    if contenu_article:
        return render(request, "encyclopedia/article.html", {
            "nom_article": article.capitalize(),
            "contenu_article": markdown2.markdown(contenu_article),
            "form_recherche": FormRecherche()
        })
    else:
        return render(request, "encyclopedia/erreur.html", {
            "msg_erreur": f"Article '{article}' non trouvé.",
            "form_recherche": FormRecherche()
        })     
        



