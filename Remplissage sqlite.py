# -*- coding: utf-8 -*-
"""
A2b - Groupe B

@author: Eduardo
"""
# BASE DE DONNEES
import sqlite3
import json    
from zipfile import ZipFile
import re

# Liste des documents contenus dans le fichier zip
def get_liste_pays():
    with ZipFile('Asia.zip','r') as z:
   		return(z.namelist())
        
# Récupère l'infobox d'un pays
def get_info(pays):
    
    with ZipFile('Asia.zip','r') as z:           
        info = json.loads(z.read('{}'.format(pays)))
        return(info)

# Enregistre un pays et ses attributs dans la base de données
def save_country(conn,info):
    
# Préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT INTO countries2 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

# Les infos à enregistrer
    common_name=get_common_name(info)
    long_name = get_long_name(info)
    capital = get_capital(info)
    leader_title1 = get_leader_title1(info)
    leader_name1 = get_leader_name1(info)
    coords_dico=get_coords_dico(info)
    lat=coords_dico['lat']
    lon=coords_dico['lon']
    pib=get_pib(info)
    superficie=get_superficie(info)
     
# Soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(common_name,long_name, capital,leader_title1,leader_name1,lat,lon,pib,superficie))
    conn.commit()


# Récupérer les informations à partir de l'infobox

# Récupère le nom usuel du pays (non mis dans la base de données mais en général identique à "wp")
def get_common_name(info):
    return info['common_name']

# Récupère le nom long du pays (il faut compléter à la main si la sortie soit 'None')
def get_long_name(info):
    try:
        return info['conventional_long_name']
    except KeyError:
        return "None"

# Récupère le nom de la capital 
def get_capital(info):
    try:
        capital = info['capital']
        m = re.match("\[\[(\w+)\]\]", capital)  # On enlève les crochets
        if m!=None:
            capital = m.group(1)    
        else:						# Si la capitale a un nom double, il faut corriger à la fin (ça ne marche pas)
            capital='None'			
        return(capital) 
        
    except KeyError:			# Si le pays n'a pas de capitale officielle (Palestine)
        return "None"

# Récupère le titre du leader
def get_leader_title1(info):
    try:
        leader_title1 = info['leader_title1']
        leader_title1 = leader_title1.replace('[','') # On enlève les crochets
        leader_title1 = leader_title1.replace(']','')
        leader_title1 = leader_title1.split('|') # On separe en deux parties (avant et après |)
        return(leader_title1[0]) # On prend juste la première partie
        # Exemple : '[[President of India|President]]' devient 'President of India'
    except KeyError:
        return "None"

# Récupère le nom du leader
def get_leader_name1(info):
    try:
        leader_name1 = info['leader_name1']
        leader_name1 = leader_name1.replace('[','') # On enlève les crochets
        leader_name1 = leader_name1.replace(']','')
        leader_name1 = leader_name1.replace('{{nowrap|','') # On enlève cette partie de ces qui l'ont
        leader_name1 = leader_name1.replace('}','')
        return(leader_name1)
    except KeyError:
        return "None"

# Récupérer les coordonnées d'un pays
# Convertir les coordonnées
# QUelques pays n'ont pas de coordonnées dans le fichier
def cv_coords(str_coords):
    # on découpe au niveau des "|" 
    c = str_coords.split('|')[1:-1]

    # on extrait la latitude en tenant compte des divers formats
    lat = float(c.pop(0))
    if (c[0] == 'N'):
        c.pop(0)
    elif ( c[0] == 'S' ):
        lat = -lat
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'N' ):
        lat += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'S' ):
        lat += float(c.pop(0))/60
        lat = -lat
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'N' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'S' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        lat = -lat
        c.pop(0)

    # on fait de même avec la longitude
    lon = float(c.pop(0))
    if (c[0] == 'W'):
        lon = -lon
        c.pop(0)
    elif ( c[0] == 'E' ):
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'W' ):
        lon += float(c.pop(0))/60
        lon = -lon
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'E' ):
        lon += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'W' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        lon = -lon
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'E' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        c.pop(0)
    
    # on renvoie un dictionnaire avec les deux valeurs
    return {'lat':lat, 'lon':lon }

# Récupère les coordonnées 
def get_coords_dico(info):
    try:
        coords = info['coordinates']#[2:-2]
    except KeyError:						# Si le pays n'en a pas dans les données fournies, on les remplira à la main
        return {'lat':0, 'lon':0}
    
    return cv_coords(coords)

# Récupère les coordonnées en chaîne de caractères (non affiché dans la base de données finalement) 
def get_coords_str(info):
    try:
        coords = info['coordinates']
    except:
        coords={'lat':0, 'lon':0}
    c = coords.split('|')[1:-1]
    if len(c)==8:
        return c[0]+'°'+c[1]+"'"+ c[2]+"'"+c[3]+' '+c[4]+'°'+c[5]+"'"+ c[6]+"'"+c[7]
    elif len(c)==6:
        return c[0]+'°'+c[1]+"'"+ c[2]+' '+c[3]+'°'+c[4]+"'"+c[5]
    else :
        return None

# Récupère le PIB total du pays
# Les PIB étaient souvent donnés avec des caractères et phrases non voulues, il a fallu extraire les valeurs
def get_pib(info):
    string = info['GDP_PPP']
    if string[0] == '{':
        liste = string.split('|')
        
        for i in liste :
            if i[0]== '$':
                string = i
    
        
    if 'billion' in string :
        
        rendu = ''
        for i in string :
            if i == '.':
                rendu += i
            try :
                nombre = int(i)
                rendu += i    
            except ValueError :
                pass
        try :
            rendu = float(rendu)*1e9
            return int(rendu)
        except ValueError :
            return 0
    
    if 'trillion' in string :
        rendu = ''
        for i in string :
            if i == '.':
                rendu += i
            try :
                nombre = int(i)
                rendu += i    
            except ValueError :
                pass
        try :
            rendu = float(rendu)*1e12
            return int(rendu)
        except ValueError :
            return 0

# Récupère la superficie du pays
def get_superficie(info):
    info=info['area_km2']
    return info.replace(',',"")


# Ouverture d'une connexion avec la base de données
conn = sqlite3.connect('pays5.sqlite',timeout=10)

# Pour accéder au résultat des requêtes sous forme d'un dictionnaire
conn.row_factory = sqlite3.Row
   
    

# REMPLISSAGE BASE DE DONNEES

# On récupère une liste de documents json des pays
liste_pays=get_liste_pays()

for pays in liste_pays[:]:   #pays est par ex "China.json"
    
    info=get_info(pays)		# On récupère l'infobox
    save_country(conn,info)	# On enregistre le pays et ses attributs dans la base de données