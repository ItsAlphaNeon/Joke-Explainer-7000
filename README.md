
# Joke-Explainer™ 7000

A Python API that explains SiIvagunner High Quality Rips!

## Getting Started

This project is an API, meaning its basically the backend to whatever app / project you are going to use this with. You'll still need to make a frontend!

### Prerequisites

Python 3.11 was used for this project, but other versions may work as well. 

Everything can be installed with PIP, using the `requirements.txt`

Also, make sure you include a .env file with your OpenAI API key. You can get one at [OpenAI](https://platform.openai.com/signup).

Refer to the .env_template for the format.

```bash

### Installing

I recommend putting this in a Python Virtual Environment.

Once you do, run `pip install -r requirements.txt`

Run the server with `python api.py`

### API Usage

The API is a simple Flask app. You can use it with any HTTP client, like Postman or curl.

The default port is 5000, but you can change it in the `api.py` file.

Example usage with Curl:

```bash
curl -X POST http://localhost:5000/explain \
-H "Content-Type: application/json" \
-d '{
    "url": "https://www.youtube.com/watch?v=rEcOzjg7vBU"
}'
```

This will return a JSON response with the explanation of the rip's joke:

`{
  "joke": "The Joke\u2122: The melody of the Athletic Theme from Super Mario World has been mashed up with \"Witch Doctor\" by David Seville, especially incorporating the iconic \"ting tang walla walla bing bang\" part!"
}`

