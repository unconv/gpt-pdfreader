# GPT-PDFReader

Use the ChatGPT API to answer questions about content in a PDF file without using OpenAI embeddings API.

## Usage

```console
$ ./conversation.py [PDF_FILE] [CHUNK_SIZE] [OVERLAP] [LIMIT] [MODEL]
```

All command line arguments are optional. You can `export OPENAI_API_KEY=[YOUR_API_KEY]` if you don't want to input it every time.

## Requirements

```console
$ pip install openai pypdf2
```
