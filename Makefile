# ตัวแปรเริ่มต้น
APP_NAME ?= fastapi-eks
ECR_REPO ?= <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/$(APP_NAME)
REGION ?= <your-region>
CLUSTER_NAME ?= fastapi-cluster
ENV ?= dev

# คำสั่งหลัก
.PHONY: all test build push deploy logs clean status ecr-login

all: test build push deploy

# รัน unit test
test:
	cd app && pytest tests/

# Build Docker image
build:
	docker build --platform linux/amd64 -t $(APP_NAME):latest ./app

# Push image ไป ECR
push: ecr-login
	docker tag $(APP_NAME):latest $(ECR_REPO):latest
	docker push $(ECR_REPO):latest

# Deploy ไป Kubernetes
deploy:
	kubectl apply -k kubernetes/overlays/$(ENV)/

# ดู logs
logs:
	kubectl logs -l app=fastapi -n fastapi-$(ENV)

# ล้างทรัพยากร
clean:
	kubectl delete -k kubernetes/overlays/$(ENV)/

# ล็อกอิน ECR
ecr-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ECR_REPO)

# ตรวจสอบสถานะ
status:
	kubectl get pods -n fastapi-$(ENV)eksctl scale nodegroup --cluster $(CLUSTER_NAME) --name fastapi-nodes-small --nodes 2 --region $(REGION)
