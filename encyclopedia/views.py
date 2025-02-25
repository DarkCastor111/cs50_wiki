import markdown2 # type: ignore
from random import *

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class FormRecherche(forms.Form):
    a_chercher = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}))

class FormAjout(forms.Form):
    titre_article = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Nouvel article"}))
    corps_article = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': "Corps de l'article"}))

class FormMiseAJour(forms.Form):
    titre_article = forms.CharField(label="", widget=forms.HiddenInput())
    corps_article = forms.CharField(label="", widget=forms.Textarea())

def index(request):
    if request.method == "POST":
        form_recu = FormRecherche(request.POST)
        if form_recu.is_valid():
            article_a_trouver = form_recu.cleaned_data["a_chercher"]
            liste_articles = []
            for article in util.list_entries():
                if article_a_trouver.upper() == article.upper():
                    liste_articles.append(article)
                    break
                elif article_a_trouver.upper() in article.upper():
                    liste_articles.append(article)
            if len(liste_articles) == 1:
                return HttpResponseRedirect(f"article/{liste_articles[0]}")
                #return render(request, "encyclopedia/article.html", {
                #    "nom_article": liste_articles[0].capitalize(),
                #    "contenu_article": markdown2.markdown(util.get_entry(liste_articles[0])),
                #    "form_recherche": FormRecherche()
                #})
            elif len(liste_articles) > 1:
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
        form_transmis = FormMiseAJour(initial={
            "titre_article": article,
            "corps_article": contenu_article
        })
        return render(request, "encyclopedia/article.html", {
            "nom_article": article.capitalize(),
            "contenu_article": markdown2.markdown(contenu_article),
            "form_recherche": FormRecherche(),
            "form_maj": form_transmis
        })
    else:
        return render(request, "encyclopedia/erreur.html", {
            "msg_erreur": f"Article '{article}' non trouvé.",
            "form_recherche": FormRecherche()
        })


def vue_ajout_article(request):
    if request.method == "POST":
        form_recu = FormAjout(request.POST)
        if form_recu.is_valid():
            titre = form_recu.cleaned_data["titre_article"]
            corps = form_recu.cleaned_data["corps_article"]
            articles_existants = [s.upper() for s in util.list_entries()]
            if titre.upper() in articles_existants:
                return render(request, "encyclopedia/erreur.html", {
                    "msg_erreur": f"Article '{titre}' déjà existant.",
                    "form_recherche": FormRecherche()
                })
            else:
                with open(f"entries/{titre}.md", "w", encoding="utf-8") as fichier:
                    fichier.write(corps.strip())
                return HttpResponseRedirect(f"article/{titre}")
            
    return render(request, "encyclopedia/maj_article.html", {
        "titre": "Création nouvel article",
        "titre_article": "ajouter", 
        "form_maj": FormAjout()
    })

def vue_modif_article(request, article):
    if request.method == "POST":
        form_recu = FormAjout(request.POST)
        if form_recu.is_valid():
            titre = form_recu.cleaned_data["titre_article"]
            corps = form_recu.cleaned_data["corps_article"]
            with open(f"entries/{titre}.md", "w", encoding="utf-8") as fichier:
                fichier.write(corps.strip())
            return HttpResponseRedirect(f"/article/{titre}")
    # Recherche du contenu de l'article
    contenu_article = util.get_entry(article)
    # Valeurs initiales du formulaire de mise à jour
    form_maj = FormMiseAJour(initial={
        "titre_article": article,
        "corps_article": contenu_article
    })
    
    return render(request, "encyclopedia/maj_article.html", {
        "titre": "Mise à jour d'un article",
        "titre_article": article,
        "form_maj": form_maj
    })

def vue_article_hasard(request):
    liste_des_articles = util.list_entries()
    n = randint(0, len(liste_des_articles)-1)
    return HttpResponseRedirect(f"/article/{liste_des_articles[n]}")
            




