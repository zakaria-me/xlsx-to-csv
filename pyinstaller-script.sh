cd ../exec
pyinstaller -F --clean -n convertisseur ../src/main.py
cp dist/convertisseur.exe R:/Traitements/263\ -\ Outil\ creation\ fichiers\ CSV\ en\ UTF8\ et\ requete\ SQL/xlsx_to_csv/exec/dist
cd R:/Traitements/263\ -\ Outil\ creation\ fichiers\ CSV\ en\ UTF8\ et\ requete\ SQL/xlsx_to_csv/src
git pull origin master
cd -