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