# INFtc3 ProjetWeb
 
Documentation technique : 


Table countries du fichier pays.sql

Cette table est composée de 10 colonnes, soit 10 attributs : le nom usuel du pays (sous forme de texte), qui est la clé primaire (c'est à dire que c'est avec cette donnée que l'on peut identifier de manière unique un pays), son nom complet (texte), sa capitale (texte), le titre du dirigeant (texte)et son nom (texte), la latitude et la longitude de la capitale (toutes deux sous forme de réels), la superficie du pays (sous forme de nombre entier), sa population (entier), ainsi que son drapeau (sous forme de texte, le nom de fichier .png, de façon à être appelé dans le fichier interface pour que le drapeau s'affiche).


Description de l'API du serveur : 

Au lancement de l'application, le serveur effectue plusieurs requêtes GET pour charger les fichiers leaflet et style, ainsi que charger toutes les données et faire apparaître les pointeurs.
 
Lorsque l'utilisateur appuie sur un des POI, le serveur reçoit une requête GET/description/nom_du_pays. Il y répond donc en envoyant les informations du pays, et en effectuant en même temps une requête GET/flags/nom_du_pays.png afin d'affichant sous les informations le drapeau du pays.

Lorsque l'utilisateur entre un nom de pays dans la barre de recherche, le serveur reçoit une requête GET/service/country/nom_du_pays. Cela lui fait renvoyer les informations du pays en question, ainsi que le drapeau grâce à la requête GET/flags/nom_du_pays.png


Description de la logique du client :

Lorsque l'utilisateur clique sur un des pointeurs, il envoie à la fois une requête qui fait s'afficher le nom du pays sur la carte, et l'ensemble des informations de la base de données concernant ce pays dans la partie gauche de l'écran.

Lorsque l'utilisateur tape un nom dans la barre de recherche, et clique sur le bouton "Fiche", le client envoie au serveur la requête pour faire s'afficher dans la partie gauche de l'écran les informations du pays.