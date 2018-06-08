ChangeLog
*********

1.0.0
======

En cours voir :doc:`todo` pour plus d'info.

0.5.0
-----

* fonctions

    - change_password

0.4.1
------

* fonction

    - ajout des permissions utilisateur
    - permission effacer patient

* programation

    - ajout check_config
    - fallback pour ordonnances si ordre faux
    - exception MapistarBadRequest
    - item ne peuvent être ajouté qu'à une ordonnance
    - remove pendulum

0.3.0
------


* fonctions
  
    - l'ordre des ordonnances est conservé
    - JWT_DURATION dans settings
    - Module Ordonnance/item
    - ajout UserPermissions
   
* programation
    
    - drop pipenv pour poetry
    - class based views pour acteviews
    - Item Permissions gérés par ActePermissionComponent
    - séparation ActePermissionComponent/ActePermission
    - speed up test : mock et cli_test.py
    - ajout SetMixin
    - ajout MapistarHttpException


0.2.0
------

* Fonctions

    - ajout Patient, Baseacte, Observation
    - ajout User
    - ajout login et permissions

* Programation

    - drop django pour PonyORM
    - drop faker pour mimesis
    - fixture propre basée sur des factory
    - utilisation d'apistar-ponyorm
    - ajout de pendulum
    - ajout exception
    - ajout shortcuts : get_or_404
    - ajout utils : import_models et PendulumDateTime descriptor
    - apistart_jwt pou authentification
