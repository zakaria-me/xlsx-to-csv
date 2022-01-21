# What is it?

This is a simple python script that reads Excel files and converts into csv and SQL create table statements. 
This was created as a tool to streamline data analysis processes inside a French local government office.
**NOTE**: As such, if the source code is written in English, all the terminal instructions are written in French. 

# How to use it
```bash
git clone git@github.com:zakaria-me/xlsx-to-csv.git
cd xlsx-to-csv/
python3 xlsx-to-csv.py
```
Place all your `xlsx` or `xls` files inside a directory named `fichiers_excel`. The program will read source files from this directory.
During conversion, it will create `fichiers_csv` and `fichiers_sql` which respectively hold `csv` and `sql` files.

Then follow everything that is prompted on your screen given that you are a French speaking fella'.

# LICENSE
GNU GPLv3, see [LICENSE](LICENSE)
