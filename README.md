# EEE_network

## Steps to run the network simulation:

1. cd ~
2. git clone https://github.com/Neurosim-lab/EEE_network.git
3. cd EEE_network/
4. cd mod
5. nrnivmodl
6. cd ../eee_net
7. ln -s "../mod/x86_64" x86_64
8. ./runsim

## One-liner to run sim from scratch:

cd ~ ; rm -rf eee_temp ; mkdir eee_temp ; cd eee_temp ; git clone https://github.com/Neurosim-lab/EEE_network.git ; cd EEE_network/mod ; nrnivmodl ; cd ../eee_net ; ln -s "../mod/x86_64" x86_64 ; ./runsim