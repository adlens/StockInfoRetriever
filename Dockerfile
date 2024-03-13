FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install pipenv && pipenv install --deploy --system
RUN pipenv run pip install redis
CMD ["python", "app.py"]
