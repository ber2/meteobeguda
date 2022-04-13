# MeteoBeguda

This project provides two tools that fetch real-time meteorological data from [meteobeguda.cat](http://www.meteobeguda.cat/):

- `etl.py` for fetching and storing daily data.
- `streamlit_app.py` for deploying a Streamlit data app at [https://share.streamlit.io/ber2/meteobeguda](https://share.streamlit.io/ber2/meteobeguda)

The common code to fetch and parse data is available in the `meteobeguda` module.

## Environment setup

You should set up a virtual environment using python 3.9. A `pyproject.toml` file has been provided with the necessary dependencies. In order to install dependencies, for instance, you may use [poetry](https://python-poetry.org/). Assuming a virtual environment has been created and activated, run:

```bash
poetry install
```

Check for a successful setup by running the unit tests:

```bash
pytest
```

## Running `etl.py`

These are the usage options:

```bash
$ python etl.py --help
Usage: etl.py [OPTIONS]

Options:
  --lookback INTEGER              [default: 1]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Running the streamlit data app

Run:

```bash
streamlit run streamlit_app.py
```

The data app will open on a browser tab.
