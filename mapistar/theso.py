from pythonthesorimed.thesoitem import ThesoItem
from apistar import Include, Route

theso_session = ThesoItem('localhost', 'thesorimed', 'j', 'j')


def fuzzy(chaine: str):
    return theso_session.fuzzy(chaine)


routes_theso = Include(
    url='/theso',
    name='theso',
    routes=[
        Route(url="/fuzzy/{chaine}/", method="GET", handler=fuzzy),
    ])
"""

api utils :


gsp :

get_the_indic_gsp


spe





scénario : 
sélection d'un medicament:
    - on part du code
        - si présent : ok
        -si pas présent :
             a = theso_session.proc('get_the_virtuel', [6410, 6411], 3)[0].sp_code_sq_pk   : il faut filtrer les commercialisés

    - on requete :
        - indication
        - poso


    - on recupère l'intérrop par
    - cpi_long, spq :  get_the _spe_details
    - indication_poso



[Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='80', ipo_dosemax='160', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='2', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='HYPERTENSION ARTERIELLE', voie='ORALE', fic=27441),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='80', ipo_dosemax='160', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='2', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes="ANGOR D'EFFORT", voie='ORALE', fic=27441),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='80', ipo_dosemax='160', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='2', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='MYOCARDIOPATHIE OBSTRUCTIVE HYPERTROPHIQUE', voie='ORALE', fic=27441),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin=None, ipo_dosemax='80', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='2', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='INFARCTUS DU MYOCARDE RECENT', voie='ORALE', fic=27442),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='80', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='CARDIOPATHIE THYREOTOXIQUE', voie='ORALE', fic=27443),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='80', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='TROUBLE DE LA CONDUCTION SUPRAVENTRICULAIRE', voie='ORALE', fic=27443),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='80', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='TROUBLE DE LA CONDUCTION INTRAVENTRICULAIRE', voie='ORALE', fic=27443),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin=None, ipo_dosemax='ADAPTER', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='1', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='HEMORRAGIE DIGESTIVE', voie='ORALE', fic=27444),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='120', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='MIGRAINE', voie='ORALE', fic=38516),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='120', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='ALGIE VASCULAIRE DE LA FACE', voie='ORALE', fic=38516),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='40', ipo_dosemax='120', un_prise='MG/PRISE', ipo_freqmin=None, freq_min=None, ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='TREMBLEMENT FAMILIAL / ESSENTIEL', voie='ORALE', fic=38516),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='0.25', ipo_dosemax='0.50', un_prise='MG/KG/ADMINISTRATION', ipo_freqmin='3', freq_min='/24 HEURES', ipo_freqmax='4', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='30 MOIS < AGE < 15 ANS', symptomes='TROUBLE DE LA CONDUCTION SUPRAVENTRICULAIRE', voie='ORALE', fic=38517),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin='0.25', ipo_dosemax='0.50', un_prise='MG/KG/ADMINISTRATION', ipo_freqmin='3', freq_min='/24 HEURES', ipo_freqmax='4', freq_max='/24 HEURES', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='30 MOIS < AGE < 15 ANS', symptomes='TROUBLE DE LA CONDUCTION INTRAVENTRICULAIRE', voie='ORALE', fic=38517),
 Record(sp_code_sq_pk=4672, sp_nom='AVLOCARDYL 40MG CPR', ipo_dosemin=None, ipo_dosemax='40', un_prise='MG/ADMINISTRATION', ipo_freqmin=None, freq_min='/24 HEURES', ipo_freqmax='.', freq_max='ADAPTER', ipo_dureemin=0, duree_min=None, ipo_dureemax=0, duree_max=None, age='AGE > 15 ANS', symptomes='ETAT DE CHOC EMOTIONNEL', voie='ORALE', fic=38518)]


[Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 6 a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('4'), unit_max='COMPRIME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 2190 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie adulte > 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('160'), unit_max='MILLIGRAMME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'adulte ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique", b_min='AGE 5475 Jour(s)', b_max='AGE 40150 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 30 mois a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('4'), unit_max='MILLIGRAMME(S)', par_masse=Decimal('1'), unit_pds='/ KG', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 900 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie adulte > 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('4'), unit_max='COMPRIME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'adulte ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique", b_min='AGE 5475 Jour(s)', b_max='AGE 40150 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 30 mois a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('1'), unit_max='MILLIGRAMME(S)', par_masse=Decimal('1'), unit_pds='/ KG', par_adm=Decimal('1'), unit_adm='/ ADMINISTRATION', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 900 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 30 mois a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('4'), unit_max='COMPRIME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 900 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 30 mois a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('160'), unit_max='MILLIGRAMME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 900 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie enfant 6 a 15 ans', min_max='MAX', nature='AD', borne_min=None, unit_min='NA', borne_max=Decimal('160'), unit_max='MILLIGRAMME(S)', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies maximales indicatives chez l'enfant ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique, et conformement aux donnees d'age, de poids ou de surface corporelle lorsqu'elles sont indiquees.", b_min='AGE 2190 Jour(s)', b_max='AGE 5475 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie adulte > 15 ans', min_max='MIN', nature='AD', borne_min=Decimal('1'), unit_min='COMPRIME(S)', borne_max=None, unit_max='NA', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies minimales indicatives chez l'adulte ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique", b_min='AGE 5475 Jour(s)', b_max='AGE 40150 Jour(s)'),
 Record(sp_code=4672, sp_nom='AVLOCARDYL 40MG CPR', critere='AGE', poso_name='Posologie adulte > 15 ans', min_max='MIN', nature='AD', borne_min=Decimal('40'), unit_min='MILLIGRAMME(S)', borne_max=None, unit_max='NA', par_masse=None, unit_pds='NA', par_adm=Decimal('24'), unit_adm='/ HEURE', par_m2=None, unit_area='NA', info="Posologies minimales indicatives chez l'adulte ne presentant pas de terrain physiopathologique pouvant necessiter une adaptation posologique", b_min='AGE 5475 Jour(s)', b_max='AGE 40150 Jour(s)')]


"""