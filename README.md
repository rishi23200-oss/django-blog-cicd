# Django Blog with CI/CD and Kubernetes Deployment

## Project Structure
/backend – Django REST API
/frontend – HTML+JS Frontend
/docker – Dockerfile, docker-compose.yml, nginx config
/k8s – Kubernetes manifests (deployment, service, ingress)
/.github/workflows/ – CI and CD pipelines

## Local Run Steps

### Prerequisites
- Docker Desktop installed and running

### Steps
```bash
# 1. Clone the repo
git clone https://github.com/rishi23200-oss/django-blog-cicd
cd django-blog-cicd

# 2. Create .env file
cp backend/.env.example backend/.env

# 3. Start all services
cd docker
docker compose up --build

# 4. Run migrations (new terminal)
docker compose exec web python manage.py makemigrations blog
docker compose exec web python manage.py migrate

# 5. Create superuser
docker compose exec web python manage.py createsuperuser
```

### Access
- Frontend: http://localhost:8080
- Backend API: http://localhost/posts/
- Admin Panel: http://localhost/admin/
- Health Check: http://localhost/health/
- Readiness: http://localhost/readiness/

## API Endpoints
| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST | /api/token/ | No |
| GET | /posts/ | No |
| POST | /posts/ | Yes |
| GET | /posts/<id>/comments/ | No |
| POST | /posts/<id>/comments/ | Yes |
| GET | /health/ | No |
| GET | /readiness/ | No |

## Deployment Steps

### DockerHub
```bash
docker build -t rishikesh1207/django-blog:latest ./backend
docker push rishikesh1207/django-blog:latest
```
- Image: https://hub.docker.com/r/rishikesh1207/django-blog

### Frontend (Netlify)
- Live Link: https://gleaming-kangaroo-44a074.netlify.app

### Backend (AWS Kubernetes - k3s on EC2)
- Live API (HTTPS): https://3.109.216.143.nip.io
- Health check: https://3.109.216.143.nip.io/health/
- Admin panel: https://3.109.216.143.nip.io/admin/ (user: rishi)

### Kubernetes Deployment Commands
```bash
sudo k3s kubectl apply -f k8s/deployment.yaml
sudo k3s kubectl apply -f k8s/service.yaml
sudo k3s kubectl apply -f k8s/ingress.yaml
```

### Monitoring (Prometheus + Grafana + Loki)
- Grafana Dashboard: http://3.109.216.143:32341 (user: admin / pass: admin123)
- Logs query in Grafana → Explore → Loki: {namespace="default"}