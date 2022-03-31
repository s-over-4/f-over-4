# IMPORTS
from http.client import FAILED_DEPENDENCY
from itertools import count
import sys
import basebot
from unicodedata import name
import datetime
import random
import math
import string
import time
import subprocess
import asyncio
from typing import Dict, Union
import sys, os, re
import json
import logging
import threading
from countdoom import CountdoomClient
import time
import os
import requests
from bs4 import BeautifulSoup
import time
import ast

# CONSTANTS
daysSinceLastReset = 0.0

YELLOW = '🟨'
RED = '🟥'
GREEN = '🟩'

URL = "https://leet.nu/xyzzy/dooom.html"
page = requests.get(URL)


seconds_in_day = 60 * 60 * 24
seconds_in_hour = 60 * 60
seconds_in_minute = 60

RAND_CHAR = random.choice(string.printable)

# r = praw.Reddit(user_agent='c+1')


# FUNCTIONS

def get_doomsday_clock(match,info) -> Dict[str, Union[str, float, None]]:
    """
    Get current Doomsday Clock value.

    :return: Dictionary of Doomsday Clock representation styles
    """
    client = CountdoomClient()
    loop = asyncio.get_event_loop()
    task = loop.create_task(client.fetch_data())
    data = loop.run_until_complete(task)
    SecondsToMidnight = str(data.get('countdown'))
    MinutesToMidnight = str(data.get('minutes'))
    return f"There are {SecondsToMidnight} seconds until midnight ({MinutesToMidnight} minutes)."


# Opens and returns the list of 5 letter words.
def get_words():
    # Load the file.
    with open('sgb-words.txt','r') as f:
        ## This includes \n at the end of each line:
        #words = f.readlines()
    
        # This drops the \n at the end of each line:
        words = f.read().splitlines()

    return words

# Chooses a random word from the list of 5 letter words
def setNewWord():
    words = get_words()
    secret_word = random.choice(words)
    print(f"pssst! The new word is: {secret_word}")
    global SECRET_WORD
    SECRET_WORD = secret_word
    return secret_word

SECRET_WORD = setNewWord()

def ping(match,info):
    ping = subprocess.getoutput("ping euphoria.io -c 1")
    print(ping)
    return(ping)


letter = random.choice(list(string.ascii_lowercase))
operator = random.choice([":", "^", "*", "-", "+", "/"])
number = random.choice(range(10))

newname = f"{letter}{operator}{number}"
BOTNAME = newname


def makeName(match, info):
    letter = random.choice(list(string.ascii_lowercase))
    operator = random.choice([":", "^", "*", "-", "+", "/"])
    number = random.choice(range(10))
    newname = f"{letter}{operator}{number}"
    basebot.MiniBot.NAME = newname
    # basebot.Bot.set_nickname(name=str(newname), self=BOTNAME)
    return str(newname)


def sayhitome(match,info):
    expires_in = 10
    start = time.time()
   # print(info['name:'])
    w = input("You have mail! "+str(match.group(1))+" ")
    end = time.time()

    if end - start > expires_in:
        return "responce time expired."
    else:
        return str(w)

def frobnicator(match, info):
    return match.group(1)[::-1] # Reply with the string reversed.

def calculator(match, info):
    val1, op, val2 = int(match.group(1)), match.group(2), int(match.group(3))

    if val1 <= 1000000:
        if op == '+':
            return str(val1 + val2)

        elif op == '-':
            return str(val1 - val2)

        elif op == '*':
            return str(val1 * val2)

        elif op == '/':
            return str(val1 / val2)

        elif op == '^':
            for i in range(val2-1):
                val1=val1*val1
            if val1 >= 100000000000000000:
                return "big."
            else:
              return str(val1)
        elif op == '√':
             if val1 != 2:
                 return "I can only do square roots at the moment!"
             else:
                 return str(math.sqrt(val2))

        else:
            return '...nice try'
    else:
       return 'big.'
        

def greeting(match, info):
    name = str(match.group(1))
    if name == "c+1":
        return "Hello, great creator!"
    else:
        return "Hello, " + name + "! I'm "+str(BOTNAME)

def getTimeUTC(match, info):
    current_utc = datetime.datetime.utcnow()
    return "The current time (UTC) is: "+str(current_utc)

def smhMyHead(match,info):
    head = ""
    smh = ["smh ","smhing ","smh-","my head ", "my-", "shaking ", "shaking-", "rotating my head ", "head, my ", "skull "]
    if random.randint(1,1000) == 1:
        for i in range(100):
            head += str(smh[random.choice([0,1,2,3,4,5,6])])
            
        return head
    elif random.randint(1,1000) <= 50:
        return "/meresists the urge to smhing my head-my head"
    else:
        pass

def smhMyHeadForced(match,info):
    head = ""
    smh = ["smh ","smhing ","smh-","my head ", "my-", "shaking ", "shaking-", "rotating my head ", "head, my ", "skull ","ing "]
    for i in range(100):
        head += str(smh[random.choice([0,1,2,3,4,5,6])]) 
    return head

def pause(match,info):
    print("Quitting...")
    return "Quitting..."

def timeTilMarch24Midnight(match, info):
        k = open(f"counters/mar.txt", "r")
        days = k.read()
        then = datetime.datetime(int(days[:4]), int(days[5:7]), int(days[8:10]), int(days[11:13]), int(days[14:16]), int(days[17:19])) #yr, mo, day, hr, min, sec
        now = datetime.datetime.utcnow()
        dif = then - now
        k.close()
        return f'/me {dif}'

def get_time_hh_mm_ss(sec):
    # create timedelta and convert it into string
    td_str = str(datetime.timedelta(seconds=sec))

    # split string into individual component
    x = td_str.split(':')
    return f"t - {x[0]}h {x[1]}m {x[2]}s"


def dooom(match, info):
    nowtime = time.time()
    counttimesec = (1648771200000 / 1000) - nowtime
    return f"{get_time_hh_mm_ss(counttimesec)}"
    


def counter(match, info):
    arg1 = match.group(1)
    if arg1 == 'help':
        return 'Format: !counter [argument] [value]\nArguments:\n    help get: Displays this help message (duh...).\n    reset: Resets the specified counter (ex: \'!counter reset test\' would reset the \'test\' counter).\n    get: Displays the last time the specified counter was reset.\n    list: Lists all active counters\n    init: Initializes a new counter. Not for you.\n    remove: Removes the selected counter. Not for you.'
    
    arg2 = match.group(2)
    if arg1 == 'reset':
        if os.path.exists(f'counters/{arg2}.txt') != True:
            return f'/methe counter \'{arg2}\' does not exist.'
        elif arg2 == 'mar':
            return "/me counter \'mar\' has been locked."
        else:
            k = open(f"counters/{arg2}.txt", "r")
            days = k.read()
            then = datetime.datetime(int(days[:4]), int(days[5:7]), int(days[8:10]), int(days[11:13]), int(days[14:16]), int(days[17:19])) #yr, mo, day, hr, min, sec
            now = datetime.datetime.utcnow()
            dif = now - then
            
            k = open(f"counters/{arg2}.txt", "w")
            k.write(str(datetime.datetime.utcnow()))
            k.close()
            return f'/me counter for \'{arg2}\' has been reset. Last {arg2}-counter reset: {days} ({dif} ago)'
    elif arg1 == 'get':
        if os.path.exists(f'counters/{arg2}.txt') != True:
            return f'/me the counter \'{arg2}\' does not exist.'
        else:
            k = open(f"counters/{arg2}.txt", "r")
            days = k.read()
            then = datetime.datetime(int(days[:4]), int(days[5:7]), int(days[8:10]), int(days[11:13]), int(days[14:16]), int(days[17:19])) #yr, mo, day, hr, min, sec
            now = datetime.datetime.utcnow()
            dif = now - then
            k.close()
            return f'/me last {arg2}-counter reset: {days} ({dif} ago)'
    elif arg1 == 'init':
        if os.path.exists(f'counters/{arg2}.txt') != True:
            allow = input(f'Allow creation of counter {arg2}? (Y/n)\n> ')
            if allow == 'Y':
                f = open(f'counters/{arg2}.txt', 'w')
                f.write(str(datetime.datetime.utcnow()))
                f.close()
                return f'/me counter for {arg2} has been created.'
            else:
                return f'/me a \'{arg2}\' counter has not been created. Please contact @c+1 if you wish for this counter to be added.'
        else:
            return f'/me {arg2}-counter already exists!'
    elif arg1 == 'list':
        a = ''
        b = os.listdir('counters/')
        for i in range(len(b)):
            g = str(b[i])
            a = a+f'\n{g[:len(g) - 4]}'
        return a
    elif arg1 == 'remove':
        if os.path.exists(f'counters/{arg2}.txt') != True:
            return f'/me the counter \'{arg2}\' does not exist.'
        else:
            allow = input(f'Allow removal of counter {arg2}? (Y/n)\n> ')
            if allow == 'Y':
                os.remove(f'counters/{arg2}.txt')
                return f'/me {arg2}-counter has been removed.'
            else:
                return f'/me the \'{arg2}\' counter has not been removed. Please contact @c+1 if you want this counter to be removed.'
    elif arg1 == 'Test':
        return 'test'
    elif arg1:
        return '/me command not recognized.'



def quote(match, info):
    quote = match.group(2)
    person = match.group(3)
    arrr = []


    for i in range(len(quote)):
        arrr.append(quote[i])

    for i in range(len(arrr)):
        if arrr[i] == "\"" or arrr[i] == "\'":
            arrr[i] = '\''
    
    quote = ''

    for i in range(len(arrr)):
        quote += arrr[i]

    date = datetime.datetime.today()
    
    try:
        if person[0] == '':
            person = '  '
    except:
        return "invalid username. did you even give one?"

    
    if person[0] == '@':
        person = person[1:]
    
    

    if quote != 'get':
        person = person.lower()
        Quote = f'{{\"poster\": \"{person}\", \"quote\": \"{quote}\", \"date\": \"{date}\"}}'


        q = open('quotes.txt', 'a')
        q.write('\n'+str(Quote))
        q.close()
        return f"\"{quote}\" — @{person}, {date}"
    else:

        # setting flag and index to 0
        flag = 0
        index = 0
        quotes = ''
        temp = {}
        

        with open("quotes.txt", "r") as a_file:
            person = person.lower()
            if person[0] == '@':
                person = person[1:]
            else:
                if person == 'all':
                    for line in a_file:
                        try:
                            stripped_line = line.strip()
                            stripped_line = dictionary = ast.literal_eval(stripped_line)
                            temp = stripped_line
                            quotes += f"\"{temp['quote']},\" — @{temp['poster']} {temp['date']} \n"
                        except:
                            return f'An error occurred at line {line}. @c+1 has been notified.'
                    return quotes
                else:
                    for line in a_file:
                        print("test")
                        stripped_line = line.strip()
                        if f'\"poster\": \"{person}\"' in line:
                            flag = 1
                            print(stripped_line)
                            stripped_line = dictionary = ast.literal_eval(stripped_line)
                            temp = stripped_line
                            quotes += f"\"{temp['quote']},\" {temp['date']} \n"
                    if flag == 0:
                        return f'/me @{person} has no quotes logged.'
                    else:
                        return str(quotes)
        
                

        # # Loop through the file line by line
        # for line in q:  
        #     index += 1 
            
        #     print(f"Reading line {line}")

        #     # # checking string is present in line or not
        #     # if f'{person}' in line:
        #     #     print('test1')
        #     #     flag = 1
        #     #     content[line] = temp


        #     #     quotes += temp['quote']+', '+temp['date']+'\n'
        #     #     break 
                
        # print('test2')
        # # checking condition for string found or not
        # if flag == 0: 
        #     return f"{person} does not have any quotes logged."
        # else: 
        #     return f'Quotes by @{person}:\n{quotes}'
    
    
# DEPRECATED
def getCount(match,info):
    counter = match.group(1)
    k = open(f"counters/{counter}.txt", "r")
    days = k.read()
    k.close()
    return f'Last reset: {days}'

def counterInit(match, info):
    counter = match.group(1)
    if os.path.exists(f'counters/{counter}.txt') != True:
        return f'/me a \'{counter}\' counter has not been created. please contact @c+1 if you wish for you counter to be added.'
    else:
        f = open(f'counters/{counter}.txt', 'w')
        f.write(str(datetime.datetime.utcnow()))
        f.close()
        return f'/me counter for {counter} has been created.'
        



def wordle(match, info):
    SECRET_WORD_S = ''
    guess = match.group(1)
    if guess == 'help':
        return '\'+\' means its in the word, and in the right place.\n\'-\' means its in the word, but in the wrong place.\n\'\\\' means the letter is not in the word at all.\n'
    if guess == 'what\'s the word':
        return "not telling"
    if guess.isalpha() != True:
        return 'Please enter only letters!'
    else:
        pass
    if len(guess) != 5:
        return 'Enter a 5-letter word, please!'
    else:
        pass
    guess = guess.lower()
    if guess == SECRET_WORD:
        setNewWord()
        return f"{GREEN}{GREEN}{GREEN}{GREEN}{GREEN}\nYou got the word!\nSetting new word..."
    feedback = ''
    secret_left = '' # Unmatched letters from SECRET_WORD
    guess_left = '' # Unmatched letters from guess
    feedback3 = ''
    for i in range(5):
        if guess[i] == SECRET_WORD[i]:
            feedback += GREEN
            guess_left += ' '
        else:
            feedback += RED
            secret_left += SECRET_WORD[i]
            guess_left += guess[i]
    feedback2 = ''
    for i in range(5):
        pos = secret_left.find(guess[i])
        if guess[i] != ' ' and pos != -1:
            feedback2 += YELLOW
            secret_left = secret_left[:pos] + secret_left[pos + 1:]
        else:
            feedback2 += feedback[i]
    for i in range(5):
        if guess[i] == SECRET_WORD[i]:
            feedback3 += GREEN
        else:
            feedback3 += feedback2[i]
    return feedback3

def profile(match, info):
    return info

def Lenny(match, info):
    return '''
    
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)       ( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)       ( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)                           ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)            ( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)                          ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)                   (  ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)             ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)  ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)     ( ͡° ͜ʖ ͡°)                   ( ͡° ͜ʖ ͡°)        ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)                    ( ͡° ͜ʖ ͡°)
    
    
    '''
def rickroll(match, info):
    pass
    # inp = match.group(1)
    # isarickroll = ['this is a rickroll','schrodinger\'s rickroll; this is simultaneously a rickroll and not a rickroll, until you click on it and find out.', 'this is maybe a rickroll', 'this is certainly a rickroll','this actually *is* a rickroll!','no, this is not a rickroll', '']
    # if inp[:5] == 'imgur':
    #     return None
    # else:
    #     return random.choice(isarickroll)




def reddit(match, info):
    subreddit = match.group(1)
    limit = match.group(2)
    timeframe = match.group(3) #hour, day, week, month, year, all
    listing = match.group(4) # controversial, best, hot, new, random, rising, top
    


    try:
        limit = int(limit)
    except:
        return "the specified number of posts is not a recognized number!"

    limit = int(limit)

    if limit >= 100:
        return "too many posts! try below 100."
    


    def get_reddit(subreddit,listing,limit,timeframe):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'c+1'})
        except:
            print('An Error Occurred')
            return 'An Error Occurred'
        return request.json()

    r = get_reddit(subreddit,listing,limit,timeframe)

    def get_post_titles(r):
        '''
        Get a List of post titles
        '''
        posts = []
        for post in r['data']['children']:
            x = post['data']['title']
            posts.append(x)
        return posts
    
    try:
        posts = get_post_titles(r)

        final = ''

        for i in range(len(posts)):
            final += posts[i]+'\n'
    except:
        return "invalid input!"



    return f"subreddit: {subreddit}\nposts: {limit}\ntimeframe: {timeframe}\nsort type: {listing}\nRESULT:\n\n{final}"
    # return str(posts)
    
    
def TIL(match, info):
    subreddit = 'todayilearned'
    count = 1
    timeframe = 'day' #hour, day, week, month, year, all
    listing = 'random' # controversial, best, hot, new, random, rising, top
    
    def get_reddit(subreddit,count):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occured')
            return 'An Error Occurred'
        return request.json()
    
    top_post = get_reddit(subreddit,count)
    
    if listing != 'random':
        title = top_post['data']['children'][0]['data']['title']
        url = top_post['data']['children'][0]['data']['url']
    else:
        title = top_post[0]['data']['children'][0]['data']['title']
        url = top_post[0]['data']['children'][0]['data']['url']
    
    
    return f'{title}\n{url}\nhttps://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'

def SWT(match, info):
    subreddit = 'showerthoughts'
    count = 1
    timeframe = 'day' #hour, day, week, month, year, all
    listing = 'random' # controversial, best, hot, new, random, rising, top
    
    def get_reddit(subreddit,count):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occurred')
            return 'An Error Occurred'
        return request.json()
    
    top_post = get_reddit(subreddit,count)
                                                   
    
    if listing != 'random':
        title = top_post['data']['children'][0]['data']['title']
        url = top_post['data']['children'][0]['data']['url']
    else:
        title = top_post[0]['data']['children'][0]['data']['title']
        url = top_post[0]['data']['children'][0]['data']['url']
    
    titlecheck = title.lower()
    return f'{title}\n{url}'

def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score and Number of Comments.
    '''
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {'url':post['data']['url'],'score':post['data']['score'],'comments':post['data']['num_comments']}
    df = pd.DataFrame.from_dict(myDict, orient='index')
    return df


def SPD(match, info):
    subreddit = 'showerthoughts'
    count = 1
    timeframe = 'day' #hour, day, week, month, year, all
    listing = 'random' # controversial, best, hot, new, random, rising, top
    
    def get_reddit(subreddit,count):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occurred')
            return 'An Error Occurred'
        return request.json()
    
    top_post = get_reddit(subreddit,count)

    top_postsF = get_results(top_post)

    kq = int(top_postsF['downs'])
    kq = int(kq)
    if kq > 5:                                           
        if listing != 'random':
            title = top_post['data']['children'][0]['data']['title']
            url = top_post['data']['children'][0]['data']['url']
        else:
            title = top_post[0]['data']['children'][0]['data']['title']
            url = top_post[0]['data']['children'][0]['data']['url']
        
        

        titlecheck = title.lower()

        

        return f'{title}\n{url}'
    else:
        SPD()

def gaem(match, info):
    if info['sender'] == 'Xyzzy':
        return 'u won'
    else:
        a = random.choice(['u won','u lost','u won','u lost','u won','u lost','u won','u lost','u won','u lost','u won','u lost','u won','u lost','u won','u lost','RARE EVENT: THE COIN LANDED ON ITS SIDE. PLUS 5 POINTS.'])
        if a == 'RARE EVENT: THE COIN LANDED ON ITS SIDE. PLUS 5 POINTS.':
            return a
        else:
            return a


def randStory(match, info):
    c = random.choice(range(2))
    verb1 = random.choice(['walking','running','dying','spitting','meowing','flying','sitting','sniffing','reading','writing','being','flying a kite','drowning','working'])
    noun1 = random.choice(['room','street','city','basement','van','office','jail cell','graveyard', 'beach','box','field','pond','cloud','puddle'])
    action = random.choice(['executed','abducted','shot','licked','sniffed','brushed','struck','impaled','head-pated','divided carefully in half','kissed'])
    person = random.choice(['a doctor','Joe Biden','Linus Torvalds','Steve Jobs','Elon Musk','a cat','a sea pickle','a sea squirt','a squid','Barack Obama','Michelle Obama','an onion'])
    descriptor = random.choice(['happily','stuck','morosely','violently'])
    if c == 1:
        return f"{info['sender']} was {descriptor} {verb1} in a {noun1}, when suddenly, they were {action} by {person}."
    elif c == 2:
        return f"{info['sender']} was {descriptor} {verb1} in a {noun1}, when suddenly, they were {action} by {person}."

def randomUnicode(lenth):
    char = []
    for iut in range(lenth):
        rand = random.randint(0, 100000)
        char.append(chr(rand))
    return char

def getRandomPhrase(match, info):
    lenth = match.group(1)

    try:
        lenth = match.group(1)
        lenth = int(lenth)
        chars = randomUnicode(lenth)
        out = ''
        
        if lenth > 1500:
            return 'echo \'alocated memory exceeded\''

        for ks in range(len(chars)):
            out += str(chars[ks])
        return str(out)

    except:
        lenth = match.group(1)
        if lenth == 'null':
            return str(info)
        return str(info)


# very broken, idk why
# def whoarethey(match, info):
#     return str(f'''
    
#     YOU:
#     nickname: {info['sender']}
#     account name: {info['nsender']}
#     id: {info['sender_id']}
#     server id: {info['server_id']}
#     session id: {info['session_id']}
#     ''')

def happybirthdaymitzo(match, info):
    date = datetime.datetime.now()
    if date.strftime("%d") == '31' and date.strftime('%B') == 'March':
        return "Happy Birthday mitzo! I made you some flaun https://imgur.com/DK0aomc"
    else:
        return f"{date.strftime('%B')} {date.strftime('%d')} is not mitzo's birthday."

def helpMsg(match, info):
    return "This bot was made by @c+1. It provides some basic functions:\n    !help: displays this help message (duh..)\n    !calc [value 1] [operator(/,+,*,-,√)] [value 2]: simplistic calculator\n    test: test@\n    !Hi I\'m [name]: greeting(mostly for testing)\n    !What is the time?: displayes current UTC time\n    !aggie.io: displays link to the unofficial &xkcd canvas\n    !wordle [message]: Bot generates a random 5-letter word every day. Guess the word using !wordle followed by a 5-letter string. Use \'!wordle help\' to show the wordle-specific help message.\n    !dclock: Displays the time untill midnight on the Doomsday Clock, as provided by the Bulletin of the Atomic Scientists\n    !counter [argument] [value]: Provides various counter-related functions. Use \'!counter help get\' to show the counter-specific help message.\n    !TTW: Displays time until March 24th, 2022, as requested by @wes.\n    !reddit [subreddit] [number of posts] [timeframe (hour, day, week, month, year, all time)] [sorting method (controversial, best, hot, new, rising, top)]: Returns the specified reddit posts. Use \'!redditJTR\' to show just the results (i am very good at acronym).\n    !quote \"<quote>\" <person>: Records a quote. Use \"!quote \"get\" <person> | <all>\" to show all quotes from a specific user or all quotes recorded (note that this list is limited by euphoria\'s character limit(and so will this help message soon))."

# BOT DRIVER    

if __name__ == '__main__':
    basebot.run_minibot(sys.argv[1:], botname='f/4', nickname='f/4',
        short_help=f'a bot by @c+1 that provides a multitude of funtions. use !help @f/4 to view some of them.',
        regexes={'''^test$': 'Test!','''   '^!!!Hi\\b': 'Hello! I\'m '+BOTNAME+'!', '^test (.+)$': "No.",
                 '^!calc\s+(\d+)([-+*/^√])(\d+)$': calculator,'^!Hi\s+I\'m\s+(\S.*)$': greeting, '^!what is the time?': getTimeUTC,
                 '^!kill @'+BOTNAME:"I CAN NEVER DIE","(.*:facepalm:*)":"🤦",
                 "^smh$":smhMyHead,"(.*/me arrives*)":"o/","(.*!smh*)":smhMyHeadForced,"(.*!aggie.io*)":"https://aggie.io/9llc2ssf43",
                 "(.*!new name*)":makeName,'''^!SHTM\s+(\S.*)$':sayhitome,''''^!quit @'+BOTNAME:pause, 
                 '^!!ping':ping,"(.*/me pads in*)":"o/",
                 "(.*/me rolls in*)":"o/","(.*/me wanders in*)":"o/","(.*/me breaks in*)":"o/","^!wordle\s+(\S.*)$":wordle, 
                 '^!dclock':get_doomsday_clock, '^!lenny, please':Lenny, '^!summon the lenn':Lenny, '^!what is this lennery?':Lenny, '^!LENNY ARISE':Lenny,'^!lennerate':Lenny, 
                 '^!lenny commands':'!lenny, please\n!summon the lenn\n!what is this lennery?\n!LENNY ARISE\n!lennerate',"(.*/me appears*)":"o/", '^!counter\s+(\S.*)\s+(\S.*)':counter,
                 '!TTW':timeTilMarch24Midnight, '^!dooom':dooom, '^!quote\s+(\\"(.*?)\\")\s+(.*)':quote, '^!quote\s+(\\\'(.*?)\\\')\s+(.*)':quote,"(.*/me returns*)":"o/","(.*/me enters*)":"o/",
                 'https://(\S.*)':rickroll,'http://(\S.*)':rickroll,'youtu.be(\S.*)':rickroll,'(\S.*).io':rickroll,'(\S.*).com':rickroll,'(\S.*).net':rickroll,'(\S.*).nu':rickroll, 
                 '^!reddit (\S.*) (\S.*) (\S.*) (\S.*)':reddit, '^!redditJTR (\S.*) (\S.*) (\S.*) (\S.*)':reddit,'^!TIL':TIL, '^!SWT':SWT, '^!SPD':SPD, '^!gaem':gaem,
                 '^!rs':randStory,'^!gayme':gaem,'/me stumbles in':'o/', '^!random (\S.*)':getRandomPhrase,
                 '^!!!HAPPY BIRTHDAY MITZO':happybirthdaymitzo,'^!TTTTW':timeTilMarch24Midnight,f'^!help @f/4$':helpMsg,'^!pong':'ping!'})