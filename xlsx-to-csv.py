from posixpath import join
import pandas as pd
import os
import subprocess

def get_all_xslx_files(directory :str, extension :str):
  list_files_name = []
  for file in os.listdir(get_xlsx_dir_path(directory)):
    if extension in file:
      # Si le fichier ".csv" correspondant au ".xlsx" existe déjà, pas besoin de le rajouter
      csv_file_name = file.replace(extension, ".csv")
      path_to_csv_file = os.path.join(get_csv_dir_path(directory), csv_file_name) 
      if not os.path.isfile(path_to_csv_file):
      # Ajouter le nom de fichier à la liste des fichiers ".xlsx"
        path_to_xlsx_file = os.path.join(get_xlsx_dir_path(directory), file)
        list_files_name.append(path_to_xlsx_file)
  return list_files_name

def get_all_csv_files(directory :str, extension :str):
  list_files_name = []
  for file in os.listdir(get_csv_dir_path(directory)):
    if extension in file:
      # Ajouter le nom de fichier à la liste des fichiers ".csv"
      list_files_name.append(file)
  return list_files_name

def xlsx_to_csv(directory :str):
  # Stocker tous les fichiers ".xlsx" du répertoire courant
  xlsx_files_name = get_all_xslx_files(directory, ".xlsx")
  # Stocker tous les fichiers ".csv" du répertoire courant
  csv_files_name = get_all_csv_files(directory, ".csv")
  for file in xlsx_files_name:
    # lire le fichier Excel
    read_file = pd.read_excel (file, sheet_name=["QP", "IRIS_2020", "COM_2020", "EPCI_2020"], skiprows=5)
    # Stocker le nom du futur fichier ".csv"
    # Le convertir en fichier ".csv"
    for sheet in read_file:
      csv_file = file.replace(".xlsx", ".csv")
      path_to_csv_file = os.path.join(get_csv_dir_path(directory), sheet + "_" + os.path.basename(csv_file))
      csv_files_name.append(path_to_csv_file)
      read_file[sheet].to_csv(path_to_csv_file, index = None, header=True, sep=';')
  return csv_files_name

def csv_to_sql(csv_files_name :list, directory :str):
  for file in csv_files_name:
    sql_file_name_to_create = file.replace("csv", "sql")
    path_to_sql_file = os.path.join(get_sql_dir_path(directory), sql_file_name_to_create)
    if not os.path.exists(path_to_sql_file):
      path_to_csv_file = os.path.join(get_csv_dir_path(directory), file)
      sql_file = open(path_to_sql_file, mode="a")
      print("Ecriture de " + sql_file_name_to_create + " en cours")
      subprocess.run(["csvsql.exe", "-ipostgresql", "-eUTF-8", path_to_csv_file], stdout=sql_file)
      sql_file.close()
      edit_sql_file(path_to_sql_file)
      print("Ecriture de " + sql_file_name_to_create + " terminée")

def edit_sql_file(path_to_sql_file :str):
  replace_double_quotes(path_to_sql_file)
  append_copy_statement_to_sql_file(path_to_sql_file)

def replace_double_quotes(path_to_sql_file :str):
  sql_file_read = open(path_to_sql_file, mode="r")
  data = sql_file_read.read()
  data = data.replace("\"", "")
  sql_file_read.close()
  sql_file_write = open(path_to_sql_file, mode="w")
  sql_file_write.write(data)
  sql_file_write.close()

def append_copy_statement_to_sql_file(path_to_sql_file):
  sql_file_append = open(path_to_sql_file, mode="a")
  print("-- NE PAS DECOMMENTER \n --\COPY 'nom_du_schema.nom_de_la_table' FROM 'chemin_d_acces_au_fichier_csv' WITH(FORMAT CSV, HEADER True, DELIMITER ';', ENCODING 'UTF-8')", file=sql_file_append) 
  sql_file_append.close()

def create_destination_directories(directory):
  sql_directory = get_sql_dir_path(directory) 
  csv_directory = get_csv_dir_path(directory) 
  if not os.path.exists(sql_directory):
    os.mkdir(sql_directory)
  if not os.path.exists(csv_directory):
    os.mkdir(csv_directory) 

def get_csv_dir_path(directory):
  path = os.path.join(directory, "fichiers_csv")
  return path

def get_sql_dir_path(directory):
  path = os.path.join(directory, "fichiers_sql")
  return path

def get_xlsx_dir_path(directory):
  path = os.path.join(directory, "fichiers_xlsx")
  return path

def main():
  # Prendre en mémoire le chemin vers le répertoire courant
  directory = os.getcwd()
  # Créer les dossiers où seront stockés les fichiers .csv et .sql
  create_destination_directories(directory)
  # Exporter les fichiers xlsx en csv
  xlsx_to_csv(directory)
  # Extraire les requetes sql des fichiers csv
  csv_to_sql(get_all_csv_files(directory, ".csv"), directory)

main()