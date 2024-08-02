# Install packages from pip
pip3 install colorama
pip3 install rich
pip3 install requests

echo Please provide your password, as RPK will be install to /usr/local/bin/

# Remove old version of RPK
sudo rm /usr/local/bin/rpk

# Move rift to /usr/local/bin
sudo cp rpk.py /usr/local/bin/rpk
mkdir ~/.rpk
cp assets/* ~/.rpk -r
sudo chmod +x /usr/local/bin/rpk

# Run
rpk
