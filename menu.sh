#!/bin/bash

chmod +x *.py

#Ansi colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'


# Portscan function
function brute_port_scan() {
    read -p "Target IP: " IP
    read -p "Starting port: " SP
    read -p "Ending port: " EP
    python3 portscanner.py -i "$IP" -s "$SP" -e "$EP"
}

# DDOS FUNCTION 
function ddos_attack() {
    read -p "Target IP: " IP
    read -p "Target port: " PORT
    sudo python3 ddos.py -i "$IP" -p "$PORT"
}

# Package capturing function
function package_capturer() {
    read -p "Count: " COUNT
    read -p "Want a CSV output file? (y/n): " OUTPUT
    if [[ $OUTPUT == 'Y' || $OUTPUT == 'y' ]]; then
        sudo python3 packagecapturer.py -c "$COUNT" -o "$OUTPUT"
    else
        exit
    fi
}

# IPINFO Function
function ip_info() {
    read -p "[*] Enter IPInfo API: " API
    read -p "[*] Enter IP address: " IP
    COUNTRY=$(curl ipinfo.io/"$IP"/country?token="$API")
    REGION=$(curl ipinfo.io/"$IP"/region?token="$API")
    CITY=$(curl ipinfo.io/"$IP"/city?token="$API")
    LOCATION=$(curl ipinfo.io/"$IP"/loc?token="$API")
    ORGANIZATION=$(curl ipinfo.io/"$IP"/org?token="$API")
    POSTAL=$(curl ipinfo.io/"$IP"/postal?token="$API")

    echo -e "Country: $COUNTRY\nRegion: $REGION\nCity: $CITY\nLocation: $LOCATION\nOrganization: $ORGANIZATION\nPostal: $POSTAL"
}

function dirfinder(){
    read -p "URL to be explored: " URL
    echo -e "${RED}REMEMBER THAT THE WORDLIST HAVE TO BE IN THE WORDLISTS DIRECTORY${RESET}"
    sleep 1
    read -p "Wordlist name: " WORDLIST
    python3 dirfinder.py -u $URL -w $WORDLIST
}

function xss_detection(){

    read -p "URL to be analyzed: " URL
    echo -e "$URL is about to be analyzed..."
    sleep 2
    python3 xss_detection.py -u $URL

}

function sql_injection(){
    read -p "URL to be injected: " URL
    read -p "Threads (MANDATORY): " THREADS
    read -p "Wanna use proxy? (y/N): " PROXY
    
    echo -e "${RED}$URL is about to be analyzed...${RESET}"
    sleep 2
    
    if [[ $PROXY == 'Y' || $PROXY == 'y' ]];then
        python3 sql_injection.py -u $URL --threads $THREADS --use-proxy
        
    else 
        python3 sql_injection.py -u $URL --threads $THREADS
        
    fi

}


while true; do
    clear
    echo -e "${RED}__________        .__           .__       ${RESET}"
    echo -e "${BLUE}\______   \___.__.|  |__ ___  __|  |__    ${RESET}"
    echo -e "${RED} |     ___<   |  ||  |  \\  \/  /  |  \   ${RESET}"
    echo -e "${BLUE} |    |    \___  ||   Y  \>    <|   Y  \\ ${RESET}"
    echo -e "${RED} |____|    / ____||___|  /__/\_ \___|  /  ${RESET}"
    echo -e "${BLUE}           \/          \/      \/    \/   ${RESET}"
    echo -e "${GREEN}MADE BY BIGBUDDA${RESET}\n"
    sleep 1
    echo -e "${RED}FOR USING THIS PROGRAM YOU MAY NEED SOME APIs${RESET}\n"
    sleep 2
    PS3='ENTER YOUR CHOICE >> '
    options=('[*] BRUTE PORT SCAN [*]' '[*] DDOS [*]' '[*] PACKAGE CAPTURER [*]' '[*] IP INFO [*]' '[*] FAKE IDENTITY [*]' '[*] DIRFINDER [*]' '[*] XSS DETECTION [*]' '[*] SQL INJECTION [*]' '[*] EXIT [*]')

    select opt in "${options[@]}"
    do
        case $opt in
            "[*] BRUTE PORT SCAN [*]") brute_port_scan;;
            "[*] DDOS [*]") ddos_attack;;
            "[*] PACKAGE CAPTURER [*]") package_capturer;;
            "[*] IP INFO [*]") ip_info;;
            "[*] FAKE IDENTITY [*]") python3 fakeInfo.py;;
            "[*] EXIT [*]") exit;;
            "[*] DIRFINDER [*]") dirfinder;;
            "[*] XSS DETECTION [*]") xss_detection;;
            "[*] SQL INJECTION [*]") sql_injection;;
            
        esac
        read -n 1 -s -r -p "Press 'c' to continue..."
        clear
        break  # end of the bucle
    done
done
