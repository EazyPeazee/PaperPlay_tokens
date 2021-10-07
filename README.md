# Tokens

This repo defines the schema for PaperPlay tokens and provides a Python implementation for generating tokens from a json-specification.

## Token schema

A token always starts with `https://paperplay.en/`

### Wildcard tokens

For wildcard tokens the local path is `id/{id}`

### Spotify tokens

For Spotify tokens the local path is `s/{spotify-uri}`. The variable `spotify-uri` is shortened by the prefix `spotify:`. To get a valid spotify-uri the prefix needs to be prepended.

## JSON spec for generating tokens

The specification contains a list of cards. Each card has two properties:

* id (string, without prefix `https://paperplay.eu`)
* image (string, path to image relative to specification file)

Example (see folder `example_spec` for full example):

    [
        {
            "id": "i/1",
            "image": "img/1.png"
        },
        {
            "id": "i/2",
            "image": "img/2.png"
        }
    ]

## Running

1. Install python
2. Create a python virtual environment
    
        virtualenv -p python3 .venv

3. Enter the virtual environment

        source .venv/bin/activate

4. Install dependencies

        pip install -r requirements.txt

5. Run the generator

        python src/generator.py example_spec/spec.json --size 30 --margin 5 --qr-padding 6


See the command line help for a detailed description of the command line arguments.