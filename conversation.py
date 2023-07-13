#!/usr/bin/env python3
import openai
import sys
import os

import pdf_reader
import lookup
import gpt

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    openai.api_key = input("Please enter your OpenAI API key: ")
    print()

program_name = sys.argv.pop(0)

if len(sys.argv):
    pdf_file = sys.argv.pop(0)
else:
    pdf_file = input("Please enter the PDF file you want to read: ")
    print()

    while not os.path.exists(pdf_file):
        print("ERROR: File not found")
        pdf_file = input("Please enter the PDF file you want to read: ")
        print()

if len(sys.argv):
    chunk_size = int(sys.argv.pop(0))
else:
    chunk_size = 4000

if len(sys.argv):
    overlap = int(sys.argv.pop(0))
else:
    overlap = 1000

if len(sys.argv):
    limit = int(sys.argv.pop(0))
else:
    limit = 5

if len(sys.argv):
    gpt.model = sys.argv.pop(0)
else:
    gpt.model = "gpt-3.5-turbo"

print("Chunking PDF...\n")
chunks = pdf_reader.chunk_pdf(pdf_file, chunk_size, overlap)

while True:
    question = input("GPT: What do you want to know?\nYou: ")
    print()
    keywords = gpt.get_keywords(question)

    print("Searching: " + ", ".join(keywords) + "")

    matches = lookup.find_matches(chunks, keywords)

    for i, chunk_id in enumerate(matches.keys()):
        print(".", end="", flush=True)

        chunk = chunks[chunk_id]
        response = gpt.answer_question(chunk, question)

        if response.get("answer_found"):
            print("\n\nGPT: " + str(response.get("response")) + "\n")
            break

        if i > limit:
            break

    if not response.get("answer_found"):
        print("\n\nGPT: I'm sorry, but I can't find that information\n")
