FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip3 install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system
CMD ["python", "app.py"]
