APP_NAME ?= fastapi-eks
ECR_REPO ?= 361769569278.dkr.ecr.ap-southeast-1.amazonaws.com/$(APP_NAME)
REGION ?= ap-southeast-1
CLUSTER_NAME ?= fastapi-cluster
ENV ?= dev
NAMESPACE ?= fastapi-$(ENV)

.PHONY: all test build push update-image deploy logs clean status ecr-login compose-up compose-down compose-test

all: test build push update-image deploy

build:
	docker build --platform linux/amd64 -t $(APP_NAME):latest .

push: 
	docker tag $(APP_NAME):latest $(ECR_REPO):latest
	docker push $(ECR_REPO):latest

update-image:
	kustomize edit set image $(APP_NAME)=$(ECR_REPO):latest k8s/overlays/$(ENV)/

deploy:
	kubectl apply -k k8s/overlays/$(ENV)/

logs:
	kubectl logs -l app=fastapi -n $(NAMESPACE)

clean:
	kubectl delete -k k8s/overlays/$(ENV)/
	kubectl delete namespace $(NAMESPACE) --ignore-not-found

ecr-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ECR_REPO)

status:
	kubectl get pods -n $(NAMESPACE)

up:
	docker-compose up -d --build $(target)

down:
	docker-compose down

test:
	docker-compose up -d
	docker-compose exec app pytest 
	docker-compose down

log:
	docker-compose logs -f $(target)

ssh:
	docker-compose exec app bash
