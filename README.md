# stack-overflow-main-service
## How to start working on this project
### Docker style

Build image from local Dockerfile


Run base services of projects.
Clone [main-service](https://github.com/tvqphuoc01/stack-overflow-main-service.git) repository

```sh
cd main_service
docker-compose -f docker-compose.yml up -d
```

Go to http://localhost:8009 to check if it's working.

### Non-Docker style

Make sure you have virtual environment in this directory

```bash
virtualenv venv
```

After that active the virtual environment

```bash
source ./venv/bin/activate
```

Load environment params

```bash
export $(cat .env.dev)
```

Install requirements package using pip

```python
pip install -r requirements.txt
```

Start server

```python
python manage.py runserver
```

## Setup Flake8 and Black

```sh
pip install pre-commit==2.14.1
pre-commit install
chmod +x .git/hooks/pre-commit
```

## Coding guildlines
- All rules about code formatting will be ignored, Black and Flake8 will take care for us
- Small files, separate concerns, every class should have it own file.
- Use queryset and manager to reuse query.
- Documentation with Redoc
- Create small tests, single usecase in one test
- Simple and small methods, descriptive methods
- Not catching generic exceptions and let Sentry handle them
- Centralize side effects (update, create model, etc) in view
- Use debug toolbar to profile API performace (could change to use other tools)
- User data has to go through serializer
