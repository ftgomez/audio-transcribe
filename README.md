# Audio transcribe
Módulo que transcribe audio a texto y lo procesa usando la API de OpenAI, permitiéndole al usuario hacer preguntas de forma interactiva sobre el contenido de la transcripción. Para poder usarlo es necesario tener un a API key de OpenAI, y cargarla como variable de ambiente en un archivo `.env`. Para eso, seguir el formato de `.env.example`.

## Instalación
Después de setear la variable de ambiente, instalar dependencias. Para eso crear ambiente virtual y usar `poetry`:

```bash
pip install poetry
poetry install
poetry shell
```

En caso de querer instalar o remover paquetes, usar `poetry add` o  `poetry remove` respectivamente.

## Uso
Ejecutar el archivo main.py de la siguiente manera:

```bash
python __main__.py -path "/path/to/mp3"   
```

De esta forma se puede interactuar con el Bot usando la consola para hacer preguntas.