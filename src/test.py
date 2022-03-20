import yaml

test = [{
        "user": "Taumah",
        "password": "admin",
        "perms": "admin" 
    },
    {
        "user": "Taumah",
        "password": "admin",
        "perms": "admin"
    }
    ]

with open('C:/Users/thoma/Desktop/O-Pynet/src/config/accounts.yaml', 'w') as file:

    outputs = yaml.dump(test, file)
