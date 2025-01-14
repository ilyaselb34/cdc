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

## Utilisation en local

Pour utiliser le script, on commence par réactiver l'environnement virtuel

```bash
cd cdc/
source env/bin/activate
```

Le script à lancer est `clean_cdc.py`. Supposons que l'on ait dans le dossier `input/` une CDC brute `Enedis_SGE_XXXX.csv`. Ce fichier doit obligatoirement 2 colonnes :

* `'Horodate'` : la date et heure de la mesure.
* `'Valeur'` : la puissance en watts.

On met ces données au pas de temps horaire (60 minutes). On aurait pu omettre le paramètre `--timestep` car le pas de temps par défaut est déjà de 60 minutes :

```bash
python clean_cdc.py --input_csv input/Enedis_SGE_XXXX.csv --timestep 60
```

Le script va, dans l'ordre :

* Homogénéiser les données au pas de temps de 60 minutes. Il va, pour chaque heure, effectuer la moyenne intra-horaire.
* Remplir les "trous" dans les données mesurées d'une durée inférieure à 4h par une **interpolation linéaire**.
* Pour les trous supérieurs à 4h, il va faire la moyenne des données du même jour de la semaine précédente et de la semaine suivante. Par exemple, si il manque des données le lundi de la semaine 10 entre 8h et 14h, il va faire la moyenne des données du lundi de la semaine 9 de 8h à 14h, et du lundi de la semaine 11 de 8h à 14h.

Le résultat va être exporté, dans un répertoire automatiquement créé portant le même nom que le fichier - ici `Enedis_SGE_XXXX/` - dans un fichier `Enedis_SGE_XXXX_cleaned.csv`.

Puis le script va analyser ces données nettoyées en exportant, toujours dans le dans répertoire `my_cdc/`, les fichiers suivants :

* `Enedis_SGE_XXXX_profil_journalier.png` : Un graphique superposant les 7 courbes de consommation horaire moyenne pour chaque jour de la semaine.
* `Enedis_SGE_XXXX_profil_annuel.png` : un diagramme en barres de la consommation mensuelle totale de janvier à décembre.
* `Enedis_SGE_XXXX_profil_hebdo.png` : une boite à moustache de la consommation quotidienne observé pour chaque jour de la semaine.

En termes d'arborescence de fichiers, résultat dans le dossier `input/` est le suivant :

```bash
├── Enedis_SGE_XXXX               <-- output
│   ├── Enedis_SGE_XXXX_cleaned.csv
│   ├── Enedis_SGE_XXXX_profil_annuel.csv
│   ├── Enedis_SGE_XXXX_profil_hebdo.csv
│   └── Enedis_SGE_XXXX_profil_journalier.csv
└── Enedis_SGE_XXXX.csv           <-- input
```

## Mise en production

Le script `run.sh` va permettre de faire tourner le programme sur le serveur `geo.enercoop.infra` sans avoir à l'exécuter manuellement. Ce script va, dans l'ordre :

* Synchroniser via WebDAV le [dossier Nextcloud](https://clood.enercoop.org/index.php/f/49323033) distant avec le dossier local `cdc/input/`
* Activer automatiquement l'environnement virtuel Python.
* Pour chaque fichier `myfile.csv` présent dans `cdc/input/`, si le répertoire `cdc/input/myfile/` n'existe pas encore, il va exécuter le script pour le créer et le remplir des outputs.
* Re-synchroniser le dossier `cdc/input/` avec le dossier Nextcloud pour y verser les outputs .

Pour synchroniser le dossier nextcloud, on utilise la commande `nextcloudcmd` :

```bash
nextcloudcmd -n --path <path>" <localdir> <nextcloudurl>
```

Où `<localdir>` est le dossier local à synchroniser, et `<path>` le chemin vers le dossier sur le serveur nextcloud `<nextcloudurl>`.

La commande s'installe avec :

```bash
sudo apt install nextcloud-desktop-client
```

Le paramètre `-n` permet d'utiliser le fichier `~/.netrc` pour s'authentifier sans avoir à rentrer le mot de passe. Cela implique de créer ce fichier et de le remplir de la manière suivante avec ses IDs intranet :

```text
machine clood.enercoop.org
login <prenom.nom>
password <mypassword>
```
