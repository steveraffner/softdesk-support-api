# SoftDesk Support API

API RESTful pour la gestion et le suivi des problèmes techniques développée avec Django REST Framework.

## 🚀 Fonctionnalités

- **Gestion des utilisateurs** avec authentification JWT
- **Gestion des projets** collaboratifs
- **Suivi des issues** (problèmes/tâches)
- **Système de commentaires**
- **Permissions granulaires** selon les rôles
- **Conformité RGPD** (âge minimum, consentement, droit à l'oubli)
- **Sécurité OWASP** (Authentification, Autorisation, Traçabilité)
- **Approche Green Code** (optimisation des requêtes, pagination)

## 🛠 Technologies utilisées

- **Django 4.2.7**
- **Django REST Framework 3.14.0**
- **Simple JWT** pour l'authentification
- **drf-spectacular** pour la documentation OpenAPI
- **Python 3.13**

## 📋 Prérequis

- Python 3.11 recommandé
- pip (gestionnaire de paquets Python)

## ⚡ Installation rapide

### 1. Cloner le repository
```bash
git clone https://github.com/steveraffner/softdesk-support-api.git
cd softdesk-support-api
```

### 2. Créer l'environnement virtuel
```bash
python3.11 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer la base de données
```bash
python manage.py migrate
```

### 5. Créer un superutilisateur
```bash
python create_superuser.py
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

L'API sera accessible à l'adresse : `http://127.0.0.1:8000/`

## 📚 Documentation API

### Documentation interactive
- **Swagger UI** : `http://127.0.0.1:8000/api/docs/`
- **ReDoc** : `http://127.0.0.1:8000/api/redoc/`
- **Schema OpenAPI** : `http://127.0.0.1:8000/api/schema/`

### Administration Django
- **Interface d'admin** : `http://127.0.0.1:8000/admin/`
- **Identifiants par défaut** : admin / admin123

## 🔐 Authentification

L'API utilise l'authentification JWT (JSON Web Token) :

### 1. Inscription
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test1234*",
    "password_confirm": "test1234*",
    "first_name": "Test",
    "last_name": "User",
    "birth_date": "2000-01-01",
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

### 2. Connexion
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "test1234*"
}
```

### 3. Utiliser le token
```http
Authorization: Bearer <access_token>
```

## 🏗 Architecture de l'API

### Modèles de données

#### User (Utilisateur)
- Modèle utilisateur personnalisé avec champs RGPD
- Validation de l'âge minimum (15 ans)
- Gestion du consentement

#### Project (Projet)
- Projets collaboratifs (Backend, Frontend, iOS, Android)
- Système d'auteur et de contributeurs

#### Issue (Problème/Tâche)
- Problèmes liés à un projet
- Priorité, statut, assignation
- Types : Bug, Feature, Task

#### Comment (Commentaire)
- Commentaires sur les issues
- Identifiant UUID unique

### Permissions et sécurité

- **Authentification obligatoire** pour toutes les ressources
- **Permissions granulaires** :
  - Seuls les contributeurs peuvent accéder aux projets
  - Seuls les auteurs peuvent modifier/supprimer leurs ressources
  - Lecture autorisée pour tous les contributeurs du projet

### Green Code

- **Pagination** automatique (20 éléments par page)
- **Optimisation des requêtes** base de données
- **Validation stricte** pour éviter les erreurs

## 🔗 Endpoints principaux

### Authentification
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/refresh/` - Actualiser le token

### Utilisateur
- `GET /api/profile/` - Profil utilisateur
- `PUT /api/profile/` - Modifier le profil
- `DELETE /api/delete-account/` - Supprimer le compte (RGPD)

### Projets
- `GET /api/projects/` - Liste des projets
- `POST /api/projects/` - Créer un projet
- `GET /api/projects/{id}/` - Détails d'un projet
- `PUT /api/projects/{id}/` - Modifier un projet
- `DELETE /api/projects/{id}/` - Supprimer un projet

### Contributeurs
- `GET /api/projects/{id}/contributors/` - Liste des contributeurs
- `POST /api/projects/{id}/add_contributor/` - Ajouter un contributeur
- `DELETE /api/projects/{id}/contributors/{contributor_id}/` - Supprimer un contributeur

### Issues
- `GET /api/projects/{project_id}/issues/` - Liste des issues
- `POST /api/projects/{project_id}/issues/` - Créer une issue
- `GET /api/projects/{project_id}/issues/{id}/` - Détails d'une issue
- `PUT /api/projects/{project_id}/issues/{id}/` - Modifier une issue
- `DELETE /api/projects/{project_id}/issues/{id}/` - Supprimer une issue

### Commentaires
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/` - Liste des commentaires
- `POST /api/projects/{project_id}/issues/{issue_id}/comments/` - Créer un commentaire
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Détails d'un commentaire
- `PUT /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Modifier un commentaire
- `DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Supprimer un commentaire

## 🛡 Conformité RGPD

### Droits des utilisateurs
- **Droit d'accès** : Consultation du profil (`GET /api/profile/`)
- **Droit de rectification** : Modification du profil (`PUT /api/profile/`)
- **Droit à l'oubli** : Suppression du compte (`DELETE /api/delete-account/`)

### Validation
- **Âge minimum** : 15 ans requis pour l'inscription
- **Consentement** : Champs `can_be_contacted` et `can_data_be_shared`

## 🔒 Sécurité OWASP

### AAA (Authentification, Autorisation, Audit)
- **Authentification** : JWT sécurisé
- **Autorisation** : Permissions basées sur les rôles
- **Audit** : Horodatage de toutes les ressources

### Protection des données
- Validation stricte des entrées
- Gestion sécurisée des mots de passe
- Tokens JWT avec expiration

## 🚀 Tests avec Postman

1. Importer la collection Postman (à venir)
2. Configurer les variables d'environnement :
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (sera défini automatiquement après connexion)

## 📝 Support

Pour toute question ou problème, veuillez consulter la documentation API interactive ou contacter l'équipe de développement.

---

**Version** : 1.0.0  
**Auteur** : Équipe SoftDesk  
**License** : Propriétaire
