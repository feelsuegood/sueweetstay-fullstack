# backend/Dockerfile

FROM python:3.11

# Setting the environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Creating a working directory
WORKDIR /app

# install poetry
RUN pip install poetry

# disable poetry venv creation
ENV POETRY_VIRTUALENVS_CREATE=false

# copy dependency files first
COPY pyproject.toml poetry.lock ./

# install dependencies
RUN poetry install --no-root

# Copying the project
COPY . .

# Opening the port (for ASGI server)
EXPOSE 8000

# Starting the ASGI server (gunicorn + uvicorn worker)
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
