import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init()

print(f'{Fore.CYAN} + "Welcome to the Sentiment Spy Section of Gaop" + {Style.RESET_ALL}')

user_name + input = input(f'{Fore.YELLOW}Enter your name: {Style.RESET_ALL}').strip()
if not user_name:
    user_name = "Sentiment spy"