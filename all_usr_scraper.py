import discum,webbrowser,os,pyfiglet
from colorama import Fore,Style

class Scraper:
    
    def __init__(self,token:str,proxy:str=None,log:bool=False):
        if proxy == None:
            self.bot=discum.Client(token=token,log={ "console": log,"file": False })
        else:
            self.bot=discum.Client(token=token,proxy=proxy,log={ "console": log,"file": False })
    
    def close_after_fetching(self,resp,guild_id):
        if self.bot.gateway.finishedMemberFetching(guild_id):
            lmembers=len(self.bot.gateway.session.guild(guild_id).members)
            print(f"{str(lmembers)} members fetched") #print numbers of members fetched
            self.bot.gateway.removeCommand({'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
            self.bot.gateway.close()
    
    def fetch_members(self,guild_id,channel_id,wait=1):
        self.bot.gateway.fetchMembers(guild_id,channel_id,keep='all',wait=wait)
        self.bot.gateway.command({'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
        self.bot.gateway.run()
        self.bot.gateway.resetSession()

        return self.bot.gateway.session.guild(guild_id).members

if __name__ == "__main__":
    if os.name == 'nt':    
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    print(Fore.LIGHTBLUE_EX)
    print(pyfiglet.figlet_format("Fla 's \nDiscord Scraper", font = "standard" ))
    print(Fore.YELLOW+"-"*72+Fore.LIGHTBLUE_EX+'\n')
    guild_id=str(input(Fore.LIGHTBLUE_EX+"Input guild id--> "+Fore.YELLOW))
    general_chat_id=str(input(Fore.LIGHTBLUE_EX+"Input general chat id--> "+Fore.YELLOW))
    token=str(input(Fore.LIGHTBLUE_EX+"Input token--> "+Fore.YELLOW))
    proxy=str(input(Fore.LIGHTBLUE_EX+"Input your proxy (ex: http://usr:pass@999.999.999.999:1111)/press enter to skip--> "+Fore.YELLOW))
    if len(proxy)>1:
        sc=Scraper(token,proxy)
    else:
        sc=Scraper(token)
    listofusrs=sc.fetch_members(guild_id,general_chat_id)
    usrstring=''
    for usr in listofusrs:
        usrstring+=usr+'\n'
    filename=f'userlist{guild_id}.txt'
    with open(filename, "w") as f:
        f.write(usrstring)
    print(f"user ids have been saved in {filename}")
    webbrowser.open(filename)
    print(Style.RESET_ALL)

