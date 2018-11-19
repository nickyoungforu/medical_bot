#!/usr/bin/env bash

python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue -c config.yml