import openai
import json

model = "gpt-3.5-turbo"

def get_keywords(question):
    prompt = f"""I want to find the answer to the following question from a PDF file. Please provide me with 10 keywords and synonyms that I can use to find the information from the PDF. Only one word per keyword. Use only lowercase letters.

{question}"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You will always provide 10 keywords that include relevant synonyms of the words in the original question"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        functions=[
            {
                "name": "list_keywords",
                "description": "Use this function to give the user a list of keywords",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "list": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A keyword"
                            },
                            "description": "A list of keywords"
                        }
                    }
                },
                "required": ["list"]
            }
        ],
        function_call={
            "name": "list_keywords",
            "arguments": ["list"]
        }
    )

    arguments = response["choices"][0]["message"]["function_call"]["arguments"].lower()
    keywords = json.loads(arguments)["list"]

    return " ".join(keywords).split(" ")

def answer_question(chunk, question):
    prompt = f"""```
{chunk}
```

Based on the above information, what is the answer to this question?

```
{question}
```"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Always set answer_found to false if the answer to the question was not found in the informaton provided."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        functions=[
            {
                "name": "give_response",
                "description": "Use this function to give the response and whether or not the answer to the question was found in the text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer_found": {
                            "type": "boolean",
                            "description": "Set this to true only if the provided text includes an answer to the question"
                        },
                        "response": {
                            "type": "string",
                            "description": "The full response to the question, if the information was relevant"
                        }
                    }
                },
                "required": ["answer_found"]
            }
        ]
    )

    return json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
