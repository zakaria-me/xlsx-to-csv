import re
from console import *
import os
import get_directory.destination_directories as dest_dir
import CONSTANT
import sys
import pandas as pd
from rich.progress import track

def process_rows(file_name :str):
  answer = console.input(Markdown(f"# A quelle ligne se trouve l'en-tête contenant les noms des colonnes dans {file_name} ?"))  
  if answer.isdigit():
    answer = int(answer) - 1
    return answer

def process_sheet(file_name :str):
  console.print(Markdown(f"""
# Quelles feuilles de {file_name} voulez-vous convertir?
- Taper un numéro(la numérotation des feuilles commencent par 0) ou le nom exact de la feuille puis appuyer sur Entrée.
- Appuyer seulement sur Entrée si vous voulez convertir toutes les feuilles.
- Entrez 'q' pour quitter: """))  
  answer = []
  for value in sys.stdin:
    if 'q' == value.rstrip():
      break
    if value == "\n" and len(answer) == 0:
      console.print(Markdown("# Vous n'avez pas entré de valeur, toutes les feuilles seront converties."))
      return CONSTANT.SHEET_NAME
    value = value.strip()
    if value.isdigit():
      value = int(value)
    if value != "":
      answer.append(value)
  console.print(answer)
  return answer

def get_all_csv_files(directory :str, extension :str):
  list_files_name = []
  for file in os.listdir(dest_dir.get_csv_dir_path(directory)):
    if extension in file:
      # Ajouter le nom de fichier à la liste des fichiers ".csv"
      list_files_name.append(file)
  return list_files_name


def process_file_bool(file_name :str):
  answer = console.input(Markdown(f"Voulez-vous convertir : {file_name}? Taper oui pour OUI ou taper non pour NON: "))  
  if answer == "oui":
    console.print(file_name + " sera converti.\n")
    return True 
  else:
    console.print(file_name + " ne sera pas converti.\n")
    return False 

def get_all_xslx_files(directory :str, extension :str):
  list_files_name = []
  for file in os.listdir(dest_dir.get_xlsx_dir_path(directory)):
    if CONSTANT.IS_INTERACTIVE and process_file_bool(file) or CONSTANT.IS_INTERACTIVE == False:
      if ".xls" in file and ".xlsx" not in file: 
        new_filename = file.replace(".xls", ".xlsx") 
        current_path = os.path.join(dest_dir.get_xlsx_dir_path(directory), file)
        new_path = os.path.join(dest_dir.get_xlsx_dir_path(directory), new_filename)
        os.rename(current_path, new_path)
        file = new_filename
      if extension in file:
        # Si le fichier ".csv" correspondant au ".xlsx" existe déjà, pas besoin de le rajouter
        # car la conversion xlsx prend relativement beaucoup de temps
        csv_file_name = file.replace(extension, ".csv")
        path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), csv_file_name) 
        if not os.path.isfile(path_to_csv_file):
        # Ajouter le nom de fichier à la liste des fichiers ".xlsx"
          path_to_xlsx_file = os.path.join(dest_dir.get_xlsx_dir_path(directory), file)
          list_files_name.append(path_to_xlsx_file)
        else:
          console.print(Markdown(f"# Le fichier {csv_file_name} existe déjà! Ce fichier sera donc ignoré et pas converti."))
  return list_files_name

def xlsx_to_csv(directory :str):
  # Stocker tous les fichiers ".xlsx" du répertoire courant
  xlsx_files_name = get_all_xslx_files(directory, ".xlsx")
  # Stocker tous les fichiers ".csv" du répertoire courant
  csv_files_name = get_all_csv_files(directory, ".csv")
  for file in xlsx_files_name:
    ######################################################################################
    # LES VALEURS A CHANGER SONT ICI
    # sheet_name : le nom de(s) ou le numero (la numerotation commence par zero) des feuille(s) excel a exporter pour le fichier excel considéré
    # skiprows : le nombre de lignes a sauter lors de l'export de csv a sql. 
    # Si on veut commencer l'export a partir de la ligne 8 du fichier excel on ecrira:
    #    skiprows=7 
    ######################################################################################
    skiprows = CONSTANT.SKIPROWS_DEFAULT 
    sheet_name = CONSTANT.SHEET_NAME 
    if CONSTANT.IS_INTERACTIVE:
      sheet_name = process_sheet(os.path.basename(file))
      skiprows = process_rows(os.path.basename(file))
    # lire le fichier Excel 
    console.print("Conversion de " + os.path.basename(file) + " en cours. Veuillez patienter...")
    read_file = ""
    try:
      read_file = pd.read_excel (file, sheet_name=sheet_name, skiprows=skiprows)
    except ValueError:
      read_file = pd.read_excel (file, sheet_name=sheet_name, skiprows=skiprows, engine='xlrd')
    excel_sheet_names = pd.ExcelFile(file).sheet_names
    console.print("\tConversion de " + os.path.basename(file) + " terminée.")
    # Stocker le nom du futur fichier ".csv"
    # Le convertir en fichier ".csv"
    if type(sheet_name) is not list and sheet_name != None:
      # pour bien nommer les feuilles csv
      this_sheet_name = ""
      if type(sheet) == int:
        this_sheet_name = excel_sheet_names[sheet]
      else:
        this_sheet_name = sheet_name
      csv_file = file.replace(".xlsx", ".csv")
      path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), str(this_sheet_name) + "_" + os.path.basename(csv_file))
      csv_files_name.append(path_to_csv_file)
      read_file.to_csv(path_to_csv_file, index = None, header=True, sep=';')
      pass
    else:
      for sheet in read_file:
        # pour bien nommer les feuilles csv
        this_sheet_name = ""
        if type(sheet) == int:
          this_sheet_name = excel_sheet_names[sheet]
        else:
          this_sheet_name = sheet
        csv_file = file.replace(".xlsx", ".csv")
        path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), str(this_sheet_name) + "_" + os.path.basename(csv_file))
        csv_files_name.append(path_to_csv_file)
        console.print("Conversion de " + str(sheet) + " en cours. Veuillez patienter...")
        read_file[sheet].to_csv(path_to_csv_file, index = None, header=True, sep=';')
        console.print("\tConversion de " + str(sheet) + " terminée.")
  return csv_files_name