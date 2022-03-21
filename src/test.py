import yaml

test = {
    'title': 'title',
    'port': 5000,
}

with open('C:/Users/thoma/Desktop/O-Pynet/src/config/config.yaml', 'w') as file:

    outputs = yaml.dump(test, file)
