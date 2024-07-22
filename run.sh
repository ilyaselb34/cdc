#!/bin/bash

# Dossier local contenant les inputs CSV sychronisés depuis nextcloud
sourcedir=$HOME/cdc/input/
cd "$sourcedir" || exit 1


# Voici l'adresse WebDAV du dossier nextcloud dans lequel les salariés versent les inputs
nextcloudurl="https://clood.enercoop.org/remote.php/webdav/Production - REZO - Public/BE_CDC/nettoyage_CDC/input/"

# On synchronise ce dossier local avec ce dossier nextcloud partagé
echo "Synchronisation du dossier Nextcloud partagé avec $sourcedir ..."
nextcloudcmd -n --silent . "$nextcloudurl" # -n permet de s'authentifier avec le fichier ~/.netrc
echo "Synchronisation terminée"
echo

# On active l'environnement vituel python nécessaire pour exécuter le script
source "$HOME/cdc/env/bin/activate"

# Pour chaque CSV du répertoire, si il n'existe pas d'output (=dossier du même nom), on exécute le script
csv_files="$(find . -maxdepth 1 -type f -name '*.csv')"
for f in $csv_files; do
    dir="${f%.*}"
    if [[ -e "$dir" ]]; then
        echo "Le répertoire $dir existe déjà, skip."
    else
        echo "Nettoyage de $f et export dans $dir ..."
        python ~/cdc/clean_cdc.py --input_csv "$f" --output_dir "$dir"
    fi
done

# On verse les outputs du dossier local vers le dossier nextcloud
echo "Resynchronisation du dossier nextcloud avec $sourcedir ..."
nextcloudcmd -n --silent "$sourcedir" "$nextcloudurl"

# Pour checker : 
# firefox https://clood.enercoop.org/index.php/f/49323033

# Ajout du job à la crontab
# Toutes les minutes du lundi au vendredi
# */1 * * * 1-5 ~/cdc/run.sh