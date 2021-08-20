import requests
import bs4

from common import config

class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()["news_sites"][news_site_uid]
        self._queries = self._config["queries"]
        self._html = None
        self._url = url

        self._visit(url)

    #Funcion auxiliar que nos ayudara a obtener informacion del documento que acabamos de parsear
    def _select(self, query_string):
        return self._html.select(query_string)

    #Visitamos directamente la pagina con esta funcion
    def _visit(self, url):
        response = requests.get(url) #Solicitamos la pagina web

        response.raise_for_status() #Levanta un error si la solicitud sale mal


        self._html = bs4.BeautifulSoup(response.text, "html.parser")

#Declaramos la clase homepage que represenara la pagina principal de nuestra web, hereda de newspage
class HomePage(NewsPage): 
    def __init__(self, news_site_uid, url): #Recibe el id del sitio de noticias y un url
        super().__init__(news_site_uid, url) #inicializamos la super clase
        

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries["homepage_article_links"]):
            if link and link.has_attr("href"): #Conprobamos que tenga el atributo href 
                link_list.append(link) #Si es valido lo agragamos a la lista

        return set(link["href"] for link in link_list) #Regresamos la lista pero con el metodo set se eliminan los duplicados

class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    #Obtenemos el cuerpo y el titulo de la noticia heredando _select siendo extensiones de newspage
    @property
    def body(self):
        result = self._select(self._queries["article_body"])

        return result[0].text if len(result) else "" #Checamos si hay resultados en la lista, sino retorna un string vacio

    @property
    def title(self):
        result = self._select(self._queries["article_title"])

        return result[0].text if len(result) else ""

    @property
    def url(self):
        result = self._url
        return result if len(result) else ""
    