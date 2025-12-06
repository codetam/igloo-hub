ECR_NAME := igloo
IMAGE_NAME := igloo-fastapi-lambda-backend

deploy:
	@echo "** Building images **"
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
	docker cp igloo-frontend:/usr/share/nginx/html ./frontend/dist

	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 505231973540.dkr.ecr.us-east-1.amazonaws.com
	docker build --file backend/main/Dockerfile.aws -t igloo-fastapi-lambda-backend . 
	docker tag igloo-fastapi-lambda-backend:latest 505231973540.dkr.ecr.us-east-1.amazonaws.com/igloo-fastapi-lambda-backend:latest
	docker push 505231973540.dkr.ecr.us-east-1.amazonaws.com/igloo-fastapi-lambda-backend:latest

	cd terraform && \
	terraform apply --auto-approve --var-file="custom.tfvars"