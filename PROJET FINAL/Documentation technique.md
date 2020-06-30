# INFtc3 ProjetWeb
 
Documentation technique : 


Table countries du fichier pays.sql

Cette table est compos�e de 10 colonnes, soit 10 attributs : le nom usuel du pays (sous forme de texte), qui est la cl� primaire (c'est � dire que c'est avec cette donn�e que l'on peut identifier de mani�re unique un pays), son nom complet (texte), sa capitale (texte), le titre du dirigeant (texte)et son nom (texte), la latitude et la longitude de la capitale (toutes deux sous forme de r�els), la superficie du pays (sous forme de nombre entier), sa population (entier), ainsi que son drapeau (sous forme de texte, le nom de fichier .png, de fa�on � �tre appel� dans le fichier interface pour que le drapeau s'affiche).



Description de l'API du serveur : 

Au lancement de l'application, le serveur effectue plusieurs requ�tes GET pour charger les fichiers leaflet et style, ainsi que charger toutes les donn�es et faire appara�tre les pointeurs.
 
Lorsque l'utilisateur appuie sur un des POI, le serveur re�oit une requ�te GET/description/nom_du_pays. Il y r�pond donc en envoyant les informations du pays, et en effectuant en m�me temps une requ�te GET/flags/nom_du_pays.png afin d'affichant sous les informations le drapeau du pays.

Lorsque l'utilisateur entre un nom de pays dans la barre de recherche, le serveur re�oit une requ�te GET/service/country/nom_du_pays. Cela lui fait renvoyer les informations du pays en question, ainsi que le drapeau gr�ce � la requ�te GET/flags/nom_du_pays.png.

Lorsque l'utilisateur choisi un classement, le serveur re�oit une requ�te GET/nom_classement. Il renvoie alors la liste dans l'ordre des 5 premiers pays pour ce classement. 



Description de la logique du client :

Lorsque l'utilisateur clique sur un des pointeurs, il envoie � la fois une requ�te qui fait s'afficher le nom du pays sur la carte, et l'ensemble des informations de la base de donn�es concernant ce pays dans la partie gauche de l'�cran.

Lorsque l'utilisateur tape un nom dans la barre de recherche, et clique sur le bouton "Fiche", le client envoie au serveur la requ�te pour faire s'afficher dans la partie gauche de l'�cran les informations du pays.

Lorsque l'utilisateur d�cide de regarder un classement, il choisit dans un menu d�roulant le classement qu'il veut voir, par exemple les 5 pays d'Asie les plus peupl�s. Une fois qu'il a s�lectionn� le Top 5, celui-ci s'affiche directement.