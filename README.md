# Tokens

This repo defines the schema for PaperPlay tokens and provides a Python implementation for generating tokens from a json-specification.

## Token schema

A token always starts with `https://paperplay.en/`

### Wildcard tokens

For wildcard tokens the local path is `id/{id}`

### Spotify tokens

For Spotify tokens the local path is `s/{spotify-uri}`. The variable `spotify-uri` is shortened by the prefix `spotify:`. To get a valid spotify-uri the prefix needs to be prepended.

## JSON spec for generating tokens