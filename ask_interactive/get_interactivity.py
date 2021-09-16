
import CONSTANT

def set_default_settings():
  skiprows = input("Entrez la valeur de la ligne où se trouve l'en-tête des colonnes de vos fichiers excel: ")
  if not skiprows.isdigit():
    print("Entrez une valeur numérique! Le programme s'achève.\n")
    exit()
  else:
    CONSTANT.SKIPROWS_DEFAULT = skiprows -1
  pass

  sheet_name = input("Entrez le nom ou le numéro de la feuille du fichier excel a process pour tous les fichiers dans 'fichiers_xlsx': ")
  if sheet_name.isdigit():
    CONSTANT.SHEET_NAME = int(sheet_name)
  else:
    CONSTANT.SHEET_NAME = sheet_name

def default_settings():
  message_default = "Voulez-vous modifier les valeurs par défaut de la feuille du fichier excel a process pour TOUS les fichiers dans 'fichier_xlsx' (par défaut cette valeur vaut 0) et la position de la ligne à partir de laquelle le process commencera (par défaut cette valeur vaut 6)?\nTaper oui pour OUI. Taper non pour NON: "
  answer = input(message_default)
  if answer == "oui":
    set_default_settings()

def is_interactive():
  message_interactif = "Voulez-vous lancer le programme en mode interactif ?\n" + "Par défaut le programme prendra en compte tous les fichiers .xlsx contenus dans 'fichiers_excel'. En outre, pour chaque fichier excel considéré, il ne convertira que la première feuille en .csv." + " De plus, il sautera par défaut les 5 premières lignes de la feuille afin de capturer directement les en-têtes avec le nom des variables.\n"  + "Taper oui pour OUI. Taper non pour NON: "
  CONSTANT.IS_INTERACTIVE = input(message_interactif)
  if CONSTANT.IS_INTERACTIVE == "oui":
    CONSTANT.IS_INTERACTIVE = True
    print("--- Lancement du programme en mode interactif ---\n")
  else: 
    CONSTANT.IS_INTERACTIVE = False
    print("--- Lancement du programme en mode indépendant ---\n")
    default_settings()
