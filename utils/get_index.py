import requests
import yaml

# Получение спецификации OpenAPI в формате JSON
response = requests.get('http://127.0.0.1:8000/openapi.json')
openapi_json = response.json()

# Конвертация JSON в YAML
openapi_yaml = yaml.dump(openapi_json)

# Сохранение YAML в файл
with open('backend/index.yml', 'w') as file:
    file.write(openapi_yaml)
