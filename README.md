# cdc

## Installation

On commence par cloner le dépôt :

```shell
git clone https://github.com/ilyaselb34/cdc.git
```

Puis on crée dans le répertoire l'environnement virtuel Python :

```shell
python3 -m venv .venv
```

Cela va créer un répertoire `.venv/` dans le dépôt, que l'on va ignorer dans le `.gitignore` en y ajoutant une ligne `.venv/`. On active l'environnement virtuel `.venv` :

```shell
source .venv/bin/activate
```

Puis on y installe dans l'environnement les paquets nécessaires listés dans `requirements.txt` :

```shell
pip install -r requirements.txt
```

## Utilisation

Pour obtenir une CDC propre au pas temps horaire :

```shell
./main.py --input_csv input/exemple_cdc.csv --timestep 60 --output_csv output/exemple_cdc_cleaned.csv
```
