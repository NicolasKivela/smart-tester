FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to install packages system-wide (no .venv)
RUN poetry config virtualenvs.create false

# Copy only dependency files first (for caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi
RUN playwright install

# Copy app source
COPY . .

CMD ["poetry", "run" ,"uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
