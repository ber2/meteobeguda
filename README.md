# MeteoBeguda

This project provides a Streamlit data app that fetches real-time meteorological data from [meteobeguda.cat](http://www.meteobeguda.cat/) and deploys it at [https://share.streamlit.io/ber2/meteobeguda](https://share.streamlit.io/ber2/meteobeguda).

## Environment setup

You should set up a virtual environment using python 3.9. A `pyproject.toml` file has been provided with the necessary dependencies. In order to install dependencies, for instance, you may use [poetry](https://python-poetry.org/). Assuming a virtual environment has been created and activated, run:

```bash
poetry install
```

Check for a successful setup by running the unit tests:

```bash
pytest
```

## Running the streamlit data app

Run:

```bash
streamlit run streamlit_app.py
```

The data app will open on a browser tab.
