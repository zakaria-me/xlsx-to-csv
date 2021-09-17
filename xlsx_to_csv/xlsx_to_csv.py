
import os
import get_directory.destination_directories as dest_dir
import CONSTANT
import sys
import pandas as pd

def process_rows(file_name :str):
  answer = input("A quelle ligne se trouve l'en-tête contenant les noms des colonnes dans " + file_name + " ? ")  
  if answer.isdigit():
    answer = int(answer) - 1
    return answer

def process_sheet(file_name :str):
  print("Quelles feuilles de " + file_name + " voulez-vous convertir?\nTaper un numéro(la numérotation des feuilles commencent par 0) ou le nom exact de la feuille puis appuyer sur Entrée. Entrez 'q' pour quitter: ")  
  answer = []
  for value in sys.stdin:
    if 'q' == value.rstrip():
      break
    if value == "\n" and len(answer) == 0:
      print("Vous n'avez pas entré de valeur, la valeur de la feuille à traiter sera: " + str(CONSTANT.SHEET_NAME))
      return CONSTANT.SHEET_NAME
    value = value.strip()
    if value.isdigit():
      value = int(value)
    if value != "":
      answer.append(value)
  print(answer)
  return answer

def get_all_csv_files(directory :str, extension :str):
  list_files_name = []
  for file in os.listdir(dest_dir.get_csv_dir_path(directory)):
    if extension in file:
      # Ajouter le nom de fichier à la liste des fichiers ".csv"
      list_files_name.append(file)
  return list_files_name


def process_file_bool(file_name :str):
  answer = input("Voulez-vous process : " + file_name + " ?\n Taper oui pour OUI ou taper non pour NON: ")  
  if answer == "oui":
    print(file_name + " sera process.\n")
    return True 
  else:
    print(file_name + " ne sera pas process.\n")
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
          print("Le fichier " + csv_file_name + " existe déjà!\nCe fichier sera donc ignoré et pas converti.\n")
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
    print("Conversion de " + os.path.basename(file) + " en cours. Veuillez patienter... Bip bip bop!")
    read_file = pd.read_excel (file, sheet_name=sheet_name, skiprows=skiprows)
    print("Conversion de " + os.path.basename(file) + " terminée. Blop bip...")
    # Stocker le nom du futur fichier ".csv"
    # Le convertir en fichier ".csv"
    if type(sheet_name) is not list:
      csv_file = file.replace(".xlsx", ".csv")
      path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), str(sheet_name) + "_" + os.path.basename(csv_file))
      csv_files_name.append(path_to_csv_file)
      read_file.to_csv(path_to_csv_file, index = None, header=True, sep=';')
      pass
    else:
      for sheet in read_file:
        csv_file = file.replace(".xlsx", ".csv")
        path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), str(sheet) + "_" + os.path.basename(csv_file))
        csv_files_name.append(path_to_csv_file)
        read_file[sheet].to_csv(path_to_csv_file, index = None, header=True, sep=';')
  return csv_files_name