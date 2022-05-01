import yaml

user = {"disk" : {0: 15, 1: 10, 2: 5, 3: 0}, "ram" : {0: 15, 1: 10, 2: 5, 3: 0}, "cpu" : {0: 15, 1: 10, 2: 5, 3: 0}}

with open('tmp/drcdata.yaml', 'w') as file:
    user = yaml.dump(user, file)


