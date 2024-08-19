import os
import re
import sqlite3
import glob
from time import sleep
from shutil import copyfile

def lista_mayusculas():
    alfabeto_mayus = []
    for c in range(65,91):
        letra = chr(c)+":"
        alfabeto_mayus.append(letra)
    return alfabeto_mayus



def ruta_bd():
   usuario = os.getlogin()
   ruta = "\\Users\\" + usuario + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
   for c in lista_mayusculas():
       if os.path.exists(c+ruta):
           ruta = c+ruta
           print(ruta)
           return ruta

def ruta_txt():
    usuario = os.getlogin()
    ruta = "\\Users\\" + usuario + "\\OneDrive\\Escritorio\\"
    if os.path.exists(ruta):
        return ruta
    else:
        print(f"No existe la ruta {ruta}"
              f"\ncompuerbe correctamente la direccion")


def archivo(nombre_archivo):
    txt = open(ruta_txt() + nombre_archivo, "w", encoding="utf-8")
    print("Txt creado")
    return txt


def ruta_steam(archivo):
   archivo.write("\n")
   archivo.write("JUEGOS INSTALADOS EN STEAM:\n")
   ruta = "\\Program Files (x86)\\Steam\\steamapps\\common\\"
   games = []
   for c in lista_mayusculas():
       if os.path.exists(c+ruta):
           steam_path = c+ruta

           steam_path = steam_path+"*"
           games_paths = glob.glob(steam_path)
           games_paths.sort(key=len,reverse=True)
           for gp in games_paths:
                games.append(gp.split("\\")[-1])
           if games:
               archivo.write(", ".join(games))

def historialChrome():
    ChromeOpen = True
    rutaBD = ruta_bd()

    while ChromeOpen == True:
        try:
            temp_history = rutaBD + ".temp"
            copyfile(rutaBD,temp_history)
            connection = sqlite3.connect(temp_history)
            cursor = connection.cursor()
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
            urls = cursor.fetchall()
            connection.close()
            print("Base de Datos Capurada Exitosamente!")
            ChromeOpen = False

        except sqlite3.OperationalError:
            print("La Base de Datos esta abierta...")
            sleep(2)
    return urls


def perfiles_twitter(archivo, historialChrome):
    archivo.write("\n\n")
    archivo.write("PERFILES VISITADOS DE TWITTER/X:\n\n")
    for c in historialChrome:
        results = re.findall("https://x.com/[A-Za-z0-9]+$",c[2])
        nombres = re.findall("https://x.com/([A-Za-z0-9]+)$",c[2])
        if results and results[0] not in ["https://x.com/home","https://x.com/notifications","https://x.com/messages"] and nombres and nombres[0] not in ["https://x.com/home","https://x.com/notifications","https://x.com/messages"]:
            archivo.write(nombres[0]+"\n")
            archivo.write(results[0]+"\n")
            archivo.write("\n")
    print("Perfiles Capturados en el txt correctamente")


def perfiles_instagram(archivo, historialChrome):
    link_no_requeridos= ["https://www.instagram.com/stories","https://www.instagram.com/p","https://www.instagram.com/direct", "https://www.instagram.com/accounts"]
    archivo.write("\n")
    archivo.write("PERFILES VISITADOS DE INSTAGRAM:\n\n")
    for c in historialChrome:
        results = re.findall("https://www.instagram.com/[A-Za-z0-9_.%-]+",c[2])
        nombres = re.findall("https://www.instagram.com/([A-Za-z0-9_.%-]+)",c[2])
        if results and results[0] not in link_no_requeridos:
            archivo.write(f"{nombres[0]}: \n{results[0]}\n")
            archivo.write("\n")
    print("Perfiles Capturados en el txt correctamente")





def canales_youtube(archivo, historialChrome):
    archivo.write("CANALES VISITADOS DE YOUTUBE:\n\n")
    contador = 0
    for c in historialChrome:
        if contador >=10:
            break
        url = c[2]  # Suponiendo que c[2] contiene la URL que queremos verificar
        results = re.findall(r"https://www.youtube.com/(?:@)?([A-Za-z0-9_\-]+)$", url)
        if results:
            nombre_canal = results[0]
            archivo.write(f"{contador + 1}. {nombre_canal}\n{url}\n\n")
            contador+=1
    print("Canales Capturados en el txt correctamente")




def compras_en_amazon(archivo, historialChrome):
    archivo.write("Busqueda reciente de Amazon:\n")
    link_no_requeridos = [
        "gp", "vender-en-amazon", "sspa", "s/ref", "events", "primeday",
        "deals", "cart","s","b", "ap", "dp", "your-orders", "b", "ref=sr_1_",
        "ref=sr_2_", "ref=sr_3_", "ref=sr_4_", "ref=sr_5_", "ref=sr_6_",
        "ref=sr_7_", "ref=sr_8_", "ref=sr_9_", "ref=sr_10_"]
    for c in historialChrome[:10]:
        resultados = re.findall("https://www.amazon.com.mx/[A-Za-z0-9_.%/-]+",c[2])
        nombres = re.findall("https://www.amazon.com.mx/([A-Za-z0-9_.%/-]+)", c[2])
        titulos = re.findall("([A-Za-z0-9:_.%/-]+)", c[0])
        if resultados and nombres[0] not in link_no_requeridos:
            archivo.write(c[0] + "\n" +resultados[0] + "\n\n")
    print("Productos vistos en Amazon)")

def ultimas_10_busquedas(archivo,historialChrome):
    archivo.write("Ultimas 10 busquedas en Chrome:\n\n\n")
    for c in historialChrome[:10]:
        archivo.write(c[0]+":\n" + c[2] + "\n\n")
    print("Ultimas 10 busquedas :)")


def perfiles_facebook(archivo,hisotrialChrome):
    archivo.write("\nPERFILES VISTADOS EN FACEBOOK\n\n")
    no_links = ["https://www.facebook.com/stories/"]
    contador = 0
    for c in hisotrialChrome:
        if contador >=10:
            break
        nombres = re.findall("https://www.facebook.com/([A-Za-z.=?0-9]+$)", c[2])
        resultado = re.findall("https://www.facebook.com/[A-Za-z.=?0-9]+$",c[2])
        if resultado and nombres[0]not in no_links:
               archivo.write(f"{contador+1}. "+resultado[0]+"\n")
               contador+=1

def bancoVisitados(hisotrialChrome):
    his_banck = None
    banks = ["azteca","bajío","inbursa","invex","banorte","citibanamex",
                     "santander","bbva","hsbc","scotiabank","banCoppel"]
    for item in hisotrialChrome:
        for b in banks:
            if b.lower() in item[0].lower():
                print(b)
                his_banck = b
                break
        if his_banck:
            break
    print(his_banck)


def main():

    nombre_archivo = "Historial de Chrome.txt"
    file = archivo(nombre_archivo)
    history = historialChrome()
    perfiles_twitter(file,history)





if __name__ == '__main__':
    main()