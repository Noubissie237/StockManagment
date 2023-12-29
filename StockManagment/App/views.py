from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import panier_cookie, data_cookie

# Create your views here.
def shop(request, *args, **kwargs):
    """Vue des produits"""

    produits = Produit.objects.all()

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'produits': produits,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']


    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/commande.html', context)

@login_required()
def update_article(request, *args, **kwargs):

    data = json.loads(request.body)
    produit_id = data['produit_id']
    action = data['action']
    
    produit = Produit.objects.get(id=produit_id)

    client = request.user.client

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action == "add":
        commande_article.quantite += 1
    
    if action == "remove":
        commande_article.quantite -=1

    commande_article.save()

    if commande_article.quantite <= 0:
        commande_article.delete()
    
    return JsonResponse("panier modifié", safe=False)


def commandeAnonyme(request, data):
    name = data['form']['name']
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']

    cookie_panier = panier_cookie(request)

    articles = cookie_panier['articles']
    client, created = Client.objects.get_or_create(
        email=email
    )

    client.name = name
    client.save()

    commande = Commande.objects.create(
        client=client
    )

    for article in articles:
        produit = Produit.objects.get(id=article['produit']['pk'])
        CommandeArticle.objects.create(
            produit=produit,
            commande=commande,
            quantite=article['quantite']
        )

        return client, commande


def traitement_commande(request, *args, **kwargs):

    data = json.loads(request.body)

    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = transaction_id

    if commande.get_panier_total == total:
        commande.complete = True

    commande.save()

    if commande.produit_physique:
        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse=data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )


    return JsonResponse("Traitement complet", safe=False)