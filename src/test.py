import yaml
from main import checkperms

user = [{'user': 'Taumah', 'password': 'admin', "perms":{"console": True, "config": True, "users": True, "screen": True}}, 
        {'user': 'admin', 'password': 'admin', "perms":{"console": True, "config": False, "users": False, "screen": False}}]

with open('config/accounts.yaml', 'w') as file:
    user = yaml.dump(user, file)


