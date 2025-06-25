#!/bin/bash -eu


DEV_NAME="$2"
IP="$3"

# exit codes
ALREADY_CREATED=1
HELP=2
NOT_FOUND_VALID_FLAGS=3


function help_use {
    echo -e "The script creating virtual bridge."
    echo -e "Syntax use: sudo bash creating_bridge.sh [ Options ] [ EthDevice ] [ IPaddr ]"
    echo -e "Where EthDevice is the physical device that we add to the virtual network bridge."
    echo -e "IPaddr address that we will assign to the virtual bridge."
    echo -e "Options: 
                    -h/help/--help: Info about Script
                    -i/install: package contains utilities for configuring Ethernet bridge
                    -d/delete: Delete  network bridge
                    --build/build: Create network bridge
            "
    echo -e "Example: sudo bash creating_bridge --build/build enp4s0 192.168.127.200\n"

    exit $HELP
}


function bridge_package {
    if ! grep -i bridge-utils <(dpkg -l) &>/dev/null; then
        apt install bridge-utils
    else
        echo -e "The latest version of Bridge-utils package $(brctl --version) is already installed"
    fi
}


function configure_physical_ethinterface {
    if [[ -n $DEV_NAME ]]; then
        ip addr add "0.0.0.0" dev $DEV_NAME
        ip link set dev $DEV_NAME promisc on
        echo -e "$DEV_NAME setup complete\n IP: 0.0.0.0 \n Mode On: promisc"
    fi
}


function create_bridge {
    if [[ -n $(awk '{print $1}' <(nmcli con | grep -i bridge-br0)) ]]; then
        echo "Сonnection br0 already created"
        exit $ALREADY_CREATED
    fi

    nmcli con add type bridge \
          con-name bridge-br0 \
          ifname br0 \
          ipv4.method manual \
          ipv4.addresses $IP/24 \
          ipv6.method disabled

    brctl addif br0 $DEV_NAME
}


function check {
    nmcli con show | grep -i br0
    ip a | grep -i br0 && echo
    brctl show && echo
    ping -c 1 $IP
}


function delete_bridge {
    nmcli connection delete bridge-br0
    nmcli device delete br0
} &>/dev/null



case "$1" in
    "help"|"-h"|"--help" ) help_use ;;
    "-i"|"install" ) bridge_package ;;
    "-d"|"delete" ) delete_bridge ;;
    "--build"|"build" )
        configure_physical_ethinterface
        create_bridge
        check
        ;;
    * ) help_use && exit $NOT_FOUND_VALID_FLAGS ;;
esac