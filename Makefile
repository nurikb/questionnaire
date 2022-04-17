ifneq (,$(wildcard ./.env))
    include .env
    export
    ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build -d --remove-orphans
up:
	docker-compose up -d
down:
	docker-compose down
logs:
	docker logs questionnaire_web_11
migrate:
	docker exec -it questionnaire_web_1 python3 manage.py migrate --noinput
makemigrations:
	docker exec -it questionnaire_web_1 python3 manage.py makemigrations
superuser:
	docker exec -it questionnaire_web_1 python manage.py createsuperuser
down-v:
	docker docker -v
dropdb:
	docker exec -i -u postgres questionnaire_db_1 dropdb postgres
createdb:
	docker exec -i -u postgres questionnaire_db_1 createdb -U postgres -W postgres
