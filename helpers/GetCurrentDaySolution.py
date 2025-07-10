import datetime
import requests
from collections import Counter
import os
def get_today_solution(word =None):
    
    # Get today's date in YYYY-MM-DD format
    date = datetime.date.today()
    url = f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json"
    PATH = f"./answer_today/answer_{date:%Y-%m-%d}.txt"
    # Fetch the answer
    if word:
        pass
    elif not os.path.exists(f"./answer_today/answer_{date:%Y-%m-%d}.txt"):
        response = requests.get(url)
        data = response.json()
        word = data['solution'].strip().upper()
        with open(PATH,"w") as f:
            f.write(word)
    else:
        print("loading from disk")
        with open(PATH,"r") as f:
            word = f.readline()
            
    word_pos = [(letter,i) for i,letter in enumerate(word)]
    counts = Counter(word)
    
    return word,word_pos,counts

if __name__ == "__main__":
    _,_,counter = get_today_solution("NERVE")
    # counter["N"] -= 1
    print(set({letter:i for letter,i in counter.items() if i > 0}.keys()))
