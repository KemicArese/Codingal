import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init()

print(f'{Fore.CYAN} + "Welcome to the Sentiment Spy Section of Gaop" + {Style.RESET_ALL}')

user_name = input(f'{Fore.YELLOW}Enter your name: {Style.RESET_ALL}').strip()
if not user_name:
    user_name = "Mysterious Agent"

history = []

print (f'\n{Fore.GREEN}Hello {user_name}. {Style.RESET_ALL}')
print(f'{Fore.GREEN}I am here to analyze the sentiment of your messages using textblob.{Style.RESET_ALL}')
print(f'{Fore.GREEN}You can type {Fore.YELLOW}exit{Fore.GREEN} to end the conversation or {Fore.YELLOW}reset{Fore.GREEN}.{Style.RESET_ALL}')

while True:
    user_input = input(f'{Fore.YELLOW}>> {Style.RESET_ALL}').strip()
    
    if user_input.lower() == 'exit':
        print(f'{Fore.RED}Goodbye, {user_name}! Stay positive!{Style.RESET_ALL}')
        break
    elif user_input.lower() == 'reset':
        history.clear()
        print(f'{Fore.GREEN}Conversation history has been reset.{Style.RESET_ALL}')
        continue
    
    analysis = TextBlob(user_input)
    sentiment = analysis.sentiment.polarity
    
    if sentiment > 0.25:
        response = f'{Fore.GREEN}Your message is positive!{Style.RESET_ALL}'
    elif sentiment < -0.25:
        response = f'{Fore.RED}Your message is negative.{Style.RESET_ALL}'
    else:
        response = f'{Fore.YELLOW}Your message is neutral.{Style.RESET_ALL}'
    
    history.append((user_input, response, sentiment))
    
    print(f'{response}')
    print(f'{Fore.CYAN}📜 Conversation History:{Style.RESET_ALL}')
    for idx, (text, polarity, sentiment_type) in enumerate(history, start=1):
        if sentiment_type == "positive":
            color = Fore.GREEN
            emoji = "😊"
        elif sentiment_type == "negative":
            color = Fore.RED
            emoji = "😞"
        else:
            color = Fore.YELLOW
            emoji = "😐"
        print(f'{color}{idx}. {emoji} {text}  '  
              f'Polarity: {polarity}{Style.RESET_ALL}')
    continue

polarity = TextBlob (user_input).sentiment.polarity
if polarity > 0.25:
    sentiment_type = "Positive"
    color = Fore.GREEN
    emoji = "😊"
elif polarity < -0.25:
    sentiment_type = "Negative"
    color = Fore.RED
    emoji = "😞"
else:
    sentiment_type = "Neutral"
    color = Fore.YELLOW
    emoji = "😐"

history.append((user_input, polarity, sentiment_type))

print(f'{color}{emoji} {sentiment_type} Sentiment Detected!'
      f'(Polarity {polarity:.2f}) {Style.RESET_ALL}')