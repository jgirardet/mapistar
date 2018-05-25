Principes Généraux
*******************

Voici un ensemeble de règle respectées dans l'API.

Les Datetimes
===============

* Le format de de base utilisé est date et dateime de python. Il ne prend pas en compte les timezone.
* Tous les données sont fournies en UTC.
* Toutes les données seront stockées par défaut en UTC donc doivent être converties en UTC côté client
  

Les Permissions
================

Générales
-----------

* un user doit avoir la permission  `del_patient` pour effacer un patient. default = False. Doit être checké dans la view

Permissions des Actes
----------------------

Géré par le composant ActesPermissionsComp sous le contrôle du ActesPermission. Renvoi un objet si valide.