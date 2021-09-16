
import os

def get_xlsx_dir_path(directory):
  path = os.path.join(directory, "fichiers_xlsx")
  return path

def get_csv_dir_path(directory):
  path = os.path.join(directory, "fichiers_csv")
  return path

def get_sql_dir_path(directory):
  path = os.path.join(directory, "fichiers_sql")
  return path

def create_destination_directories(directory):
  sql_directory = get_sql_dir_path(directory) 
  csv_directory = get_csv_dir_path(directory) 
  if not os.path.exists(sql_directory):
    os.mkdir(sql_directory)
  if not os.path.exists(csv_directory):
    os.mkdir(csv_directory) 