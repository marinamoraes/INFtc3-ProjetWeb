# BASE DE DONNEES
import sqlite3
import json    
from zipfile import ZipFile
import re



# Ouverture d'une connexion avec la base de données
conn = sqlite3.connect('pays.sqlite',timeout=10)


c = conn.cursor()

c.execute('''CREATE TABLE "countries" (

    "wp"    TEXT NOT NULL UNIQUE,
    "name"    TEXT,
    "capital"    TEXT, 
    "leader_title"   TEXT, 
    "leader_name"    TEXT,
    "latitude"    REAL,
    "longitude"    REAL,
    "superficie"    INTEGER,
    "population"    INTEGER,
    "flag"  TEXT,
    
    
    PRIMARY KEY("wp")

);''')

conn.commit()


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
    sql = 'INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)'

# Les infos à enregistrer
    common_name=get_common_name(info)
    long_name = get_long_name(info)
    capital = get_capital(info)
    leader_title1 = get_leader_title1(info)
    leader_name1 = get_leader_name1(info)
    coords_dico=get_coords_dico(info)
    lat=coords_dico['lat']
    lon=coords_dico['lon']
    superficie=get_superficie(info)
    population=get_population(info)
    flag=get_flag(info)
    
     
# Soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(common_name,long_name, capital,leader_title1,leader_name1,lat,lon,superficie, population, flag))
    conn.commit()


# Récupérer les informations à partir de l'infobox

# Récupère le nom usuel du pays (non mis dans la base de données mais en général identique à "wp")
def get_common_name(info):
    return info['common_name']

# Récupère le nom long du pays (il faut compléter à la main si la sortie soit 'None')
def get_long_name(info):
    try:
        long_name= info['conventional_long_name']
        
    except KeyError:
        return "Republic of Singapore"
    if info['common_name']=='Kazakhstan':
        long_name= 'Republic of Kazakhstan'
    if info['common_name']=='Nepal':
        long_name= 'Federal Democratic Republic of Nepal'
    if info['common_name']=='Palestine':
        long_name= 'State of Palestine'
    if info['common_name']=='Sri Lanka':
        long_name= 'Democratic Socialist Republic of Sri Lanka'
    return long_name

# Récupère le nom de la capital 
def get_capital(info):
    try:
        capital = info['capital']
        m = re.match("\[\[(\w+)\]\]", capital)  # On enlève les crochets
        if m!=None:
            capital = m.group(1)    
        else:						# Si la capitale a un nom double, il faut corriger à la fin (ça ne marche pas)
            capital='None'			
         
        
    except KeyError:			# Si le pays n'a pas de capitale officielle (Palestine)
        return "None"
    if info['common_name']=='Brunei':
        capital='Bandar Seri Begawan'
    if info['common_name']=='Cambodia':
        capital='Phnom Penh'
    if info['common_name']=='UAE':
        capital='Abou Dabi'
    if info['common_name']=='India':
        capital= 'New Delhi'
    if info['common_name']=='Kazakhstan':
        capital= 'Astana'
    if info['common_name']=='Kuwait':
        capital='Kuwait'
    if info['common_name']=='Malaysia':
        capital= 'Kuala Lumpur'
    if info['common_name']=='Oman':
        capital= 'Mascate'
    if info['common_name']=='Singapore':
        capital= 'Singapore'
    if info['common_name']=='Sri Lanka':
        capital= 'Sri Jayawardenapura Kotte'
    if info['common_name']=='Yemen':
        capital= 'Sanaa'
    return capital
    
    
# Récupère le titre du leader
def get_leader_title1(info):
    try:
        leader_title1 = info['leader_title1']
        leader_title1 = leader_title1.replace('[','') # On enlève les crochets
        leader_title1 = leader_title1.replace(']','')
        leader_title1 = leader_title1.split('|') # On separe en deux parties (avant et après |)
         # On prend juste la première partie
        # Exemple : '[[President of India|President]]' devient 'President of India'
        
    except KeyError:
        return "None"
    if info['common_name']=='Brunei':
        leader_title1[0]= 'Sultan of Brunei'
    if info['common_name']=='Qatar':
        leader_title1[0]= 'Emir of Qatar'
    if info['common_name']=='Jordan':
        leader_title1[0]='King of Jordan'
        
    return leader_title1[0]


# Récupère le nom du leader
def get_leader_name1(info):
    try:
        leader_name1 = info['leader_name1']
        leader_name1 = leader_name1.replace('[','') # On enlève les crochets
        leader_name1 = leader_name1.replace(']','')
        leader_name1 = leader_name1.replace('{{nowrap|','') # On enlève cette partie de ces qui l'ont
        leader_name1 = leader_name1.replace('}','')
        
    except KeyError:
        return "None"
    if info['common_name']=='China':
        leader_name1 = 'Xi Jiping'
    if info['common_name']=='Palestine':
        leader_name1='Mahmoud Abbas'
    return leader_name1

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
        if info['common_name']=='Malaysia':
            lat=3+9/60+20/3600
            lon=101+41/60+49/3600
        if info['common_name']=='Maldives':
            lat=4+10/60+29/3600
            lon=73+30/60+35/3600
        if info['common_name']=='Palestine':
            lat=31+47/60
            lon=35+14/60
        if info['common_name']=='the Philippines':
            lat=14+35/60
            lon=120+58/60
        if info['common_name']=='Yemen':
            lat=15+21/60+11/3600
            lon=44+12/60+54/3600
        return {'lat':lat, 'lon':lon }
        
    
    return cv_coords(coords)


# Récupère la superficie du pays
def get_superficie(info):
    info=info['area_km2']
    return info.replace(',',"")

# Récupère la population du pays
def get_population(info): 
    try :
        population = info['population_census']
    except:
        population = info['population_estimate']
        
    if info['common_name']=='Armenia':
        population='3,018,854'
    if info['common_name']=='Cambodia':
        population='15,288,489'
    if info['common_name']=='Cyprus':
        population='838,897'
    if info['common_name']=='Georgia':
        population='3,713,804'
    if info['common_name']=='Iraq':
        population='38,872,655'
    if info['common_name']=='Kazakhstan':
        population='18,448,600'
    if info['common_name']=='Lebanon':
        population='5,469,612'
    if info['common_name']=='Myanmar':
        population='53,582,855 '
    if info['common_name']=='Pakistan':
        population='212,742,631'
    if info['common_name']=='Russia':
        population='146,793,744'
    if info['common_name']=='Singapore':
        population='5,638,700'
    if info['common_name']=='South Korea':
        population='51,446,201'
    if info['common_name']=='Turkey':
        population='82,003,882'
    if info['common_name']=='Turkmenistan':
        population='5,411,012'
    if info['common_name']=='Vietnam':
        population='98,721,275'
    
    return population

def get_flag(info):
    country=info['common_name']
    flag='{}-150x100.png'.format(info['common_name'])
    return flag
    



# Pour accéder au résultat des requêtes sous forme d'un dictionnaire
conn.row_factory = sqlite3.Row
   
    

# REMPLISSAGE BASE DE DONNEES

# On récupère une liste de documents json des pays
liste_pays=get_liste_pays()

for pays in liste_pays[:]:   #pays est par ex "China.json"
    
    info=get_info(pays)		# On récupère l'infobox
    save_country(conn,info)	# On enregistre le pays et ses attributs dans la base de données
    
