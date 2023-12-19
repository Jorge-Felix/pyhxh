import os
import argparse
import requests
from colorama import Fore, Style
from tqdm import tqdm
import socket
from urllib3.exceptions import NewConnectionError, MaxRetryError
from chardet.universaldetector import UniversalDetector

def detect_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']

def load_wordlist(wordlist_path):
    encoding = detect_encoding(wordlist_path)
    with open(wordlist_path, 'r', encoding=encoding) as file:
        return file.readlines()

def check_url(url, line):
    _url = f"{url}/{line.rstrip()}"
    response = requests.get(_url)

    status_colors = {
        200: Fore.GREEN,
        404: Fore.RED,
        500: Fore.LIGHTRED_EX,
        301: Fore.LIGHTYELLOW_EX,
        302: Fore.LIGHTMAGENTA_EX
    }

    status_messages = {
        200: "(Status: OK)",
        404: "(Status: Not Found)",
        500: "(Status: Internal Server Error)",
        301: "(Status: Moved Permanently)",
        302: "(Status: Found '302')"
    }

    status_color = status_colors.get(response.status_code, Fore.YELLOW)
    status_message = status_messages.get(response.status_code, f"(Status: {response.status_code})")

    tqdm.write(status_color + f"{_url}" + Style.RESET_ALL + status_message)

def main(url, wordlist_path):
    if url.endswith('/'):
        url = url.rstrip(url[-1])

    try:
        lines = load_wordlist(wordlist_path)

        for line in tqdm(lines, desc="Checking URLs", unit="URL", position=0, leave=True, ascii='░▒█'):
            check_url(url, line)

    except KeyboardInterrupt:
        print(Fore.RED + "You have stopped the code" + Style.RESET_ALL)
    except (socket.gaierror, NewConnectionError):
        print(Fore.RED + "Temporary failure in name resolution or failed to establish a new connection" + Style.RESET_ALL)
    except MaxRetryError as e:
        print(Fore.RED + f"Max retries exceeded with url: {e.request.url}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"RequestException: {e}" + Style.RESET_ALL)
    finally:
        print(Fore.CYAN + "The execution has finished" + Style.RESET_ALL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("It finds directories in web pages")
    parser.add_argument("-u", type=str, required=True, help="Target URL")
    parser.add_argument("-w", type=str, required=True, default="/wordlists/leakypaths.txt",
                        help="Wordlist name that must be in the wordlists directory")
    args = parser.parse_args()
    
    url = args.u
    wordlist = args.w
    wordlist_path = os.path.join("wordlists", wordlist)
    
    main(url, wordlist_path)
