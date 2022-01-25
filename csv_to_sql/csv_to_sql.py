import os
from textwrap import fill
import get_directory.destination_directories as dest_dir
import csv_to_sql.fill_sql_query as fill_sql_query
import csv, ast

def append_update_code_geography_statement_to_file(path_to_sql_file: str):
  sql_file_append = open(path_to_sql_file, mode="a")
  print("""
ALTER TABLE 
	'nom_du_schema.nom_de_la_table'

RENAME CODGEO TO CODGEO_XXXX; 
""", file=sql_file_append) 
  sql_file_append.close()

def append_update_geography_statement_to_file(path_to_sql_file: str):
  sql_file_append = open(path_to_sql_file, mode="a")
  print("""
ALTER TABLE 
	'nom_du_schema.nom_de_la_table'

RENAME LIBGEO TO LIBGEO_XXXX; 
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

def edit_sql_file(path_to_sql_file :str, filename :str, path_to_csv_file :str):
  add_drop_statement_to_sql_file(path_to_sql_file)
  replace_double_quotes(path_to_sql_file)
  append_copy_statement_to_sql_file(path_to_sql_file)
  append_update_geography_statement_to_file(path_to_sql_file)
  append_update_code_geography_statement_to_file(path_to_sql_file)
  # get nom du schema
  nom_du_schema = fill_sql_query.get_nom_du_schema(filename)
  # get nom de la table
  nom_de_la_table = fill_sql_query.get_nom_de_la_table(filename)
  # replace
  sql_file_read = open(path_to_sql_file, mode="r")
  data = sql_file_read.read()
  data = data.replace("'nom_du_schema.nom_de_la_table'", nom_du_schema + "." + nom_de_la_table) 
  data = data.replace("chemin_d_acces_au_fichier_csv", path_to_csv_file) 
  data = data.replace("XXXX", fill_sql_query.get_year(filename)) 
  sql_file_read.close()
  sql_file_write = open(path_to_sql_file, mode="w")
  sql_file_write.write(data)
  sql_file_write.close()

def write_sql_file(headers, type_list, sql_file_name_to_create, sql_file):
  statement = "\nCREATE TABLE 'nom_du_schema.nom_de_la_table' ("
  for i in range(len(headers)):
    statement = (statement + '\n\t' + '{} {}' + ',').format(headers[i], type_list[i])
  statement = statement[:-1] + '\n);\n'
  sql_file.write(statement)

def guess_data_type(val, current_type):
  try:
      # Evaluates numbers to an appropriate type, and strings an error
      t = ast.literal_eval(val)
  except ValueError:
      return 'VARCHAR'
  except SyntaxError:
      return 'VARCHAR'
  if type(t) in [int, float]:
      if (type(t) in [int]) and current_type not in ['DECIMAL', 'VARCHAR']:
        return 'NUMERIC'
      if type(t) is float and current_type not in ['VARCHAR']:
        return 'DECIMAL'
  else:
      return 'VARCHAR'

def analyze_csv(path_to_csv_file, sql_file_name_to_create, sql_file):
  f = open(path_to_csv_file, 'r')
  reader = csv.reader(f, delimiter=';')
  # Declare variable beforehand to pass them by reference
  longest, headers, type_list = [], [], []
  for row in reader:
    if len(headers) == 0:
      headers = row
      for col in row:
        longest.append(0)
        type_list.append('')
    else:
      for i in range(len(row)):
        # NA is the csv null value
        if type_list[i] == 'VARCHAR' or row[i] == '':
          pass
        else:
          var_type = guess_data_type(row[i], type_list[i])
          type_list[i] = var_type
  f.close()
  write_sql_file(headers, type_list, sql_file_name_to_create, sql_file)

def csv_to_sql(csv_files_name :list, directory :str):
  for file in csv_files_name:
    sql_file_name_to_create = file.replace("csv", "sql")
    path_to_sql_file = os.path.join(dest_dir.get_sql_dir_path(directory), sql_file_name_to_create)
    if not os.path.exists(path_to_sql_file):
      path_to_csv_file = os.path.join(dest_dir.get_csv_dir_path(directory), file)
      sql_file = open(path_to_sql_file, mode="a")
      print("Ecriture de " + sql_file_name_to_create + " en cours")
      analyze_csv(path_to_csv_file, sql_file_name_to_create, sql_file)
      sql_file.close()
      edit_sql_file(path_to_sql_file, sql_file_name_to_create, path_to_csv_file)
      print("Ecriture de " + sql_file_name_to_create + " terminée")