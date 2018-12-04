### SpaCy chinese support
https://github.com/howl-anderson/Chinese_models_for_SpaCy

### nlu samples generate
```bash
python nlu_generator/nlu_gen.py
```

### train nlu model
```bash
python -m rasa_nlu.train -c nlu_config.yml --fixed_model_name current --data data/nlu.json -o models --project nlu --verbose
```

### train core model
```bash
python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue -c config.yml
```

### run endpoint server
```bash
python -m rasa_core_sdk.endpoint --actions actions
```

### run cmdline input
```bash
python -m rasa_core.run --core models/dialogue --nlu models/nlu/current --debug --endpoints endpoint.yml
```

### run asr input
```bash
python asr/asr_input.py
python -m rasa_core.run --core models/dialogue --nlu models/nlu/current --debug --endpoints endpoint.yml --connector rest --port 5002 --credentials credentials.yml
```
