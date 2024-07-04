# cdc

## Introduction

Les données de consommation électrique ou Courbes de Charge (CDC) électrique récupérées via le portail SGE d'Enedis au format CSV comportent parfois des irrégularités qui constituent un obstacle à leur étude. Il arrive que des données enregistrées de manière régulière (ex: toutes les 30 min) subissent une interruption de ce pas de temps (ex: le pas passe à 120min sur une certaine durée), il manque alors une partie des données, qui deviennent inexploitables pour leur étude en aval comme dans Archelios. Le présent projet permet d'automatiser le nettoyage de données de CDC, et l'export de graphiques permettant leur analyse.

## Installation

Via un terminal Linux ou Windows PowerShell, on commence par cloner le dépôt et se placer dedans :

```bash
git clone https://github.com/ilyaselb34/cdc.git
cd cdc/
```

Puis on va créer un environnement virtuel Python. Sous Windows, pour accorder les autorisations nécessaires à la création d'un environnement virtuel uniquement à cette session PowerShell et évite les risques de sécurité futurs :

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Et on vérifie que la commande `Get-ExecutionPolicy` renvoie `RemoteSigned`

On crée l'environnement virtuel Python, que l'on nomme ici `env`, que l'on active :

```bash
python -m venv env
source env/bin/activate
```

Avec Windows :

```bash
env\Scripts\Activate
```

Et on installe les paquets nécessaires :

```bash
pip install -r requirements.txt
```

## Utilisation

Le script à lancer est `cleand_cdc.py`. Supposons que l'on ait une CDC brute nommée `my_cdc.csv`. On met ces données au pas de temps horaire (60 minutes). On aurait pu omettre le paramètre `--timestep` car le pas de temps par défaut est déjà de 60 minutes :

```bash
python clean_cdc.py --input_csv my_cdc.csv --timestep 60
```

Le script va, dans l'ordre :

* Homogénéiser les données au pas de temps de 60 minutes.
* Remplir les "trous" dans les données mesurées d'une durée inférieure à 4h par une **interpolation linéaire**.
* Pour les trous supérieurs à 4h, il va faire la moyenne des données du même jour de la semaine précédente et de la semaine suivante. Par exemple, si il manque des données le lundi de la semaine 10 entre 8h et 14h, il va faire la moyenne des données du lundi de la semaine 9 de 8h à 14h, et du lundi de la semaine 11 de 8h à 14h.

Le résultat va être exporté, dans un répertoire automatiquement créé portant le même nom que le fichier - ici `my_cdc/` - dans un fichier `my_cdc_cleaned.csv`.

Puis le script va analyser ces données nettoyées en exportant, toujours dans le dans répertoire `my_cdc/`, les fichiers suivants :

* `my_cdc_profil_journalier.png` : Un graphique superposant les 7 courbes de consommation horaire moyenne pour chaque jour de la semaine.
* `my_cdc_profil_annuel.png` : un diagramme en barres de la consommation mensuelle totale de janvier à décembre.
* `my_cdc_profil_hebdo.png` : une boite à moustache de la consommation quotidienne observé pour chaque jour de la semaine.

En termes d'arborescence de fichiers, résultat est le suivant :

```bash
├── my_cdc
│   ├── my_cdc_cleaned.csv
│   ├── my_cdc_profil_annuel.csv
│   ├── my_cdc_profil_hebdo.csv
│   └── my_cdc_profil_journalier.csv
└── my_cdc.csv
```
