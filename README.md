# cdc

## Introduction

Les données fournies par SGE au format CSV possèdent parfois des irrégularités temporelles qui constituent un obstacle à une étude optimale de ces données et à l'obtention de résultats optimaux. En clair, il arrive que des données enregistrées de manière régulière (ex: toutes les 30 min) subissent une interruption de ce pas de temps (ex: le pas passe à 120min sur une certaine durée), il manque alors une partie des données et il devient compliqué de réaliser des rapports.

Quand cela arrive il faut manipuler les données à la main sur un tableur, ce qui peut s'avérer fastidieux sachant que les données sont récoltées sur une année entière. C'est pourquoi il est nécessaire d'automatiser ce traitement.

Pour ce faire, nous allons utiliser un environnement virtuel Python.

## Clonage du dépôt GitHub

### Clonage sous Windows

- Ouvrez l'invite de commande Windows PowerShell.
- Placez vous dans le dossier dans lequel vous souhaitez cloner le dépôt avec la commande suivante (vous pouvez copier l'adresse avec clic droit dans la barre d'adresse de l'explorateur de fichiers Windows):

```bash
cd chemin\absolu\du\dossier
```

- Clonez le dépôt avec la commande:

```bash
git clone https://github.com/ilyaselb34/cdc.git
```

Le dépôt est maintenant cloné.

### Clonage sous Linux

- Ouvrez un terminal:
- Placez-vous dans le dossier dans lequel vous souhaitez cloner le dépôt avec la commande suivante :

```bash
cd /chemin/absolu/du/dossier
```

- Clonez le dépôt avec la commande:

```bash
git clone https://github.com/ilyaselb34/cdc.git
```

Le dépôt est maintenant cloné.

## Installation de l'environnement virtuel

### Installation sous Windows

- Ouvrez l'invite de commande Windows PowerShell si vous l'avez fermée
- Placez vous dans le répertoire dans lequel vous avez cloné le dépôt avec la commande suivante si vous n'y êtes pas déjà.

```bash
cd chemin\absolu\du\dossier
```

- Placez vous dans le répertoire cdc avec

```bash
cd cdc
```

- Entrez la commande:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Cela permet d'accorder les autorisations nécessaires à la création d'un environnement virtuel uniquement à cette session PowerShell et évite les risques de sécurité futurs

- Facultatif : Vous pouvez vérifier le statut de l'autorisation avec la commande:

```bash
Get-ExecutionPolicy
```

La console doit renvoyer "RemoteSigned"

- Entrez la commande:

```bash
python -m venv env
```

Cela crée l'environnement virtuel python nommé 'env'

- Activez l'environnement avec la commande:

```bash
env\Scripts\Activate
```

- Maintenant que l'environnement est activé, installez les modules nécessaires avec la commande :

```bash
pip install -r requirements.txt
```

- Facultatif: vous pouvez consulter les modules installés dans l'environnement avec la commande :

```bash
pip freeze
```

L'environnement est prêt à être utilisé.

### Installation sous Linux

- Ouvrez un terminal si ce n'est pas déjà fait.
- Placez-vous dans le répertoire dans lequel vous avez cloné le dépôt avec la commande suivante si vous n'y êtes pas déjà.

```bash
cd /chemin/absolu/du/dossier
```

- Placez-vous dans le répertoire cdc avec

```bash
cd cdc
```

- Entrez la commande :

```bash
python3 -m venv env
```

Cela crée l'environnement virtuel Python nommé 'env'.

- Activez l'environnement avec la commande :

```bash
source env/bin/activate
```

- Maintenant que l'environnement est activé, installez les modules nécessaires avec la commande :

```bash
pip install -r requirements.txt
```

- Facultatif: vous pouvez consulter les modules installés dans l'environnement avec la commande :

```bash
pip freeze
```

L'environnement est prêt à être utilisé.

## Utilisation

Supposons que vous ayez un fichier de courbes de charges à étudier/corriger, nommé Enedis_SGE_HDM_A06GKIR0.csv et que vous souhaitiez mettre ces données au pas de temps horaire (une mesure toutes les 60 min).

Dans ce cas, vous appellerez le script main.py avec l'invite de commande de la manière suivante:

### Utilisation sous Windows

- Placez vous dans le répertoire cdc:

```bash
cd adresse\absolue\du\dossier
cd cdc
```

- Si l'environnement n'est pas déjà activé, activez le:

```bash
env\Scripts\Activate
```

- Appelez maintenant le script main.py et utilisez les arguments --input_csv et --timestep:

```bash
python clean_cdc.py --input_csv courbes_2023.csv --timestep 60
```

### Utilisation sous Linux

- Placez vous dans le répertoire cdc:

```bash
cd /chemin/absolu/du/dossier
cd cdc
```

- Si l'environnement n'est pas déjà activé, activez le:

```bash
source env/bin/activate
```

- Appelez maintenant le script main.py et utilisez les arguments --input_csv et --timestep:

```bash
python clean_cdc.py --input_csv Enedis_SGE_HDM_A06GKIR0.csv --timestep 60
```

### Résultats

Le programme imprime alors un tableau à 2 lignes qui indique les lignes du CSV généré où le temps écoulé depuis la mesure précédente varie. Si le tableau ne contient que 2 lignes, c'est que le pas temporel est constant.

Un tableau CSV nommé courbes_2023_cleaned.csv est alors exporté dans le sous répertoire output.
