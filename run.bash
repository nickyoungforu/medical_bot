#!/usr/bin/env bash

python -m rasa_core.run --core models/dialogue --nlu models/nlu/current --debug --endpoints endpoint.yml