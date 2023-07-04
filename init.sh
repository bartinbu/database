#!/bin/bash
cd ~
echo "Node Name"
read nodeName
echo "Node Type"
echo "1 - Humidity Sensor"
echo "2 - Distance sensor"
read typeID

if (( $typeID == 2 )) ; then
    nodeName+="_Distance"   
elif (( $typeID == 1 )) ; then
    nodeName+="_Humidity"
else
    echo "Invalid choice plase start again!"
fi
ssh-keygen -t rsa
echo "------------------------Go to github settings and click 'add SSH key' with this key.------------------------"
cat ~/.ssh/id_rsa.pub
echo "-----------------------------------------Press enter after copy.--------------------------------------------"
read pulse
cd /home/database
git config --global init.defaultBranch origin $nodeName
git config --global user.email "raspberrypi.bartin@gmail.com"
git config --global user.name "bartinbu"
git config --global pull.rebase false
git remote set-url origin git@github.com:bartinbu/database.git
git branch $nodeName
git checkout $nodeName
git push --set-upstream origin $nodeName
pip install -r requirements.txt

echo "[NODEINFO]
    nodename = $nodeName
    nodetype = $typeID
    sensorsize = 5
    ">config.ini
(crontab -l; echo "* * * * * /home/database/sync.sh >> /home/database/run.log") | sort -u | crontab -
