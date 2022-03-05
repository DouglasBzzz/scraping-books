import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


url = "https://www.bookdepository.com/top-new-releases"
pagina = requests.get(url)
soup = BeautifulSoup(pagina.content, "html.parser")
livros = soup.find_all("div", class_ = "book-item")

print(livros[0])

"""
por exemplo, se quisessemos serializar algo mais pratico... como as informacoes de autor, como fariamos? 
assim... 
"""

titulo_livro = livros[1].find("meta", {"itemprop":"name"}).get("content")
#print(titulo_livro)
autor_livro = livros[1].find("p", class_ = "author").find("a").text
formato_livro = livros[1].find("p", class_= "format").text
data_publicacao = livros[1].find("p", class_= "published").text
isbn_livro = livros[1].find("a", class_= "btn btn-sm btn-primary add-to-basket").get("data-isbn")
moeda_livro = livros[1].find("a", class_= "btn btn-sm btn-primary add-to-basket").get("data-currency")
preco_livro = livros[1].find("a", class_= "btn btn-sm btn-primary add-to-basket").get("data-price")

print("--------------")
print("dados do livro: ")
print(autor_livro)
print(formato_livro)
print(data_publicacao)
print(isbn_livro)
print(moeda_livro)
print(preco_livro)

"""
Mas tem um jeito mais fácil de fazer as coisas, e aninhar os resultados... listas... dicionários :D 
"""

dicionario_de_livros = {
    "titulo":[],
    "autor": [],
    "formato": [],
    "data_publicao": [],
    "isbn": [],
    "moeda": [],
    "valor": [],
    "data": []
}

for livro in livros:
    dicionario_de_livros["titulo"].append(livro.find("meta", {"itemprop": "name"}).get("content"))
    dicionario_de_livros["autor"].append(livro.find("p", class_="author").find("a").text)
    dicionario_de_livros["formato"].append(livro.find("p", class_="format").text)
    dicionario_de_livros["data_publicao"].append(livro.find("p", class_="published").text)
    dicionario_de_livros["isbn"].append(livro.find("a", class_="btn btn-sm btn-primary add-to-basket").get("data-isbn"))
    dicionario_de_livros["moeda"].append(livro.find("a", class_="btn btn-sm btn-primary add-to-basket").get("data-currency"))
    dicionario_de_livros["valor"].append(livro.find("a", class_="btn btn-sm btn-primary add-to-basket").get("data-price"))
    dicionario_de_livros["data"].append(datetime.date.today())

"""
por fim... após termos feito o mapeamento... vamos plotar um DATAFRAME do pandas... um baita formato tabular para
manipularmos registros.. :D 
"""

df = pd.DataFrame.from_dict(dicionario_de_livros)
print(df)

"""
criar lógica para colocar esse cara em arquivo CSV tbm...
"""

#setup
username = "***"
host = "***"
database = "***"
password = "***"
#fim_do_setup

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")
if df.to_sql(con=engine, name="repositorio-livros",if_exists="append", index=False):
    print("deu boa no banco....")
else:
    print("deu pau, debuga pra ver....")
