FROM python:3.9

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
COPY README.md .
COPY api /app/api
COPY audio_transcribe /app/audio_transcribe

RUN pip install poetry
RUN poetry install
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]