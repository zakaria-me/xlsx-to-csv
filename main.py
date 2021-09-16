import get_directory.get_current_directory as get_cwd
import ask_interactive.get_interactivity as get_inter
import get_directory.destination_directories as dest_dir
import xlsx_to_csv.xlsx_to_csv as xlsx_to_csv 
import csv_to_sql.csv_to_sql as csv_to_sql 

def main():
  # Prendre en mémoire le chemin vers le répertoire courant
  directory = get_cwd.get_current_directory() 
  # Ask for interactive or not ?
  get_inter.is_interactive()
  # Créer les dossiers où seront stockés les fichiers .csv et .sql
  dest_dir.create_destination_directories(directory)
  # Exporter les fichiers xlsx en csv
  xlsx_to_csv.xlsx_to_csv(directory)
  # Extraire les requetes sql des fichiers csv
  csv_to_sql.csv_to_sql(xlsx_to_csv.get_all_csv_files(directory, ".csv"), directory)
  # Pour éviter que l'invite de commande se referme directement aprés la fin du script
  input("L'éxecution est terminée.Appuyer sur Entrée pour quitter le programme...")

main()