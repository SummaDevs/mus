#!/bin/bash

# run from project root

source .venv/bin/activate

python --version

python -m spacy download en_core_web_lg
# python -m spacy download en_core_web_trf

python -m spacy download uk_core_news_lg
# python -m spacy download uk_core_news_trf

python -m spacy download ru_core_news_lg
