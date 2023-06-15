import json
import sys
import toml


toml_config = toml.dumps(config)

with open(output_file, 'w') as target:
    target.write(toml_config)