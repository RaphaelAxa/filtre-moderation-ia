Modération de contenu des messages envoyés sur l'application mobile.

Programme utilisant l'IA Générative afin de vérifier que le message ne contienne pas de contenu inapproprié selon les règles de modération.

Cela fonctionne en envoyant un prompt (requête/demande formulé) à l'IA afin de vérifier que le contenu n'est pas inapproprié.

Pour adapter, améliorer les résultats vous n'avez juste qu'à ouvrir "system_prompt.yaml" dans un éditeur et modifier le message envoyé à l'IA. Vous pouvez par exemple ajouter des règles de modération, ajouter du contexte toute ce qui semble utile et qui permettra à l'IA de mieux comprendre ce que vous voulez faire.

Vous n'avez pas besoin de toucher au code juste à modifier ce prompt afin de voir les résultats. Pas besoin également de toucher à "input_prompt.yaml", ce fichier correspond à l'envoie du message en lui-même à analyser à l'IA donc il doit resté inchangé.

Pour voir les résultats de manière interactif :

###  Pré-requis :
 - Python 3.10+ (idéalement 3.12.6)
 - Git (Gestion de versions)
 - Créer un compte sur Groq (console.groq.com) et obtenir une clé d'accès API dans menu -> API Keys -> Create API Key -> Sauvegarder dans un fichier quelque part la clé API (suite de chiffres et lettres)

```bash
# Cloner le repo distant
git clone https://github.com/dracoeau/filtre-moderation-ia.git

# Création de l'environnement virtuel
python -m venv myenv

# Installation de toutes les dépendances nécessaires au bon fonctionnement du projet
pip install -r requirements.txt
```

Créer un fichier qui se nomme .env à la racine du projet
Dans ce fichier mettre :

```bash
GROQ_API_KEY="la valeur de votre clé api"
```

### Lancer la démo sur le site Web avec streamlit (vous pourrez envoyer vos messages à l'IA et voir en direct les résultats)

Utiliser la commande suivante dans le terminal à la racine du projet :
```bash
streamlit run demo.py
```

### Lancer le code avec résultat en local sur le terminal (les messages à tester sont dans le fichier main.py donc si vous voulez les changer il faut aller les modifier dans le fichier main.py)

```bash
python main.py
```
