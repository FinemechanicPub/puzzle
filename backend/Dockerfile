FROM python:3.10-slim-bookworm
RUN groupadd -r puzzle && useradd --no-log-init -r -g puzzle puzzle
WORKDIR /code
# Install dependencies
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy backend files
COPY ./app ./app
COPY ./engine ./engine
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini
COPY ./manage.py ./manage.py
# Swith user
USER puzzle
# Set variables
ENV BRANCH=${GITHUB_REF}
ENV COMMIT=${GITHUB_SHA}
# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]