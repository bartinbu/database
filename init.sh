cd ~
echo "Node Name:"
read nodeName
ssh-keygen -t rsa
echo "------------------------Go to github settings and click 'add SSH key' with this key.------------------------"
cat ~/.ssh/id_rsa.pub
echo "-----------------------------------------Press enter after copy.--------------------------------------------"
read pulse
cd /home/pi/Desktop/database
git config --global init.defaultBranch origin main
git config --global user.email "raspberrypi.bartin@gmail.com"
git config --global user.name "bartinbu"
git config --global pull.rebase false
git remote set-url origin git@github.com:bartinbu/database.git
git branch $nodeName
git checkout $nodeName
git push --set-upstream origin istasyon2
pip install -r requirements.txt
cd ..
echo "[NODEINFO]
nodename = $nodeName
sensorsize = 5
">config.ini
(crontab -l; echo "* * * * * /home/pi/Desktop/database/sync.sh") | sort -u | crontab -
