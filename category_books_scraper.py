import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from one_book_scraper import extract_book_data
import csv

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
        if response.status_code == 200:
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
#               # On met à jour l'URL courante pour la prochaine boucle
                current_url = urljoin(current_url, next_link)
                page_count += 1
                print(f"Page suivante trouvée. Passage à la page {page_count}")
            else:
                break  # Sortie immédiate car il n'y a plus de page suivante
        else:
            # Si le status_code n'est pas 200 (ex: 404)
            print(f"Echec du chargement de la page {page_count}")
            break  # On arrête tout si le site ne répond pas
            
    return books_urls

def save_category_to_csv(category_books_list, filename):
    """
    Sauvegarde la liste complète des livres de la catégorie dans un CSV.
    """
    headers = [
        "product_page_url", "universal_product_code", "title",
        "price_including_tax", "price_excluding_tax", "number_available",
        "product_description", "category", "review_rating", "image_url"
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(category_books_list) # On enregistre TOUS les livres de la catégorie
    print(f"\n Enregistrement de {len(category_books_list)} livres dans '{filename}'...")

# Point d'entrée du script
if __name__ == "__main__":
    # URL de la catégorie choisie (Food and Drink)
    category_url = "https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html"
    # On récupère d'abord tous les liens
    book_urls= get_books_urls_from_category(category_url)
    category_books = []
    total = len(book_urls)
    
    #=== Extraction des données de chaque livre ===
    # tracking de la progression avec un compteur
    for index, url in enumerate(book_urls, 1):
        data = extract_book_data(url)
        print(f"\n Livre {index} / {total} extrait.")
        if data:
            category_books.append(data)
        
    # On sauvegarde tout les livres de la catégorie dans un CSV
    if category_books:
        # On extrait le nom  et on le nettoie (ex: "Food and Drink") -> "food_and_drink"
        category_name = category_books[0]['category'].lower().replace(' ', '_')
        # On définit le nom du fichier CSV
        save_category_to_csv(category_books, f"category_{category_name}.csv")


print(f"Phase 2 terminée : category_{category_name}.csv créé avec succès.")