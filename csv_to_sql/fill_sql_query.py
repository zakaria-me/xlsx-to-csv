import re
def dec_or_disp(filename):
    if filename.find("DEC") != -1:
        return "DEC"
    if filename.find("DISP") != -1:
        return "DISP"

def get_echelle_admin(filename):
    if filename.find("ARR") != -1:
        return "ARR"
    if filename.find("DEPT") != -1:
        return "DEPT"
    if filename.find("EPCI") != -1:
        return "EPCI"
    if filename.find("METROPOLE") != -1:
        return "METROPOLE"
    if filename.find("REG") != -1:
        return "REG"
    if filename.find("COM") != -1:
        return "COM"

def get_pauvres(filename):
     return "Pauvres" if filename.find("Pauvres") != -1 else ""

def get_categorie_donnee(filename):
    if filename.find("ENSEMBLE") != -1:
        return "ENSEMBLE"
    categorie_pattern = re.compile(r'(.*)_(\d)_(.*)')
    if len(categorie_pattern.split(filename)) >= 3:
        categorie = categorie_pattern.split(filename)[1]
        categorie_number = categorie_pattern.split(filename)[2]
        return categorie + "_" + categorie_number
    return ""

def get_year(filename):
    year_pattern = re.compile(r'.*(\d\d\d\d).*')
    return year_pattern.split(filename)[1]

def get_nom_du_schema(filename):
    return "filosofi_" + get_year(filename)

def get_nom_de_la_table(filename):
    table_name = dec_or_disp(filename) + "_" + get_echelle_admin(filename) + "_"
    if get_pauvres != "":
        table_name += "Pauvres"  + "_"
    table_name += get_categorie_donnee(filename)
    return table_name.lower()