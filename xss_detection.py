import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from colorama import Fore, Style
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO)

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}

    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan_xss(url, payload):
    forms = get_all_forms(url)
    logging.info(f"{Fore.CYAN}[+] Detected {len(forms)} forms on {url}.{Style.RESET_ALL}")
    js_script = f"<script>{payload}</script>"
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()

        if js_script in content:
            logging.info(f"{Fore.GREEN}[!!] XSS Detected on {url}{Style.RESET_ALL}")
            logging.info(f"{Fore.GREEN}[*] Form details:{Style.RESET_ALL}")
            pprint(form_details, indent=2)
            is_vulnerable = True
        else:
            logging.info(f"{Fore.RED}[-] No XSS Detected on {url}{Style.RESET_ALL}")
            logging.info(f"{Fore.RED}[*] Form details:{Style.RESET_ALL}")
            pprint(form_details, indent=2)

    return is_vulnerable

def main():
    parser = argparse.ArgumentParser(description="XSS Scanner")
    parser.add_argument("-u", help="Target URL")
    args = parser.parse_args()

    xss_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "xss-data", "xss-payload-list.txt")
    total_payloads = 0
    successful_payloads = 0

    with open(xss_file, 'r') as file:
        for line in file:
            payload = line.strip()
            url = f"{args.u}/?q={payload}"
            total_payloads += 1

            if scan_xss(url, payload):
                successful_payloads += 1

    logging.info(f"\n{Fore.YELLOW}Summary:{Style.RESET_ALL}")
    logging.info(f"{Fore.CYAN}Total Payloads Tested: {total_payloads}{Style.RESET_ALL}")
    logging.info(f"{Fore.GREEN}Successful Payloads (XSS Detected): {successful_payloads}{Style.RESET_ALL}")
    logging.info(f"{Fore.RED}Payloads that Didn't Trigger XSS: {total_payloads - successful_payloads}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
