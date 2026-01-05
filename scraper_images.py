import os
# Importation des outils pour le téléchargement massif des images
from scraper_utils import (
    extract_book_data, 
    get_books_urls_from_category, 
    get_all_categories_links, 
    download_image, 
    BASE_URL
)

def run_phase4():
    """
    Exécute la Phase 4 : Téléchargement de TOUTES les images de tous les livres.
    Crée le dossier d'images s'il n'existe pas, puis parcourt tout le site.
    Retourne le nombre total d'images téléchargées/vérifiées.
    """
    print("\n--- Phase 4 : Téléchargement de toutes les images du site ---")
    
    total_images = 0 # Compteur simple pour le total des images téléchargées
    
    # Vérification/Création du dossier de base pour les images
    images_dir = os.path.join("scraped_data", "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Récupération de toutes les catégories
    categories = get_all_categories_links(BASE_URL)
    print(f"{len(categories)} catégories trouvées.")
    
    # Double boucle (Catégories > Livres) pour le téléchargement
    for category in categories:
        print(f"\nTéléchargement images : {category['name']}...")
        book_urls = get_books_urls_from_category(category['url'])

        # initialisation du compteur pour la catégorie et reset a chaque catégorie débutée
        category_img_count = 0 
        for i, url in enumerate(book_urls, 1):
            print(f"  [{i}/{len(book_urls)}] Téléchargement...", end="\r")
            # On extrait les données pour avoir l'URL de l'image et l'UPC (nom du fichier)
            data = extract_book_data(url)
            if data:
                # Téléchargement de l'image (si pas déjà présente)
                if download_image(data['image_url'], data['category'], data['universal_product_code']):
                    category_img_count += 1
                    total_images += 1
                    
        print(f"\n  {category_img_count} images traitées pour {category['name']}")
        
    print(f"\n--- Fin de la Phase 4 : {total_images} images téléchargées au total ---")
    return total_images # On retourne le score final

