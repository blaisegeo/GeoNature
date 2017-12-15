#!/bin/bash

. ./config/settings.ini

cd backend

echo "Création du fichier de configuration ..."
if [ ! -f config.py ]; then
  cp config.py.sample config.py
fi


echo "préparation du fichier config.py..."
my_url="${my_url//\//\\/}"
sed -i "s/SQLALCHEMY_DATABASE_URI = .*$/SQLALCHEMY_DATABASE_URI = \"postgresql:\/\/$user_pg:$user_pg_pass@$db_host:$db_port\/$db_name\"/" config.py
sed -i "s/URL_APPLICATION = .*$/URL_APPLICATION = '${my_url}geonature' /g" config.py
sed -i "s/URL_API = .*$/URL_API = '${my_url}api'/g" config.py
nano config.py

#Virtual env Installation
echo "Installation du virtual env..."



if [[ $python_path ]]; then
  virtualenv -p $python_path venv
else
  virtualenv --python python3 venv
fi



source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# lancement de gunicorn
make prod

#Frontend installation
#Node and npm instalation
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash
export NVM_DIR="$HOME/.nvm"
 [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 6.11.2
cd ../..
echo " ############"
echo "instalation des paquets npm"
npm install
echo " ############"
echo "instalation global d'angular cli"
npm install -g @angular/cli


cd ../frontend/src/conf
if [ ! -f app.config.ts ]; then
  cp app.config.sample.ts app.config.ts
fi


sed -i "s/URL_APPLICATION: .*$/URL_APPLICATION: '${my_url}geonature\/',/g" app.config.ts
sed -i "s/API_ENDPOINT: .*$/API_ENDPOINT: '${my_url}geonature\/api\/',/g" app.config.ts
sed -i "s/API_TAXHUB: .*$/API_TAXHUB: '${my_url}taxhub\/api\/',/g" app.config.ts

nano app.config.ts 

ng build --base-href /geonature/
