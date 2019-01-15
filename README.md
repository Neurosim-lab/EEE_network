# EEE_network

Steps to run the network simulation:

cd ~

git clone https://github.com/Neurosim-lab/EEE_network.git

cd EEE_network/

git checkout joes_branch

cd mod

nrnivmodl

ln -s ~/EEE_network/mod/x86_64 ~/EEE_network/x86_64

cd ../eee_network

./runsim

