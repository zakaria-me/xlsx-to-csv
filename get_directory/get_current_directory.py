import os

def input_dir_not_valid(directory):
  if directory == "":
    return 1
  try: 
    # Si le repertoire ne contient pas fichiers_xlsx
    for dir in os.listdir(directory):
      if dir == "fichiers_xlsx":
        return 0
    return 3
  except:
  # Si le repertoire n'existe pas
    return 2

def get_current_directory():
  message = "Quel est le chemin amenant au répertoire d'où vous lancez le programme ? "
  directory = input(message)
  validity_of_dir_name = input_dir_not_valid(directory)
  while validity_of_dir_name > 0:
    if validity_of_dir_name == 1: 
      directory = input("Le chemin que vous avez spécifié n'est pas valide. Retentez. " + message)
    elif validity_of_dir_name == 2:
      directory = input("Le répertoire que vous avez spécifié n'existe pas. Retentez. " + message)
    elif validity_of_dir_name == 3:
      directory = input("Ce répertoire ne contient pas le fichier_xlsx! Retentez. " + message)
    validity_of_dir_name = input_dir_not_valid(directory)
  return directory