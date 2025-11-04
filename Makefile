links:
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000"

build-api:
	docker build -t mlops-iris-api -f ./src/api/Dockerfile .

run-api:
	docker run --rm -d --name iris-api -p 8000:8000 mlops-iris-api

stop-api:
	docker stop iris-api