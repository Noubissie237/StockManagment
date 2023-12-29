from .models import *
import json

def panier_cookie(request):
    articles = []

    commande = {
        'get_panier_total':0,
        'get_panier_article':0,
        'produit_physique': True,
    }

    nombre_article = commande['get_panier_article']

    try:
        panier = json.loads(request.COOKIES.get('panier'))
        for obj in panier:

            nombre_article += panier[obj]['qte']

            produit = Produit.objects.get(id=obj)

            total = produit.price * panier[obj]['qte']

            commande['get_panier_article'] += panier[obj]['qte']

            commande['get_panier_total'] += total

            article = {
                'produit': {
                    'pk': produit.id,
                    'name': produit.name,
                    'price': produit.price,
                    'nombre': produit.nombre
                },
                'quantite': panier[obj]['qte'],
                'get_total': total

                }

            articles.append(article)

            if produit.digital == False:
                commande['produit_physique'] = True
                
    except:
        pass

    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return context


def data_cookie(request):

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        articles = commande.commandearticle_set.all()

        nombre_article = commande.get_panier_article

    else:

        cookie_panier = panier_cookie(request)
        articles = cookie_panier['articles']
        commande = cookie_panier['commande']
        nombre_article = cookie_panier['nombre_article']

    context = {
        'articles' : articles, 
        'commande': commande,
        'nombre_article': nombre_article
    }

    return context