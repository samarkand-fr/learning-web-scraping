from scraper_utils import extract_book_data, save_to_csv

def run_phase1():
    """
    Phase 1 : Extrait les données d'une seule page produit et les enregistre dans book.csv.
    """
    url = "http://books.toscrape.com/catalogue/wuthering-heights_307/index.html"
    
    # Extraction des données 
    data = extract_book_data(url)
    
    # Sauvegarde si l'extraction a réussi
    if data:
        save_to_csv([data], "book.csv")

if __name__ == "__main__":
    run_phase1()