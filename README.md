# mlops-iris-api

## Commande make

```bash
# construction de l'image docker
make build-api

# lancement de l'API dockerisé 
make run-api

# arrêt de l'API dockerisée
make stop-api

# test unitaire de l'API
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}'
```