# mlops-iris-api

## Commande make

```bash
# construction de l'image docker
make build-api

# lancement de l'API dockerisé 
make run-api

# arrêt de l'API dockerisée
make stop-api

# lancement des services API+NGNIX (docker compose)
make start-project

# arrêt des services API+NGNIX (docker compose)
make stop-project
```

## Test unitaire API

```bash
# sur un docker API directement
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}'

# au travers du reverse proxy NGINX (écoutant sur le port 8080 avec route /predict)
curl -X POST "http://localhost:8080/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}'
```

## Outils de test de charge

```bash
# installation Apache Bench (AB fait partie de la suite apache2-utils)
sudo apt-get install apache2-utils

# utilisation simple (1000 requêtes totales avec 100 en parallèle)
ab -n 1000 -c 100 -p request.json -T application/json http://localhost:8080/predict

# analyse des logs d'un service avec replicas
# -f : follow (en direct)
# -t : timestamp daemon docker (en plus de ceux de l'appli pour cross verif entre services)
docker-compose -p mlops logs -t -f mlops-iris-api
```

## Gestion de la securité SSL/TLS

```bash
# creation d'un certificat autosigné (en root)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout deployments/nginx/certs/nginx.key -out deployments/nginx/certs/nginx.crt -subj "/CN=localhost"

# generation d'un fichier user/mot de passe htpasswd (initialisation avec un premier user admin)
htpasswd -c deployments/nginx/.htpasswd admin
# ajout d'une nouvelle entrée si htpasswd déjà existant
htpasswd deployments/nginx/.htpasswd username
```

## Test unitaire avec sécurité SSL/TLS

```bash
# au travers du reverse proxy NGINX (écoutant sur le port 443 avec route /predict)
curl -X POST "https://localhost/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}' \
    --cacert ./deployments/nginx/certs/nginx.crt;

# verifier le certificat deployé qui répond sur 443 (normalement NGINX)
openssl s_client -connect localhost:443 -showcerts </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -fingerprint -sha256

# comparer/verifier le certificat 
openssl x509 -in deployments/nginx/certs/nginx.crt -noout -subject -issuer -fingerprint -sha256

# au travers du reverse proxy NGINX (écoutant sur le port 443 avec route /predict) AVEC un user/password
curl -X POST "https://localhost/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}' \
    --user admin:admin \
    --cacert ./deployments/nginx/certs/nginx.crt;
```

## Test unitaire avec Rate Limiting

```bash
# au travers du reverse proxy NGINX (écoutant sur le port 443 avec route /predict) AVEC un user/password
for i in {1..20}; \
        do curl -s -o /dev/null -w "%{http_code}\n" \
        -X POST "https://localhost/predict" -H "Content-Type: application/json" \
        -d '{"petal_length":6.5, "petal_width":0.8}' \
        --user "admin:admin" --cacert ./deployments/nginx/certs/nginx.crt; \
    done
```

## Configuration des métriques et observabilité

```bash
# inspection du réseau docker pour retrouver son masque d'IP
docker network inspect mlops_default | grep Subnet

# test du fichier de conf après ajustement
docker exec nginx_revproxy nginx -t

# rechargement à chaud
docker exec nginx_revproxy nginx -s reload
```

## Rappels : Element de debugging

```bash
# visualisation des logs de l'application ou de nginx
docker-compose -p mlops logs mlops-iris-api # mode nom de projet (-p) + service
docker-compose logs nginx_revproxy # mode nom de container direct

# execution depuis le répertoire
docker-compose -p mlops exec nginx curl -X POST "http://mlops-iris-api:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}' \
    --user admin:admin \
    --cacert /etc/nginx/certs/nginx.crt;

# tester la syntaxe du nginx.conf ou visualiser son contenu sur le container
# - option 1 par docker
docker exec nginx_revproxy nginx -t 
docker exec nginx_revproxy cat /etc/nginx/nginx.conf
# - option 2 par docker-compose
docker-compose -p mlops exec nginx nginx -t 
docker-compose -p mlops exec nginx cat /etc/nginx/nginx.conf
```
