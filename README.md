# Zinc Assignment

## Build, Test, and Run Instructions

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 1. Build the Docker Images

From the project root directory:
```bash
docker-compose build
```

---

### 2. Start the Services

This will start both the Django API and MySQL database:
```bash
bash start.sh
```
You can check the health of the containers with:
```bash
docker-compose ps
```

---

### 3. Run Database Migrations

Apply Django migrations to set up the database schema:
```bash
docker-compose exec django python manage.py migrate
```

---

### 4. Import Sales Data

Place your CSV files in `core/static/` and call the import endpoint:
```bash
curl http://localhost:8000/api/import-sales/
```

---

### 5. Run Unit Tests

To run all unit tests:
```bash
docker-compose exec django python manage.py test core.tests
```

---

### 6. Stopping and Cleaning Up

To stop the containers:
```bash
docker-compose down
```

To remove all data (including MySQL data):
```bash
docker-compose down -v
```

---

### 7. CI/CD
- On push to `master`, GitHub Actions will build, migrate, and test the project automatically.

---

### 8. API Endpoints
- `GET /api/import-sales/` — Import sales from CSV
- `GET /api/metrics/revenue/?start=YYYY-MM-DD&end=YYYY-MM-DD` — Revenue metrics
- `GET /api/metrics/revenue/daily/?start=YYYY-MM-DD&end=YYYY-MM-DD` — Daily revenue metrics
- `GET /health` - Check mysql connection

---

For more details, see [DESIGN.md](./DESIGN.md).
