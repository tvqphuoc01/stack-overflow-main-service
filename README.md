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

## How to create network for docker and connect 2 services
- Create network with name `stackoverflow` if not exist
- Run docker network create [OPTIONS] NETWORK-NAME if you haven't created the network
- Run docker network ls to check if network is created
- Run docker ls -a and get the id of the docker container you want to add to the network
- Run docker network connect NETWORK-NAME CONTAINER-ID
- Run docker network inspect NETWORK-NAME to check if the container is added to the network
- install apt-get update && apt-get install ping to check if the container can ping to other container in the network
- Change request url to http://your-container-name:8000 to request data from this repo