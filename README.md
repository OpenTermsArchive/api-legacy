# CGUs-api

## Get Started

### Endpoints

So far the API has two endpoints:
- `/first_occurence/v1/{term}` returns the first occurence of a given term for each "service" / "document_type" pair
- `/` and `/docs` is automatically generated documentation

### Running with Docker

The easiest option if you have Docker installed as it will automatically download the data for you.

```sh
docker build --no-cache --tag cgus-api:latest .
docker run -d --name myapi -p 80:80 cgus-api:latest
```

The API is served at `localhost`.

### Running with python (for development)

This API was built using `python3.8`. We suggest you use a virtual environment.

Install requirements

```sh
python -m pip install -r requirements.txt
```

Navigate to the `./app` directory and run the app

```
cd app
export PYTHONPATH=.
uvicorn main:app --reload
```

Note: you might need to edit `config.py` to give it the path to your local copy of the dataset.