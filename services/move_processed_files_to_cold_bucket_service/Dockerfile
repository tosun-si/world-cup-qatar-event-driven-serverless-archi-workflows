FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

COPY services/move_processed_files_to_cold_bucket_service/requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY services $APP_HOME/services

CMD ["uvicorn", "services.move_processed_files_to_cold_bucket_service.main:app", "--host", "0.0.0.0", "--port", "8080"]
