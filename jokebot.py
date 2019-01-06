import time
import csv
import sys
import requests

def delivery(prompt, punch):
    print(prompt)
    time.sleep(2)
    print(punch)

def read_inp():
    inp = input("Enter a command: ")
    if inp == "next":
        return True
    elif inp == "quit":
        return False
    else:
        print("I don't understand")
        return read_inp()

joke_list = []
def read_jokes(csv_inp):
    with open(csv_inp) as csv_file:
        joke_reader = csv.reader(csv_file)
        for row in joke_reader:
            joke_list.append(row)
        return joke_list
#Assuming that the csv file provided ensures prompts don't have commas before the delimiter

def get_dad_jokes():
    r = requests.get('https://www.reddit.com/r/dadjokes.json', headers = {'User-agent': 'troysjokebot'})
    response = r.json()
    i = 0
    while True:
        try:
            title = response['data']['children'][i]['data']['title']
            body = response['data']['children'][i]['data']['selftext']
            over_18 = response['data']['children'][i]['data']['over_18']
        except IndexError:
            break
        if over_18 == False and title[0:4] == "Why " or title[0:5] == "What " or title[0:4] == "How ":
            joke_list.append([title, body])
        i += 1
    return joke_list

if len(sys.argv) == 2:
    read_jokes(str(sys.argv[1]))
elif len(sys.argv) == 1:
    get_dad_jokes()
else:
    print("Too Many Arguments!")
    exit()

if not joke_list:
    print("No Jokes Provided!")
    exit()

prompt, punch = joke_list[0]
delivery(prompt, punch)

i = 1
while read_inp():
    if i >= len(joke_list):
        print("Ran out of jokes!")
        time.sleep(1)
        break
    prompt, punch = joke_list[i]
    delivery(prompt, punch)
    i += 1

print("Shutting down Jokebot...")
