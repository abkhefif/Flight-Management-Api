# ✈️ Flight Management System

> API REST complète pour la gestion des vols et des créneaux aéroportuaires avec allocation automatique et détection de conflits

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)

**Développé par :** Abdallah Khefif  
**Contact :** abdallah.khefif@gmail.com  
**GitHub :** [@abkhefif](https://github.com/abkhefif)

---

## 📋 Table des matières

- [Description](#-description)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Tests](#-tests)
- [API Documentation](#-api-documentation)
- [Architecture](#️-architecture)
- [Améliorations futures](#-améliorations-futures)

---

## 🎯 Description

Système de gestion de vols développé pour démontrer mes compétences en développement backend Python. Le projet implémente une **API REST complète** avec :

- **Allocation automatique de créneaux horaires** (slots) pour chaque vol
- **Détection de conflits** entre vols utilisant les mêmes ressources
- **Validation métier stricte** via Pydantic
- **Architecture en couches** (Models, Schemas, Services, Routes)
- **Tests exhaustifs** avec pytest (87% coverage sur le service métier)

**Contexte :** Projet développé dans le cadre de ma recherche d'emploi comme **Backend Developer** pour mettre en pratique mes compétences en Python, FastAPI, SQLAlchemy et architecture API REST.

---

## ✨ Features

### 🔹 Gestion des ressources aéroportuaires

| Ressource | Description | Endpoints |
|-----------|-------------|-----------|
| **Airports** | Gestion des aéroports avec codes IATA, villes, pays, fuseaux horaires | 5 endpoints CRUD |
| **Runways** | Gestion des pistes d'atterrissage avec dimensions et statuts | 5 endpoints CRUD |
| **Gates** | Gestion des portes d'embarquement par terminal | 5 endpoints CRUD |
| **Flights** | Création de vols avec allocation automatique de slots | 5 endpoints CRUD |
| **Slots** | Créneaux horaires générés automatiquement | 5 endpoints CRUD |

**Total : 25 endpoints REST**

### 🔹 Logique métier avancée

#### ✅ Allocation automatique de slots
Lors de la création d'un vol, le système crée automatiquement **2 slots** :
- **Slot DEPARTURE** : 30 min avant le départ prévu + 15 min après
- **Slot ARRIVAL** : 30 min avant l'arrivée prévue + 15 min après
```python
# Exemple : Vol AF123 départ à 10h00
Slot DEPARTURE: 09h30 → 10h15  (runway de l'aéroport de départ)
Slot ARRIVAL:   14h30 → 15h15  (runway de l'aéroport d'arrivée)
```

#### ✅ Détection de conflits
Le système vérifie automatiquement les **chevauchements de créneaux** :
- Impossible de créer 2 vols utilisant la même runway au même moment
- Retourne une erreur **409 Conflict** si détecté
- Utilise des **transactions SQLAlchemy** avec rollback automatique

#### ✅ Validations métier
**Validations Pydantic automatiques :**
- Airports de départ ≠ arrivée
- Heure d'arrivée > heure de départ
- Durée minimum de vol : 15 minutes
- Durée de slot : entre 15 et 60 minutes

**Gestion des erreurs :**
- `400 Bad Request` : Runway non disponible
- `409 Conflict` : Conflit de créneaux détecté
- `422 Unprocessable Entity` : Validation échouée

---

## 🛠️ Tech Stack

### Backend
- **Python 3.12** - Langage principal
- **FastAPI 0.104** - Framework web moderne et performant
- **Uvicorn 0.24** - Serveur ASGI

### Base de données
- **SQLAlchemy 2.0** - ORM Python
- **Alembic 1.12** - Migrations de base de données
- **SQLite** - Base de données (dev/test)

### Validation & Configuration
- **Pydantic 2.5** - Validation de données
- **pydantic-settings 2.1** - Configuration via variables d'environnement
- **python-dotenv 1.0** - Chargement de fichiers `.env`

### Tests
- **pytest 8.3** - Framework de tests
- **pytest-cov 6.0** - Coverage des tests
- **87% coverage** sur le service métier principal

---

## 📦 Installation

### Prérequis
- Python 3.12+
- pip
- virtualenv (recommandé)

### Étapes
```bash
# 1. Cloner le repository
git clone https://github.com/abkhefif/flight-management-system.git
cd flight-management-system

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer le fichier .env
cat > .env << EOF
DATABASE_URL=sqlite:///./app.db
EOF

# 5. Initialiser la base de données
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(engine)"

# 6. Lancer le serveur
uvicorn app.main:app --reload
```

**L'API est maintenant accessible sur :** `http://localhost:8000`

---

## 🚀 Usage

### Documentation interactive
Accédez à la documentation Swagger : `http://localhost:8000/docs`

### Exemples avec curl

#### Créer un airport
```bash
curl -X POST "http://localhost:8000/api/v1/airports" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "CDG",
    "name": "Charles de Gaulle",
    "city": "Paris",
    "country": "France",
    "timezone": "Europe/Paris"
  }'
```

#### Créer une runway
```bash
curl -X POST "http://localhost:8000/api/v1/runways" \
  -H "Content-Type: application/json" \
  -d '{
    "runway_code": "09L/27R",
    "length_meters": 4200,
    "width_meters": 45,
    "surface_type": "asphalt",
    "status": "AVAILABLE",
    "airport_id": "airport_id_here"
  }'
```

#### Créer un vol (avec allocation automatique de slots)
```bash
curl -X POST "http://localhost:8000/api/v1/flights" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_number": "AF123",
    "airline": "Air France",
    "departure_airport_id": "cdg_id",
    "arrival_airport_id": "jfk_id",
    "scheduled_departure": "2026-01-22T10:00:00",
    "scheduled_arrival": "2026-01-22T14:00:00",
    "status": "SCHEDULED"
  }'
```

#### Lister tous les vols
```bash
curl -X GET "http://localhost:8000/api/v1/flights"
```

---

## 🧪 Tests

Le projet inclut une suite de tests complète avec **pytest**.

### Lancer tous les tests
```bash
pytest
```

### Tests avec coverage
```bash
pytest --cov=app --cov-report=html
```

### Tests par module
```bash
# Tests des airports
pytest tests/test_airports.py -v

# Tests des vols
pytest tests/test_flights.py -v

# Tests de validation
pytest tests/test_flight_validations.py -v

# Tests de conflits
pytest tests/test_flight_conflicts.py -v
```

### Coverage actuel
```
app/services/flight_service.py    87%   ← Service métier principal
app/models/                       100%   ← Tous les modèles
app/schemas/                       95%+  ← Validation Pydantic
TOTAL GLOBAL:                     ~78%
```

### Types de tests inclus
- ✅ Tests CRUD de base (POST, GET all)
- ✅ Tests de validation Pydantic
- ✅ Tests de détection de conflits
- ✅ Tests d'isolation de base de données (`:memory:`)

---

## 📊 API Documentation

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| **Airports** | | |
| GET | `/api/v1/airports` | Liste tous les airports |
| POST | `/api/v1/airports` | Crée un airport |
| GET | `/api/v1/airports/{id}` | Récupère un airport |
| PUT | `/api/v1/airports/{id}` | Met à jour un airport |
| DELETE | `/api/v1/airports/{id}` | Supprime un airport |
| **Runways** | | |
| GET | `/api/v1/runways` | Liste toutes les runways |
| POST | `/api/v1/runways` | Crée une runway |
| GET | `/api/v1/runways/{id}` | Récupère une runway |
| PUT | `/api/v1/runways/{id}` | Met à jour une runway |
| DELETE | `/api/v1/runways/{id}` | Supprime une runway |
| **Gates** | | |
| GET | `/api/v1/gates` | Liste toutes les gates |
| POST | `/api/v1/gates` | Crée une gate |
| GET | `/api/v1/gates/{id}` | Récupère une gate |
| PUT | `/api/v1/gates/{id}` | Met à jour une gate |
| DELETE | `/api/v1/gates/{id}` | Supprime une gate |
| **Flights** | | |
| GET | `/api/v1/flights` | Liste tous les vols |
| POST | `/api/v1/flights` | Crée un vol + slots automatiques |
| GET | `/api/v1/flights/{id}` | Récupère un vol |
| PUT | `/api/v1/flights/{id}` | Met à jour un vol |
| DELETE | `/api/v1/flights/{id}` | Supprime un vol |
| **Slots** | | |
| GET | `/api/v1/slots` | Liste tous les slots |
| GET | `/api/v1/slots/{id}` | Récupère un slot |

**Documentation interactive complète :** `http://localhost:8000/docs`

---

## 🏗️ Architecture

### Structure du projet
```
flight-management-system/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/          # Endpoints REST
│   │           ├── airports.py
│   │           ├── runways.py
│   │           ├── gates.py
│   │           ├── flights.py
│   │           └── slots.py
│   ├── core/
│   │   └── database.py          # Configuration SQLAlchemy
│   ├── models/                  # Modèles SQLAlchemy (ORM)
│   │   ├── airport.py
│   │   ├── runway.py
│   │   ├── gate.py
│   │   ├── flight.py
│   │   └── slot.py
│   ├── schemas/                 # Schémas Pydantic (validation)
│   │   ├── airport.py
│   │   ├── runway.py
│   │   ├── gate.py
│   │   ├── flight.py
│   │   └── slot.py
│   ├── services/                # Logique métier
│   │   └── flight_service.py   # Allocation slots + conflits
│   ├── config.py                # Configuration (env vars)
│   └── main.py                  # Point d'entrée FastAPI
├── tests/                       # Suite de tests pytest
│   ├── conftest.py              # Fixtures pytest
│   ├── test_airports.py
│   ├── test_runways.py
│   ├── test_gates.py
│   ├── test_flights.py
│   └── test_flight_conflicts.py
├── requirements.txt             # Dépendances Python
├── .env                         # Variables d'environnement
├── .gitignore
└── README.md
```

### Architecture en couches
```
┌─────────────────────────────────────────┐
│          FastAPI Routes                 │  ← Endpoints REST
│         (api/v1/routes/)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│        Pydantic Schemas                 │  ← Validation
│           (schemas/)                     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Service Layer                   │  ← Logique métier
│          (services/)                     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       SQLAlchemy Models                 │  ← ORM
│           (models/)                      │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Database                       │  ← SQLite
└─────────────────────────────────────────┘
```

### Patterns utilisés
- **Repository Pattern** : Isolation de la logique d'accès aux données
- **Service Layer** : Logique métier séparée des routes
- **Dependency Injection** : FastAPI `Depends()` pour les sessions DB
- **DTO Pattern** : Pydantic schemas pour Create/Read/Update

---

## 🚀 Améliorations futures

### Priorité haute
- [ ] Migration vers PostgreSQL (production)
- [ ] Authentification JWT
- [ ] Pagination sur les endpoints GET
- [ ] Rate limiting
- [ ] Logging structuré (Loguru)

### Priorité moyenne
- [ ] Containerisation Docker
- [ ] CI/CD avec GitHub Actions
- [ ] Déploiement sur cloud (Render/Railway)
- [ ] Monitoring (Prometheus/Grafana)

### Priorité basse
- [ ] Frontend React/Vue pour visualisation
- [ ] WebSockets pour notifications temps réel
- [ ] Export PDF des horaires de vols
- [ ] API de météo intégrée

---

## 📄 License

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Abdallah Khefif**

- 📧 Email : abdallah.khefif@gmail.com
- 💼 LinkedIn : [Abdallah Khefif](https://linkedin.com/in/abdallah-khefif)
- 🐙 GitHub : [@abkhefif](https://github.com/abkhefif)

---

## 🙏 Remerciements

Projet développé dans le cadre de ma formation à 42Rome et de ma recherche d'emploi comme Backend Developer.

**Stack technique apprise :** Python, FastAPI, SQLAlchemy, pytest, architecture API REST, design patterns.

---

**⭐ Si ce projet vous a plu, n'hésitez pas à mettre une étoile sur GitHub !**
