#!/bin/bash

# Chemin vers le répertoire où se trouve ce script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Déplace le fichier de configuration
mv -f $SCRIPT_DIR/O-Pynet/config.json $SCRIPT_DIR/tempopyconfig.json

# Supprime le dossier O-Pynet
rm -rf $SCRIPT_DIR/O-Pynet/

# Clone le dépôt
git clone https://github.com/Lenitra/O-Pynet.git $SCRIPT_DIR/O-Pynet

# Remet le fichier de configuration
mv -f $SCRIPT_DIR/tempopyconfig.json $SCRIPT_DIR/O-Pynet/config.json

# Remet le fichier de mise à jour
mv -f $SCRIPT_DIR/O-Pynet/executables/update.bash $SCRIPT_DIR/updateOpynet.bash
