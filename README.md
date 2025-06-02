# DevOps AWS Demo – Asset Tracker & Monitoring

![Project Status](https://img.shields.io/badge/status-in--progress-blue)
![CI/CD](https://github.com/Fsam10/devops-aws-demo/actions/workflows/ci-cd.yml/badge.svg)

## Présentation

Ce projet est un démonstrateur complet d’une **infrastructure Cloud DevOps moderne** :  
- **Infrastructure as Code (Terraform + AWS)**
- **Déploiement continu (GitHub Actions, ECR, EKS)**
- **Monitoring intelligent (Prometheus, Grafana)**
- **Application API Python/Flask conteneurisée**


---

## Architecture Globale

                    +------------------------+
                    |   GitHub Repository    |
                    +-----------+------------+
                                |
                         (GitHub Actions)
                                |
            +-------------------+--------------------+
            |                                        |
    +-------v--------+                        +-------v------+
    |   Build &      |                        |   Deploy     |
    |   Test Docker  |                        |   to EKS     |
    +-------+--------+                        +-------+------+
            |                                        |
    +-------v--------+                        +-------v------+
    |   AWS ECR      |----------------------->|   EKS        |
    +----------------+         (Image pull)   +-------+------+
                                                       |
                                  +--------------------+--------------+
                                  |                                   |
                          +-------v-------+                   +-------v-------+
                          | Asset API     |                   | Prometheus    |
                          | (Flask, CRUD) |                   | + Grafana     |
                          +-------+-------+                   +-------+-------+
                                  |                                   |
                          +-------v-------+                   +-------v-------+
                          |   PostgreSQL  |                   |  AlertManager |
                          |     (RDS)     |                   +-------+-------+
                          +-------+-------+                           |
                                  |                                   |
                              +---v---+                          +----v----+
                              |  S3   |-- (logs & backups) --->  | Glacier |
                              +-------+                          +---------+




---

## Fonctionnalités principales

### 1. **Infrastructure as Code (IaC)**
- Provisionnement complet via **Terraform** :  
  - Cluster **EKS** (Kubernetes managé)
  - Réseau (VPC, subnets privés/publics)
  - Buckets S3
  - Gestion fine IAM

### 2. **Application de démonstration**
- API CRUD **Python Flask** (Asset tracker IT)

### 3. **Pipeline CI/CD (GitHub Actions)**
- Build image Docker
- Push sur **Amazon ECR**
- Déploiement automatisé sur **EKS**

### 4. **Monitoring & Alerting**
- Stack **Prometheus + Grafana** (installés par Helm chart officiel)
- Monitoring :  
    - *Métriques cluster* (CPU, RAM, pods, etc.)
    - *Métriques applicatives custom* exposées par l’API (/metrics Prometheus)
- Dashboards et alertes (latence, erreurs 5xx, taux de succès)

### 5. **RSE / Impact Carbone** (in progress)
- Cycle de vie S3 : archivage automatique des logs vers Glacier (ou simulé)
- Script d’automatisation compression/envoi des logs
- Rapport estimatif de l’empreinte carbone basée sur la volumétrie

---

## 📦 Structure du repo

 - terraform/ # Infra as Code (EKS, VPC, S3)
 - k8s/ # Manifests deployment, service
 - app/ # Code de l’API Flask + seed + Dockerfile
 - monitoring/ # Manifests Prometheus, Grafana, ServiceMonitor
 - .github/workflows/ # Pipelines CI/CD (build, test, deploy)
 - rse/ # Scripts d’archivage + rapport carbone
 - README.md


---

## 🛠️ Lancer le projet

### 1. **Prérequis**
- Compte AWS (accès admin conseillé)
- AWS CLI & kubectl & helm configurés
- Terraform
- Docker

### 2. **Déploiement Infra**
```bash
cd terraform
terraform init
terraform apply
# Note les outputs pour la config kubectl/EKS et les variables d’environnement
````

### 3. **CI/CD**
Pousse une modif sur main : la pipeline GitHub Actions build/test/push/déploie tout automatiquement.

### 4. **Monitoring**
Accède à Grafana via port-forward ou via ELB

Login : admin / mot de passe dans les secrets K8s

### 5. **Logs & RSE** (in progress)
Script Python/Bash dans /rse pour compresser/envoyer logs

Voir rapport RSE pour l’estimation CO2e


### **📊 Exemples de captures/dashboards**



### **🔁 Perspectives & Améliorations**
Intégration complète de la gestion du cycle de vie S3 > Glacier (actuellement simulée)

Ajout d’alertes RSE automatisées (notification si volume ou empreinte > seuil)

Déploiement multi-environnements (dev, staging, prod)

Sécurité avancée (IAM least privilege, secrets Vault…)





**Auteur** : Samuel Fandio 
