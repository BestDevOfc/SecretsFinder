import os
import re
import math

from src.templates import*
from src.find_entropies import FindEntropies

'''
1) gets high entropy strings
2) greps for common keywords that are sensitive and filters them out if there are too
    many results (like sometimes "password" will return 1000 results.)

    

    passsword_
    database_password
    _credentials
    credentials_
    secret_key
    api_key
    private_key

3) will also run trufflehog on the file path for secret keys, SSH keys, etc 

'''


def recursive_file_tree(directory):
    '''
    similar to recursive "-r" flags given to grep and other CLI commands.
    for entropy
    
    '''
    


    # recursively store file paths for the extract_high_entropy_strings() function
    file_paths: list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    
    print(f"Number of files we need to run self.extract_high_entropy_string() on {len(file_paths):,}")
    return file_paths

def grep_for(data: str, path: str, filter: bool = False):
    if filter == False:
        os.system(f"grep --color=always -Ri \"{data}\" {path} 2>/dev/null")
    else:
        '''
        
            this is for keywords that tend to return way too many results, such as 
            "password", as a result we make sure to put this limit on it:
            len >= 5 and len <= 140

            therefore, we'll still get perhaps hashes and 5 ensures we don't get output that's only one character or
            2 long.
        
        '''
        command = f'''grep --color=always -Ri "{data}" {path} | awk 'length($0) >= 5 && length($0) <= 140'  2>/dev/null'''
        os.system(command)

def entropy_finder_module(path: str):
    entropyFinder = FindEntropies()
    
    # is a directory, we need to extract all the file names first:
    file_paths: list = []
    if os.path.isdir( path ) == True:
        file_paths = recursive_file_tree(directory=path)
        input()
    
    entropy_strings = entropyFinder.extract_high_entropy_strings(path)
    
    if entropy_strings:
        print("High-entropy strings found:")
        for string in entropy_strings:
            # print(string)
            grep_for(string, path)
    else:
        print("No high-entropy strings found.")

def grepper_module(path: str):
    '''
    
        greps for sensitive keywords, and categorizes them based
        on whether they tend to give many false positives or not.
    
    '''
    # grep --color=always -Ri "jwt" /var/www | awk 'length($0) >= 5 && length($0) < 200'  2>/dev/null
    '''
    TODO:
        password w/ filtering + these new ones (need to do some testing on 
        'password'
        "password"
        password=
        password:
    '''    
    many_false_positives: list = [
        "password",
        "credential",
        "jwt"
    ]
    sensitive_keyword: list = [
        # these need the combination of '_' prefix and suffixes
        "database_password",
        "secret_key",
        "api_key",
        "private_key",
        
    ]
    
    print(f"ENTER to grep for: {Cols.YELLOW}{many_false_positives}")
    input('')
    for keyword in many_false_positives:
        grep_for(keyword, path, True)

    print(f"ENTER to grep for: {Cols.YELLOW}{sensitive_keyword}")
    input('')
    for keyword in sensitive_keyword:
        grep_for(keyword, path)
    

def main():
    clear_screen()
    print(f'''
          {Display.TITLE}
        {Display.LINE}

            {Cols.RED}[*] - {Cols.YELLOW} Which module would you like to run?
            {Cols.RED}[1] - {Cols.GREEN} Entropy Finder 
            {Cols.RED}[2] - {Cols.GREEN} Keywords Grepper

        {Display.LINE}''')
    option: int = int(input(">> ").strip().rstrip())
    
    clear_screen()
    path: str = input("Enter the path: ")
    
    # check if the path exists or not
    if os.path.exists( path ) == False:
        print(f"{Cols.GREEN} [!] - {Cols.RED}[ Path does not exist! ]")
        return

    # run the selected module:
    option_to_module: dict = {
        1: entropy_finder_module,
        2: grepper_module
    }
    option_to_module[ option ]( path )

if __name__ == "__main__":
    main()