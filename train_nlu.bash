#!/usr/bin/env bash

python -m rasa_nlu.train -c nlu_config.yml --fixed_model_name current --data data/nlu.json -o models --project nlu --verbose
