# Run Local Commands

local-webserver-bash:
	docker exec -it airflow_webserver bash

local-up:
	docker-compose up -d

local-down:
	docker-compose down

local-build-up:
	docker-compose up --build -d

local-webserver-logs:
	docker logs -f airflow_webserver

local-scheduler-logs:
	docker logs -f airflow_scheduler

local-worker-logs:
	docker logs -f airflow_worker

local-postgres-logs:
	docker logs -f airflow_postgres


