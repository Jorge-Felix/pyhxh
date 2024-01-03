import re
import requests
import argparse
import os
import threading
from bs4 import BeautifulSoup
from colorama import Fore, Style

class SQLInjector:
    def __init__(self, url, num_threads=5, use_proxy=False, custom_headers=None):
        self.url = url
        self.num_threads = num_threads
        self.use_proxy = use_proxy
        self.custom_headers = custom_headers or {}
        self.lock = threading.Lock()
        self.results = []

    def detect_sql_injection(self, input_data, patterns):
        return any(pattern.search(input_data) for pattern in patterns)

    def test_sql_injection(self, form, initial_response, sql_payloads, sql_patterns):
        first_response_length = len(initial_response)
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name')
            if input_name:
                for payload in sql_payloads:
                    data = {input_name: payload}
                    response = requests.post(self.url, data=data, headers=self.custom_headers)
                    if self.detect_sql_injection(response.text, sql_patterns):
                        print(f"{Fore.GREEN}[+] Potential SQL injection detected in {input_name}: {payload}{Style.RESET_ALL}")

                        # Check if the response is different from the initial response
                        if response.text != initial_response:
                            print(f"{Fore.CYAN}[*] Detected different response:{Style.RESET_ALL}")
                            print(f"First response length: {first_response_length}")
                            print(f"Subsequent response length: {len(response.text)}")
                            print("Summary: Subsequent response is different from the first one.")
                            self.results.append({
                                'input_name': input_name,
                                'payload': payload,
                                'response_length_difference': len(response.text) - first_response_length
                            })

                    else:
                        print(f"{Fore.RED}[-] No SQL injection detected in {input_name}: {payload}{Style.RESET_ALL}")

    def scan_forms(self, sql_payloads):
        forms, initial_response = self.find_forms()
        sql_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in [
                r'\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)\b',
                r'\b(?:UNION(?:\s+ALL)?|AND|OR)\b',
                r"'",
                r'\b(?:DROP\s+TABLE|ALTER\s+TABLE|CREATE\s+TABLE)\b',
                r'\b(?:EXEC(?:UTE)?\s*\()|\b(?:DECLARE\s+@|\bCAST\s*\()',
                r'\b(?:xp_cmdshell|sp_executesql)\b',
                r'\b(?:WAITFOR\s+DELAY\s+\'\d{0,5}:\d{0,5}:\d{0,5}\')\b',
                r'\b(?:CONVERT|CONVERTTO|CONVERT_FROM)\b',
            ]
        ]

        threads = []
        for form in forms:
            thread = threading.Thread(target=self.test_sql_injection, args=(form, initial_response, sql_payloads, sql_patterns))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.results

    def find_forms(self):
        response = requests.get(self.url, headers=self.custom_headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        return forms, response.text

def main():
    parser = argparse.ArgumentParser(description="SQL Injection Tester for Web Forms")
    parser.add_argument("-u", "--url", help="URL of the target website", required=True)
    parser.add_argument("--threads", type=int, default=5, help="Number of threads for concurrent testing")
    parser.add_argument("--use-proxy", help="Use proxy for requests", action="store_true")
    args = parser.parse_args()

    url = args.url
    num_threads = args.threads
    use_proxy = args.use_proxy

    # You can add custom headers if needed
    custom_headers = {
        'Custom-Header': 'Header-Value',
    }

    sql_injector = SQLInjector(url, num_threads=num_threads, use_proxy=use_proxy, custom_headers=custom_headers)

    sql_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sql-data")
    
    results = []
    # Iterate through all .txt files in the sql-data directory
    for filename in os.listdir(sql_data_path):
        if filename.endswith(".txt"):
            sql_file = os.path.join(sql_data_path, filename)
            with open(sql_file, 'r') as file:
                sql_payloads = [line.strip() for line in file]

            result = sql_injector.scan_forms(sql_payloads)
            results.extend(result)

    print(Fore.CYAN + "[*] Summary:" + Style.RESET_ALL)
    print(results)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
    finally:
        print(Fore.BLUE + "The script has finished" + Style.RESET_ALL)
