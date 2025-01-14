#!/bin/bash

# Dossier local contenant les inputs CSV sychronisés depuis nextcloud
sourcedir=$HOME/cdc/input/
cd "$sourcedir" || exit 1

# On active la verbose pour les tests
verbose=false

# Voici le chemin vers le dossier nextcloud dans lequel les salariés versent les inputs
nextcloudurl=https://clood.enercoop.org/
path="/Production - REZO - Public/BE_CDC/nettoyage_CDC/input/"

# On synchronise le dossier local avec ce dossier nextcloud partagé
$verbose && echo "Synchronisation du dossier Nextcloud partagé avec $sourcedir ..."
nextcloudcmd -n --silent --path "$path" . $nextcloudurl # -n permet de s'authentifier avec le fichier ~/.netrc
$verbose && echo "Synchronisation terminée"
# echo

# On active l'environnement vituel python nécessaire pour exécuter le script
source "$HOME/cdc/env/bin/activate"

# Pour chaque CSV du répertoire, si il n'existe pas d'output (=dossier du même nom), on exécute le script
csv_files="$(find . -maxdepth 1 -type f -name '*.csv')"
for f in $csv_files; do
    dir="${f%.*}"
    if [[ -e "$dir" ]]; then
        $verbose && echo "Le répertoire $dir existe déjà, skip."
        continue
    else
        $verbose && echo "Nettoyage de $f et export dans $dir ..."
        python ~/cdc/clean_cdc.py --input_csv "$f" --output_dir "$dir"
    fi
done

# On verse les outputs du dossier local vers le dossier nextcloud
# echo
$verbose && echo "Resynchronisation du dossier nextcloud avec $sourcedir ..."
nextcloudcmd -n --silent --path "$path" . $nextcloudurl
$verbose && echo "Synchronisation terminée"
exit 0 # Permet de ne pas sortir sur un statut 1 suite à la ligne du dessus

# Pour checker : 
# firefox https://clood.enercoop.org/index.php/f/49323033