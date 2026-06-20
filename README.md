# Django Blog with CI/CD and Kubernetes Deployment

## Project Structure


## Local Run Steps

### Prerequisites
- Docker Desktop installed and running

### Steps
```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/django-blog-cicd.git
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
docker build -t YOUR_DOCKERHUB_USERNAME/django-blog:latest ./backend
docker push YOUR_DOCKERHUB_USERNAME/django-blog:latest
```

### Frontend (Netlify)
- Netlify Link: https://gleaming-kangaroo-44a074.netlify.app

### Backend (AWS Kubernetes)
- AWS Backend URL: http://13.201.135.175

### Monitoring
- Grafana Dashboard: (add after deploy)
