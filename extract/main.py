import argparse
import datetime
import csv
import logging #Modulo para imprimir en consola mas elegante que un print
logging.basicConfig(level=logging.INFO)
import re #Modulo de expresiones regulares

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config

logger = logging.getLogger(__name__) #Obtenemos una referencia a nueestro logger
#Validar diferentes tipos de patron para las urls
is_well_formed_link = re.compile(r"^https?://.+/.+$") #https://example.com/hello
is_root_path = re.compile(r"^/.+$") #/some-text


def _news_scraper(news_site_uid):
    host = config()["news_sites"][news_site_uid]["url"]

    logging.info("Beginning scraper for {}".format(host))
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links: #Recorremos cada uno de los articulos del homepage
        article = _fetch_article(news_site_uid, host, link) #Obtenemos el articulo

        if article:
            logger.info("Article fetched!!")
            articles.append(article)

    _save_articles(news_site_uid, articles)

#Funcion auxiliar para guardar la infor scrapeada
def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime("%Y_%m_%d") #Obtenemos fecha de hoy
    out_file_name = "{news_site_uid}_{datetime}_articles.csv".format( #Creamos el nombre del archivo a guardar
        news_site_uid=news_site_uid,
        datetime=now)
    
    #Generamos los headers de nuestro csv filtrando los datos, rechazando los que empiecen con _
    csv_headers = list(filter(lambda property: not property.startswith("_"), dir(articles[0])))

    #Guardamos nuestros articulos
    with open(out_file_name, mode = "w+", encoding="utf-8") as f: #Abrimos el archivo y si no existe lo crea
        writer = csv.writer(f) 
        writer.writerow(csv_headers)

        for article in articles:
            #row forma de determinar todos los valores adentro de nuestro objeto
            row = [str(getattr(article, prop)) for prop in csv_headers] #Nos aseguramos que se guarden todas las propiedades
            writer.writerow(row)



#Funcion para obtener el articulo
def _fetch_article(news_site_uid, host, link):
    logger.info("Start fetching article at {}".format(link))

    article = None
    #Al hacer peticiones html podemos tener problemas por eso es necesario usar try y except
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except: #(HTTPError, MaxRetryError) as e:
        logger.warning("Error while fechting the article", exc_info = False)

    #Si el articulo no tiene cuerpo imprimimos el error y no devuelve nada, si lo tiene lo retorna
    if article and not article.body:
        logger.warning("Invalid article. There is no body")
        return None
    return article

#Funcion para construir las urls
def _build_link(host, link):
    #Si tenemos una url completa simplemente regresamos el link
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link): #Si tenemos un url que empiece con / unimos el host con el link para tener la url completa
        return "{}{}".format(host, link)
    else:
        return "{}/{}".format(host=host, uri=link)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()["news_sites"].keys()) # asignamos de nuestra configuracion la llave de nuestro mapa
    parser.add_argument("news_site",
                         help = "The news site that want to scrape",
                         type = str,
                         choices = news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)