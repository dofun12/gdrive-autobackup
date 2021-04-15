#!/bin/bash

SERVICE_NAME="gdrive-autobackup"
SERVICE_FILE="$SERVICE_NAME.service"
DESCRIPTION="gdrive-autobackup"
PIPENV_BIN=$(whereis pipenv|awk '{print $2}')

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
touch $SERVICE_FILE
cat > $DIR/$SERVICE_FILE <<EOL
[Unit]
Description=${DESCRIPTION}

[Service]
Restart=always
User=${USER}
WorkingDirectory=${DIR}
ExecStart=${PIPENV_BIN} run python main.py --profile prod --cron

[Install]
WantedBy=multi-user.target
EOL

sudo cp $SERVICE_FILE /lib/systemd/system/
sudo systemctl daemon-reload
echo "USE: 'sudo service $SERVICE_NAME start' to Start"
echo "USE: 'sudo systemctl enable $SERVICE_NAME' to Start at boot"

