import yaml

test = {
    'title': 'title',
    'port': 5000,
}

with open('config/config.yaml', 'w') as file:
    outputs = yaml.dump(test, file)
