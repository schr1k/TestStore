## Setup:

```bash
docker compose build
```

```bash
docker compose up
```

---
If you want to create superuser to interact with admin-panel run
```bash
docker compose run django python manage.py migrate
```
```bash
docker compose run django python manage.py createsuperuser
```

### .env file structure:
```dotenv
# Telegram
TOKEN=''
CHANNEL_USERNAME=''
RETURN_URL=''

# Postgres
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_DB='postgres'
POSTGRES_HOST='pgdb'
POSTGRES_PORT='5432'

# Redis
REDIS_HOST='redis'
REDIS_PORT='6379'
REDIS_DB='4'

# Yookassa
YOOKASSA_ACCOUNT_ID=
YOOKASSA_SECRET_KEY=''

```