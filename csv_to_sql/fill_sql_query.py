import re
def dec_or_disp(filename):
    if filename.find("TRDEC") != -1 or filename.find("OPRDEC") != -1: # or else DEC gets captured in TRDEC or OPRDEC
        if filename.find("DISP") != -1:
            return "DISP"
        else:
            return "DEC"
    if filename.find("DEC") != -1:
        return "DEC"
    if filename.find("DISP") != -1:
        return "DISP"
    else:
        return "NONE"

def get_echelle_admin(filename):
    if filename.find("ARR") != -1:
        return "ARR"
    if filename.find("DEP") != -1:
        return "DEP"
    if filename.find("EPCI") != -1:
        return "EPCI"
    if filename.find("EPT") != -1:
        return "EPT"
    if filename.find("METROPOLE") != -1:
        return "METROPOLE"
    if filename.find("REG") != -1:
        return "REG"
    if filename.find("COM") != -1:
        return "COM"
    else:
        return "NONE"

def get_pauvres(filename):
     return "Pauvres" if filename.find("Pauvres") != -1 else ""

def get_categorie_donnee(filename):
    if filename.find("ENSEMBLE") != -1:
        return "ENSEMBLE"
    categorie_pattern = re.compile(r'(.*)_(\d)_(.*)')
    categorie_pattern_trdeciles_10 = re.compile(r'(.*)_(\d\d)_(.*)') # if not present TRDECILES_10 doesn't get detected
    if len(categorie_pattern_trdeciles_10.split(filename)) >=3:
        categorie = categorie_pattern_trdeciles_10.split(filename)[1]
        categorie_number = categorie_pattern_trdeciles_10.split(filename)[2]
        return categorie + "_" + categorie_number
    if len(categorie_pattern.split(filename)) >= 3:
        categorie = categorie_pattern.split(filename)[1]
        categorie_number = categorie_pattern.split(filename)[2]
        return categorie + "_" + categorie_number
    return ""

def get_year(filename):
    year_pattern = re.compile(r'.*FILO(\d\d\d\d).*')
    if(len(year_pattern.split(filename)) > 1):
        return year_pattern.split(filename)[1]
    return "8888"

# in FILOSOFI, from 2012 to 2015 geo_year = data_year + 1
def get_geo_year_filosofi(year):
    year_int = int(year) + 1
    return str(year_int)

def get_nom_du_schema(filename):
    return "filosofi_" + get_year(filename)

def get_nom_de_la_table(filename):
    table_name = dec_or_disp(filename) + "_" + get_echelle_admin(filename) + "_"
    if get_pauvres(filename) != "":
        table_name += "Pauvres"  + "_"
    table_name += get_categorie_donnee(filename)
    return table_name.lower()