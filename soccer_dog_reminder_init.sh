#!/bin/bash
echo "/usr/bin/python "$PWD"/soccer_dog_reminder.py" > ./soccer_dog_reminder.sh
chmod a+x ./soccer_dog_reminder.sh
chmod a+x ./soccer_dog_reminder.py
echo "30 19 * * * "sh $PWD"/soccer_dog_reminder.sh > "$PWD"/cron.log" >> ./cron
echo "30 8 * * * "sh $PWD"/soccer_dog_reminder.sh > "$PWD"/cron.log" >> ./cron
crontab cron
rm cron