#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Script directory: $SCRIPT_DIR"

ls -al $SCRIPT_DIR/config/celery/celery.service

cp $SCRIPT_DIR/config/celery/celery.service /etc/systemd/system/

mkdir /var/log/celery

systemctl daemon-reload

systemctl start celery.service

systemctl status celery


