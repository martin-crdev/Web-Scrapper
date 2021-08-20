import yaml 

# Variable global nos servira para cachear la info, 
# para no tener que leer a disco cada que queramos utilizar la configuracion
__config = None

def config():
    global __config #Declaramos como variable global para poder acceder a ella en cualquier lado 
    if not __config: #Si no tenemos la configuracion la cargamos
        with open("config.yaml", mode="r") as f: #Abrimos nuestro archivo en modo de lectura
            __config = yaml.safe_load(f) #cargamos el archivo 

    return __config # Si ya cargamos la configuracion simplemente retornara, 
                    # la variable para no estar cargado incesariamente la configuracion