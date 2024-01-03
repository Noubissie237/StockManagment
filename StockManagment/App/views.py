from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json, requests
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import panier_cookie, data_cookie, getDataFromApi
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def traitement_commande(request, *args, **kwargs):

    data = json.loads(request.body)


    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = data["payment_info"]["transaction_id"]

    commande.total_trans = data['payment_info']['total']

    if commande.get_panier_total == total:
        commande.complete = True
        commande.status = data['payment_info']['status']

    else:
        commande.status = "REFUSED"
        commande.save()
        return JsonResponse("Attention!!! Traitement Refuse Fraude detecte!", safe=False)

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'shop/index.html', context={'name' : request.user.username})
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:

        res = getDataFromApi(request)
        print(res)
        form = LoginForm()
        
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')

