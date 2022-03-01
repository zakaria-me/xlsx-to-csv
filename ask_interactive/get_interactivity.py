from console import console
from rich.text import Text
from rich.markdown import Markdown
import CONSTANT
import xlsx_to_csv.xlsx_to_csv as xlsx_to_csv

def set_default_settings():
  skiprows = console.input(Markdown("# Entrez la valeur de la ligne où se trouve l'en-tête des colonnes de vos fichiers excel: "))
  if not skiprows.isdigit():
    console.print(Markdown("## Entrez une valeur numérique! Le programme s'achève."))
    console.input()
    exit()
  else:
    CONSTANT.SKIPROWS_DEFAULT = int(skiprows) -1
  pass

  CONSTANT.SHEET_NAME = xlsx_to_csv.process_sheet("vos fichiers excel")
 # sheet_name = input("Entrez le nom ou le numéro de la feuille du fichier excel a process pour tous les fichiers dans 'fichiers_xlsx': ")
 # if sheet_name.isdigit():
 #   CONSTANT.SHEET_NAME = int(sheet_name)
 # else:
 #   CONSTANT.SHEET_NAME = sheet_name

def default_settings():
  message_default_content = """
  Voulez-vous modifier:
- les valeurs par défaut de la feuille du fichier excel à convertir pour **TOUS** les fichiers dans 'fichier_xlsx' ? (par défaut cette valeur vaut 0)
- et la position de la ligne à partir de laquelle la conversion commencera ? (par défaut cette valeur vaut 1)
# Taper oui pour OUI. Taper non pour NON: """
  message_default = Markdown(message_default_content)
  answer = console.input(message_default)
  if answer == "oui":
    set_default_settings()

def is_interactive():
  message_interactif_content = """
# Voulez-vous lancer le programme en mode interactif ?
- Par défaut le programme prendra en compte **tous les fichiers .xlsx et .xls** contenus dans 'fichiers_excel'. 
- En outre, pour chaque fichier excel considéré, il convertira **TOUTES** les feuilles en .csv. 
- De plus, il capturera directement les en-têtes avec le nom des variables en première ligne.
# Taper oui pour OUI. Taper non pour NON: """
  message_interactif = Markdown(message_interactif_content)
  CONSTANT.IS_INTERACTIVE = console.input(message_interactif)
  if CONSTANT.IS_INTERACTIVE == "oui":
    CONSTANT.IS_INTERACTIVE = True
    console.rule("[bold red] Lancement du programme en mode interactif")
  else: 
    CONSTANT.IS_INTERACTIVE = False
    console.rule("[bold red] Lancement du programme en mode indépendant")
    default_settings()
