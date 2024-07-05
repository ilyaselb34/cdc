#!/bin/bash

# On remplit au préalable un fichier `~/.netrc` pour s'authentifier automatiquement 
# dans Nextcloud

sourcedir=$HOME/cdc_input/
cd "$sourcedir" || exit 1

# On synchronise le dossier local avec le dossier nextcloud partagé dans lequel
# les salariés versent les inputs

# On active l'environnement vituel python
# echo "$(which python)"
source ~/cdc/env/bin/activate
# echo "$(which python)"
# exit 0

echo "Synchronisation du dossier nextcloud avec $sourcedir ..."
nextcloudurl="https://clood.enercoop.org/remote.php/webdav/Production - REZO - Public/BE_CDC/nettoyage_CDC/input/"
nextcloudcmd -n --silent . "$nextcloudurl"

# Pour chaque fichier CSV présent dans le répertoire, si il n'existe pas de dossier 
# du même nom, on exécute le script
csv_files="$(find . -type f -name '*.csv')"
for f in $csv_files; do
    dir="${f%.*}"
    if [[ ! -e "$dir" ]]; then
        echo "Nettoyage de $f et export dans $dir ..."
        # TODO Execution du script dans un environnement virtuel
        python ~/cdc/clean_cdc.py --input_csv "$f" --output_dir "$dir"
    fi
done

# Resynchronisation du dossier local vers le dossier nextcloud
echo "Resynchronisation du dossier nextcloud avec $sourcedir ..."
nextcloudcmd -n --silent "$sourcedir" "$nextcloudurl"

# Ajout du job à la crontab
# Toutes les minutes du lundi au vendredi
# */1 * * * 1-5 ~/cdc/run.sh