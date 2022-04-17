import discum,os,pyfiglet
from colorama import Fore,Style

class TokenTester:
    def __init__(self,log=False) -> None:
        self.bot=discum.Client(log={"console": log,"file": False})
        self.total_working_on_tested=0

    def get_tokens(tokens_txt:str=None,tokens_sql_str:str=None):
        if tokens_txt == None and tokens_sql_str == None:
            raise ValueError("No tokens were given.")
        elif tokens_txt != None:
            with open(tokens_txt,'r') as f:
                tokens=f.read().splitlines()
            return tokens
        elif tokens_sql_str != None:
            tokens=tokens_sql_str.split(':O')
            tokens=["O"+t[:58] for t in tokens[1:]] #add O again since we removed it| first split is gonna be an email so we remove it
            return tokens
        else:
            raise ValueError("Error 100, something went wrong, tokens couldn't be loaded")

    def test_token(self,token:str):
        result=self.bot.checkToken(token)
        if result[0] == True and result[1] == True:
            self.total_working_on_tested+=1
            return True
        else:
            return None
    
    def test_tokens(self,token_list:list,results_file:str=None,method:str='w'):
        """Command to get working tokens from a list, results_file has only working tokens inside of it and if non existing will be created in the working directory"""
        working_tokens=[]
        broken_tokens=[]
        print("Testing tokens...")
        for token in token_list:
            result=self.test_token(token)
            if result == True:
                working_tokens.append(token)
            else:
                broken_tokens.append(token)
        if results_file != None:
            tokens_string="\n".join(working_tokens)
            try:
                with open(results_file,method) as f:
                    f.write(tokens_string)
                    print(f"results have been saved in {results_file}")
            except Exception:
                raise ValueError("Something went wrong while writing the file.")
        return working_tokens,broken_tokens
    
    def test_tokens_from_file(self,token_file:str,results_file:str=None,method:str='w'):
        """Command to get working tokens from a file, results_file has only working tokens inside of it and if non existing will be created in the working directory"""
        with open (token_file,'r') as f:
            token_list=f.read().splitlines()
        working_tokens=[]
        broken_tokens=[]
        print("Testing tokens...")
        for token in token_list:
            result=self.test_token(token)
            if result == True:
                working_tokens.append(token)
            else:
                broken_tokens.append(token)
        if results_file != None:
            tokens_string="\n".join(working_tokens)
            try:
                with open(results_file,method) as f:
                    f.write(tokens_string)
                    print(f"results have been saved in {results_file}")
            except Exception:
                raise ValueError("Something went wrong while writing the file.")
        return working_tokens,broken_tokens

if __name__ == "__main__":
    tt=TokenTester()
    if os.name == 'nt':    
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    print(Fore.LIGHTBLUE_EX)
    print(pyfiglet.figlet_format("Fla 's \nToken Tester", font = "standard" ))
    print(Fore.YELLOW+"-"*55+Style.RESET_ALL+'\n')
    mode=int(input(Fore.LIGHTBLUE_EX+"Press 1 to test a single token or 2 to test multiple tokens from a file--> "+Fore.YELLOW))
    if mode == 1:
        try:
            result=tt.test_token(input(Fore.LIGHTBLUE_EX+"Input the token--> "+Fore.YELLOW))
            print(Fore.GREEN +"WORKING" if result == True else Fore.RED +"NOT WORKING")
        except Exception:
            print("Invalid syntax.")
        
    elif mode == 2:
        token_file_path=input(Fore.LIGHTBLUE_EX+"Input the token file path, must be a txt with a token for each line--> "+Fore.YELLOW)
        results_file_path=input(Fore.LIGHTBLUE_EX+"Input the result file name, must be a txt file or press enter to continue without saving the results--> "+Fore.YELLOW)
        if len(results_file_path)>1:
            method=input(Fore.LIGHTBLUE_EX+"Input the method to write the file. type w/a --> "+Fore.YELLOW)
            tt.test_tokens_from_file(token_file_path,results_file_path,method=method)
        else:
            results=tt.test_tokens_from_file(token_file_path)
            print(Style.RESET_ALL+Fore.GREEN)
            print(f"{len(results[0])} wokring tokens:{results[0]}{Fore.RED}\n\n{len(results[1])}  non-working tokens:{results[1]}")
    print(Style.RESET_ALL)
