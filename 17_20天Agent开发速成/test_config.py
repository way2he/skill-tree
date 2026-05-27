import sys
sys.path.insert(0, '.')

from llm.core.default import CONFIG_PATH, _read_provider_config

print(f'CONFIG_PATH: {CONFIG_PATH}')
print(f'Exists: {CONFIG_PATH.exists()}')
print(f'Config: {_read_provider_config("ollama")}')
