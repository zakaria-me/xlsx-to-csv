import os
from console import console
from console import base_style 
from rich.markdown import Markdown

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
  message_content = "# Quel est le chemin amenant au répertoire où se trouve 'fichiers_xls' ? "
  message = Markdown(message_content, justify="center", style=base_style)
  directory = console.input(message)
  validity_of_dir_name = input_dir_not_valid(directory)
  while validity_of_dir_name > 0:
    if validity_of_dir_name == 1: 
      console.print(Markdown("## Le chemin que vous avez spécifié n'est pas valide. Retentez. "))
      directory = console.input(message)
    elif validity_of_dir_name == 2:
      console.print(Markdown("## Le répertoire que vous avez spécifié n'existe pas. Retentez. "))
      directory = console.input(message)
    elif validity_of_dir_name == 3:
      console.print(Markdown("## Ce répertoire ne contient pas le fichier_xlsx! Retentez. "))
      directory = console.input(message)
    validity_of_dir_name = input_dir_not_valid(directory)
  return directory