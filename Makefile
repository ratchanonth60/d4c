# ตัวแปรเริ่มต้น
APP_NAME ?= fastapi-eks
ECR_REPO ?= 361769569278.dkr.ecr.ap-southeast-1.amazonaws.com/$(APP_NAME)
REGION ?= ap-southeast-1
CLUSTER_NAME ?= fastapi-cluster
ENV ?= dev

# คำสั่งหลัก
.PHONY: all test build push deploy logs clean status ecr-login

all: test build push deploy

# รัน unit test ใน Docker
test:
	docker-compose up -d
	docker-compose exec app pytest 
	docker-compose down

# Build Docker image
build:
	docker build --platform linux/amd64 -t $(APP_NAME):latest .

# Push image ไป ECR
push: 
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
	kubectl get pods -n fastapi-$(ENV)

# รัน docker-compose
compose-up:
	docker-compose up -d --build

# ปิด docker-compose
compose-down:
	docker-compose down

# รัน test ใน compose
compose-test:
	docker-compose exec app pytest /app/tests/
