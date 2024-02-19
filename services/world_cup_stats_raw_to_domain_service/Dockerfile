FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

COPY services/world_cup_stats_raw_to_domain_service/requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY services $APP_HOME/services

CMD ["uvicorn", "services.world_cup_stats_raw_to_domain_service.main:app", "--host", "0.0.0.0", "--port", "8080"]
