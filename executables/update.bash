#!/bin/bash

# Déplace le fichier de configuration
mv -f O-Pynet/config.json tempopyconfig.json

# Supprime le dossier O-Pynet
rm -rf O-Pynet/

# Clone le dépôt
git clone https://github.com/Lenitra/O-Pynet.git

# Remet le fichier de configuration
mv -f tempopyconfig.json O-Pynet/config.json


# Remet le fichier de mise à jour
mv -f O-Pynet/update.bash update.bash
