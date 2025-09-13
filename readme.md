
1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the root directory with the following keys:
```
DJANGO_SECRET_KEY=cmosnieocndsl
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1],0.0.0.0
 
DATABASE_NAME=irs_db
DATABASE_USER=irs_user
DATABASE_PASSWORD=irs_pass
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_URL=postgresql://irs_user:irs_pass@db:5432/irs_db
 
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
### important commands

**Run migrations:**
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

**Create a superuser (optional):**
```bash
python manage.py createsuperuser
```
 **Run the development server:**
```bash
python manage.py runserver
```

---

### Setup Instructions (with Docker)

1. **Start services using Docker Compose:**
```bash
docker-compose up --build
```

---

### PostgreSQL Backup & Restore

**Backup:**
```bash
bash backup/backup_postgres.sh
```

**Restore:**
```bash
cat backup.sql | docker exec -i <db_container_name> psql -U irs_user -d irs_db
```

---

### Useful Commands

- Check logs: `docker-compose logs -f`
- Stop services: `docker-compose down`
- Remove volumes: `docker-compose down -v`

---

### Notes

- Uses JWT for authentication
- API base URL: `/api/accounts/`
                `api/uploads/`
                `api/services`
