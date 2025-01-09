# Litrevu

## Sommaire
- [Installation](#installation)
- [Migration de la base de données](#migration-de-la-base-de-données)
- [Lancer l'application](#lancer-lapplication)

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/ThomasDpr/litrevu.git
    cd litrevu
    ```

2. Créez et activez un environnement virtuel avec Pipenv :
    ```bash
    pipenv install
    pipenv shell
    ```

   Ou, si vous préférez utiliser un environnement virtuel standard et le fichier `requirements.txt` :
    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Installez les dépendances npm avec pnpm ou npm :
    ```bash
    pnpm install
    ```
    ou
    ```bash
    npm install
    ```

## Migration de la base de données

1. Appliquez les migrations :
    ```bash
    python manage.py migrate
    ```

## Lancer l'application

1. Si vous avez pnpm, utilisez le raccourci "dev" pour lancer le serveur Django et le watcher Tailwind CSS :
    ```bash
    pnpm run dev
    ```

   Si vous utilisez npm, lancez les commandes suivantes dans des terminaux séparés :
    ```bash
    npm run build:css
    python manage.py runserver
    ```

2. Ouvrez votre navigateur et allez à l'adresse suivante :
    ```
    http://127.0.0.1:8000
    ```