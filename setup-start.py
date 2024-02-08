"""
this is the set-up here the permissions are given and 
everyting is installed, PLS TRY NOT TO MODIFY THIS ONE

also this code has to be executed as sudo

you can check it deeply and you wont find dangerous actions

made by bigbudda :)
"""

from subprocess import call
import os
import stat
from colorama import Style, Fore
import sys


def main() -> None:
    files:list[str] = ['inst.sh', 'menu.sh']
    current_dir = os.getcwd()
    #Permisions for reading and writting
    all_permissions = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
    
    
    """
    Checking if the files are in the correct path.
    
    it they're not in correct path pls check the repository or
    reinstall the tool again from github
    
    """
    try:
        for file_name in files:
            file_path = os.path.join(current_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
    
    #Here the permissions are given
        for file_name in files:
            file_path = os.path.join(current_dir, file_name)
            os.chmod(file_path, all_permissions)
        
        
        del current_dir
        del files
        
        call(["./inst.sh"], shell=True)
        call(["./menu.sh"], shell=True)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the required files are in the current directory.")
    
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
    finally:
        sys.exit()
        
if __name__ == '__main__':
    main()

        
        
    
