# Audio transcribe
Module that transcribes audio to text and processes it using the OpenAI API, allowing the user to interactively ask questions about the content of the transcription. To use it, you need to have an OpenAI API key and load it as an environment variable in a `.env` file. Follow the format of `.env.example` for this.

## Instalación
After setting the environment variable, install dependencies. To do this, create a virtual environment and use `poetry`:

```bash
pip install poetry
poetry install
poetry shell
```

If you want to install or remove packages, use `poetry add` or `poetry remove` respectively.

## Uso
Run the `main.py` file as follows:

```bash
python main.py -path "/path/to/mp3"
```

This way, you can interact with the bot using the console to ask questions. Additionally, you can use `docker-compose` to launch an API on port `8000`. This API has two POST endpoints: `create_chat`, which takes the path to an audio file and a question about its content, and `chat`, which takes questions about an existing conversation.
