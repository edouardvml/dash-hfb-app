import os
import sys

def resource_path(relative_path):
    """ 
    Obtenir le chemin absolu vers la ressource, fonctionne avec PyInstaller 
    """
    try:
        base_path = sys._MEIPASS  # type: ignore # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
    except Exception:
        base_path = os.path.abspath(".") #Get absolute path from current repository
    return os.path.join(base_path, relative_path)