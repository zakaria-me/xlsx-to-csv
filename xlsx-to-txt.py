import pandas as pd
import os
 
  # Prendre en mémoire le chemin vers le répertoire courant
directory = os.getcwd()
  # Stocker tous les fichiers ".xlsx" du répertoire courant
xlsx_files_name = []
for file in os.listdir(directory):
  if ".xlsx" in file:
    # Ajouter le nom de fichier à la liste des fichiers ".xlsx"
    xlsx_files_name.append(file)

csv_files_name = []
for file in xlsx_files_name:
  # lire le fichier Excel
  read_file = pd.read_excel (file, sheet_name=0, skiprows=5)
  # Stocker le nom du futur fichier ".csv"
  csv_file = file.replace(".xlsx", "") + ".csv"
  csv_files_name.append(csv_file)
  # Le convertir en fichier ".csv"
  read_file.to_csv (csv_file, index = None, header=True, sep=';')

#read_file = pd.read_excel (xlsx_files_name[1], sheet_name=0, skiprows=5)
#read_file.to_csv (xlsx_files_name[1] + ".csv", index = None, header=True, sep=';')