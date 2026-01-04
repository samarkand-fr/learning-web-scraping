import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

def extract_book_data(url):
    """
    Extrait les données détaillées d'un livre depuis sa page produit.
    Retourne un dictionnaire contenant les attributs du livre.
    """
    # On envoie une requête GET pour récupérer le contenu de la page
    response = requests.get(url)
    # On vérifie si la requête a réussi (code 200)
    if response.status_code != 200:
        print(f"Erreur : Impossible de charger la page (Code d'erreur : {response.status_code})")
        return {}   # return an empty dictionary

    # Page chargée avec succès. Début du 'parsing' (analyse du HTML).
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraction des données
    product_page_url = url

    # Extraction du titre
    title_tag = soup.find('h1')
    # Utilisation d'une valeur par défaut si le titre n'est pas trouvé
    title = title_tag.text.strip() if title_tag else "N/A"
    print(f"Titre du livre trouvé : '{title}'")

    # Extraction du tableau d'informations produit (UPC, prix, disponibilité)
    table = soup.find('table', class_='table-striped')
    rows = table.find_all('tr') if table else []
    
    # Valeurs par défaut pour éviter toute erreur si une donnée est absente
    upc = "N/A"
    price_excl_tax = "N/A"
    price_incl_tax = "N/A"
    number_available = "N/A"
    # Plutôt que de dépendre de la position des lignes dans le tableau, j’identifie chaque donnée à partir de son libellé.(plus robuste,plus maintenable)
    # Parcours de chaque ligne du tableau d'informations produit
    for row in rows:
        # Récupération des balises <th> (libellé) et <td> (valeur)
        th = row.find("th")
        td = row.find("td")
        # Si l'une des balises est absente, on passe à la ligne suivante
        if not th or not td:
            continue
        # Nettoyage du texte extrait
        header = th.text.strip()
        value = td.text.strip()
        # Association du libellé à la bonne variable
        match header:
            case "UPC":
                upc = value
            case "Price (excl. tax)":
                price_excl_tax = value
            case "Price (incl. tax)":
                price_incl_tax = value
            case "Availability":
                number_available = value
            case _:
                pass # Les autres champs du tableau ne nous intéressent pas

    # Extraction de la description du livre
    description_tag = soup.find('div', id='product_description')
    if description_tag:
        # find_next('p') cherche la première balise <p> après celle-ci
        product_description = description_tag.find_next('p').text
        #print(f"Description du livre : {product_description}")
    else:
        product_description = "Pas de description disponible."

    # Extraction de la catégorie via le fil d'Ariane (breadcrumb)
    breadcrumb = soup.find('ul', class_='breadcrumb')
    # Les liens sont : Home -> Books -> [Nom de la Catégorie] 
    # Vérifie si le breadcrumb existe
    if breadcrumb:
        links = breadcrumb.find_all('a')  # Récupère tous les liens <a>
        # La catégorie est située dans le 3ème lien (index 2)
        if len(links) >= 3:
            category = links[2].text.strip()
        else:
            category = "Inconnue"  # Valeur par défaut si pas de catégorie
    else:
        category = "Inconnue"  # Valeur par défaut si breadcrumb absent
    print(f" Catégorie : {category}")


    # Extraction de la note (rating) via la classe CSS
    # Retourne une liste : ['star-rating', 'Three']
    rating_tag = soup.find('p', class_='star-rating')
    if rating_tag:
        # extrais la valeur correspondant au nombre d’étoiles
        review_rating = rating_tag.get("class")[1]
    else:
        # Valeur par défaut si l'évaluation n'est pas trouvée
        review_rating = "Zero"


    # Recherche du conteneur HTML qui contient l'image du produit
    image_tag = soup.find('div', class_='item active')
    # Valeur par défaut si l'image n'est pas trouvée
    image_url = ""
    # Vérification de la présence du conteneur et de la balise <img> avant d’essayer d’accéder à son attribut.
    # Cette vérification empêche toute exception liée à un HTML incomplet.
    if image_tag and image_tag.find('img'):
        # Récupération du chemin relatif de l'image
        image_src = image_tag.find('img').get('src')

        # Construction de l'URL complète de l'image
        image_url = urljoin(url, image_src)


    return {
        "product_page_url": url,
        "universal_product_code": upc,
        "title": title,
        "price_including_tax": price_incl_tax,
        "price_excluding_tax": price_excl_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }

def get_books_urls_from_category(category_url):
    """
    Parcourt toutes les pages d'une catégorie et récupère les liens de chaque livre.
    """
    books_urls = []
    current_url = category_url
    page_count = 1  # Initialisation du compteur

    # ==== BOUCLE DE PARSING DES PAGES DE LA CATÉGORIE ====
    # on continue tant qu'il y a une URL courante
    while current_url:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Erreur : Impossible de charger la page (Code {response.status_code})")
            return books_urls  # return liste actuelle des URLs and il va arreter la boucle avec une safe exit  
            
        # Page chargée avec succès
        soup = BeautifulSoup(response.content, 'html.parser')
        # ======Extraction des liens sur la page actuelle ====== 
        # Sur une page catégorie, chaque livre est dans une balise <article class='product_pod'>
        book_tags = soup.find_all('article', class_='product_pod')
        print(f"=== {len(book_tags)} livres identifiés sur page {page_count } ===")
        # On parcourt chaque livre pour extraire son lien
        for tag in book_tags:
            # On récupère le lien 'href' dans le titre <h3> du livre
            link = tag.find('h3').find('a').get('href')
            # On construit l'URL complète du livre
            full_url = "http://books.toscrape.com/catalogue/" + link.replace("../", "")
            books_urls.append(full_url)

        # === Gestion de la pagination (bouton 'Next') ===
        # On cherche si une balise <li> avec la classe 'next' existe
        next_button = soup.find('li', class_='next')
        if next_button:
            next_link = next_button.find('a').get('href')
            # On met à jour l'URL courante pour la prochaine boucle
            current_url = urljoin(current_url, next_link)
            page_count += 1
            print(f"Page suivante trouvée. Passage à la page {page_count}")
        else:
            break  # Sortie immédiate car il n'y a plus de page suivante
            
    return books_urls

def get_all_categories_links(base_url):
    """
    Récupère la liste de toutes les catégories du site depuis la barre latérale.
    """
    categories = []
    # Requête vers la page d'accueil
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de charger la page (Code {response.status_code})")
        # la page inaccessible  donc le meilleur est de retourner une liste actuelle vide
        return categories
        
    # Parse HTML de la page d'accueil
    soup = BeautifulSoup(response.content, 'html.parser')
    # On cherche le conteneur des catégories dans la barre de navigation à gauche qui est dans une <ul class='nav-list'>
    nav_list = soup.find('ul', class_='nav-list').find('ul')
    # On récupère tous les liens de catégories
    links = nav_list.find_all('a')
    # On parcourt chaque lien pour extraire le nom et l'URL
    for link in links:
        category_name = link.text.strip()
        category_link = urljoin(base_url, link.get('href'))
        categories.append({"name": category_name, "url": category_link})
        print(f" {len(categories)} catégories trouvées au total.")

    return categories

def save_to_csv(data_list, filename):
    """
    Sauvegarde une liste de dictionnaires de données dans un fichier CSV.
    Les fichiers sont enregistrés dans 'scraped_data/csv'.
    """
    if not data_list:
        print(f"Annulation : Aucune donnée à écrire pour {filename}.")
        return
    
    # Chemin vers le dossier CSV
    csv_dir = os.path.join("scraped_data", "csv")
    
    # Création du dossier s'il n'existe pas
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        
    # Chemin complet du fichier
    file_path = os.path.join(csv_dir, filename)
    
    # Récupération des clés (les noms des colonnes) depuis le premier livre de la liste
    headers = list(data_list[0].keys())
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader() # Écrit la ligne d'en-tête
        writer.writerows(data_list) # Écrit toutes les lignes de données



