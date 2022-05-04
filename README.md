# Open Terms Archive - API

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

This project has been initially done to provide a backend infrastructure for [Scripta Manent](https://disinfo.quaidorsay.fr/en/open-terms-archive/scripta-manent)

We will leave this project as it is for now an focus on having a more global approach to serve the data from each instance.

## Get Started

### Endpoints
All API endpoints are automatically documented in `/docs`

### Running with Docker

The easiest option if you have Docker installed as it will automatically download the latest data available for you.

```sh
docker build --build-arg=COMMIT=$(git rev-parse --short HEAD) --tag cgus-api:latest .
docker run -d --name myapi -p 80:80 cgus-api:latest
```

The API is served at `localhost`.


### Custom command for M1

```sh
docker run --platform cgus-api --platform linux/amd64  -d --name myapi -p 80:80 cgus-api:latest
```
### Running with python (for development)

This API was built using `python3.8`. We suggest you use a virtual environment.

You will also need a local copy of the dataset. By default, it is assumed to be in `./dataset` but you can always change this by editing `./app/config.py`.

To download the dataset, run :
`./download_dataset.sh`

Install requirements

```sh
python -m pip install -r requirements.txt
```

And run the app :

```
export PYTHONPATH=".":"./app/"
uvicorn main:app --reload
```

## Develop

The required setup in order to contribute to the repo:
- `pip install -r requirements-dev.txt`
- `python -m python_githooks`

## Update Dataset

The API has a `/check_for_dataset` route that automatically finds out if a newer version of the dataset has been released [here](https://github.com/OpenTermsArchive/contrib-versions/releases/latest) and update the API to use it.

You can check which dataset release is being used by calling the `/version` endpoint.

- - - -

## License

The code in this repository is distributed under the  European Union Public Licence (EUPL) v1.2.
