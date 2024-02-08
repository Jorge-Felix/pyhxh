#!/bin/bash


apt install -y python3 pip nmap curl || sudo apt-get install -y python3 pip nmap curl


if [ $? -eq 0 ]; then
    
    pip install -r requirements.txt

    
    if [ $? -eq 0 ]; then
        echo "Successfully installed :D"
    else
        echo "Something went wrong while installing Python packages :c"
    fi
else
    echo "Something went wrong while installing system packages :c"
fi
