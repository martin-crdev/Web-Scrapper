import datetime
import logging
logging.basicConfig(level=logging.INFO)
import subprocess #Nos permite manipular archivos de terminal

logger = logging.getLogger(__name__)
news_sites_uids = ["eltiempo", "elpais"]

def run():
    _extract()
    _transform()
    _load()

#Funcion para extraer la informacion 
def _extract():
    logger.info("Starting extract process") #Avisamos al usuario de lo que esta sucediendo
    for news_sites_uid in news_sites_uids: #Iteramos por cada uno de nuestros sitios
        now = datetime.datetime.now().strftime("%Y_%m_%d") #Obtenemos fecha de hoy
        out_file_name = "{news_site_uid}_{datetime}_articles.csv".format( #Creamos el nombre del archivo a guardar
        news_site_uid=news_sites_uid,
        datetime=now)
        subprocess.run(["py", "main.py", news_sites_uid], cwd="./extract") #ejecutamos main.py de la carpeta extract
        subprocess.run(["mv", out_file_name, "../transform/{news}_.csv".format(
                         news=news_sites_uid) #Los movemos a la carpeta transform
                        ], cwd="./extract") #Indicamos que el current workink directory sea extract
         

#Funcion para procesar la informacion
def _transform():
    logger.info("Starting transform process") #Avisamos al usuario lo que esta pasando
    for news_sites_uid in news_sites_uids: #Iteramos por cada uno de nuestros sitios
        dirty_data_filename = "{}_.csv".format(news_sites_uid) #Indicamos el nombre del archivo sin procesar
        clean_data_filename = "clean_{}".format(dirty_data_filename) #Nombre del archivo ya procesado
        subprocess.run(["py", "main.py", dirty_data_filename], cwd="./transform") #Mandamos el archivo a procesar
        subprocess.run(["rm", dirty_data_filename], cwd="./transform") #Borramos el archivo sin procesar
        subprocess.run(["mv", clean_data_filename, "../load/{}.csv".format(news_sites_uid)],
                        cwd="./transform") #Movemos el archivo ya procesado a la carpeta load

#Funcion para cargar los datos a una DB
def _load():
    logger.info("Starting load process") #Avisamos al usuario lo que esta pasando
    for news_sites_uid in news_sites_uids: #Iteramos por cada uno de nuestros sitios
        clean_data_filename = "{}.csv".format(news_sites_uid) #guardamos el nombre de nuestro archivo a cargar
        subprocess.run(["py", "main.py", clean_data_filename], cwd="./load") #Cargamos el archivo
        #subprocess.run(["rm", clean_data_filename], cwd="./load") #Eliminamos el archvivo

if __name__ == "__main__":
    run()