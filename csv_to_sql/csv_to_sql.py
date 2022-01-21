import os
import subprocess
import get_directory.destination_directories as dest_dir

def append_update_geography_statement_to_file(path_to_sql_file: str):
  sql_file_append = open(path_to_sql_file, mode="a")
  print("""
ALTER TABLE 
	'nom_du_schema.nom_de_la_table'

RENAME 'nom de la colonne LIBGEO' TO LIBGEO_XXXX; --- Remplacer XXXX par l'annee de la geographie
""", file=sql_file_append) 
  sql_file_append.close()

def append_copy_statement_to_sql_file(path_to_sql_file :str):
  sql_file_append = open(path_to_sql_file, mode="a")
  print("COPY 'nom_du_schema.nom_de_la_table' FROM 'chemin_d_acces_au_fichier_csv' WITH(FORMAT CSV, HEADER True, DELIMITER ';', ENCODING 'UTF-8');", file=sql_file_append) 
  sql_file_append.close()

def replace_double_quotes(path_to_sql_file :str):
  sql_file_read = open(path_to_sql_file, mode="r")
  data = sql_file_read.read()
  data = data.replace("\"", "")
  sql_file_read.close()
  sql_file_write = open(path_to_sql_file, mode="w")
  sql_file_write.write(data)
  sql_file_write.close()

def add_drop_statement_to_sql_file(path_to_sql_file :str):
  sql_file_read = open(path_to_sql_file, mode="r")
  data = sql_file_read.read()
  # the + operator is not the most efficient, maybe try something else?
  data = "DROP TABLE IF EXISTS 'nom_du_schema.nom_de_la_table'; \n" + data
  sql_file_read.close()
  sql_file_write = open(path_to_sql_file, mode="w")
  sql_file_write.write(data)
  sql_file_write.close()
  pass

def edit_sql_file(path_to_sql_file :str):
  add_drop_statement_to_sql_file(path_to_sql_file)
  replace_double_quotes(path_to_sql_file)
  append_copy_statement_to_sql_file(path_to_sql_file)
  append_update_geography_statement_to_file(path_to_sql_file)

def csv_to_sql(csv_files_name :list, directory :str):
  for file in csv_files_name:
    sql_file_name_to_create = file.replace("csv", "sql")
    path_to_sql_file = os.path.join(dest_dir.get_sql_dir_path(directory), sql_file_name_to_create)
    if not os.path.exists(path_to_sql_file):
      path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), file)
      sql_file = open(path_to_sql_file, mode="a")
      print("Ecriture de " + sql_file_name_to_create + " en cours")
      subprocess.run(["csvsql.exe", "-ipostgresql", "-eUTF-8", path_to_csv_file], stdout=sql_file)
      sql_file.close()
      edit_sql_file(path_to_sql_file)
      print("Ecriture de " + sql_file_name_to_create + " terminée")