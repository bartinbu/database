#!/bin/bash
cd ~
echo "Node Name"
read nodeName
echo "Node Type"
echo "1 - Humidity Sensor"
echo "2 - Distance sensor"
read typeID
ssh-keygen -t rsa
echo "------------------------Go to github settings and click 'add SSH key' with this key.------------------------"
cat ~/.ssh/id_rsa.pub
echo "-----------------------------------------Press enter after copy.--------------------------------------------"
read pulse
cd /home/pi/database
git config --global init.defaultBranch origin $nodeName
git config --global user.email "raspberrypi.bartin@gmail.com"
git config --global user.name "bartinbu"
git config --global pull.rebase false
git remote set-url origin git@github.com:bartinbu/database.git
git branch $nodeName
git checkout $nodeName
git push --set-upstream origin $nodeName
pip install -r requirements.txt
cd ..
if (( $typeID == 2 )) ; then
    echo "[NODEINFO]
    nodename = $nodeName Humidity
    nodetype = $typeID
    sensorsize = 5
    ">config.ini
elif (( $typeID == 1 )) ; then
    echo "[NODEINFO]
    nodename = $nodeName Distance
    nodetype = $typeID
    sensorsize = 5
    ">config.ini
else
    echo "Invalid choice plase start again!"
fi
(crontab -l; echo "* * * * * /home/pi/database/sync.sh") | sort -u | crontab -
