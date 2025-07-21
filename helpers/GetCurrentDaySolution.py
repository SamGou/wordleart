import datetime
import requests
from collections import Counter
import os

def _API_write_word_to_disk(url,PATH,date):
    response = requests.get(url)
    data = response.json()
    word = data['solution'].strip().upper()
    with open(PATH,"w") as f:
        f.write("\n".join([f"{date:%Y-%m-%d}", word]))
            
def get_today_solution(word =None):
    
    # Get today's date in YYYY-MM-DD format
    date = datetime.date.today()
    url = f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json"
    PATH = f"./answer_today/answer.txt"
    # Fetch the answer
    if word:
        pass
    elif not os.path.exists(f"{PATH}"):
        _API_write_word_to_disk(url,PATH,date)
    else:
        with open(PATH,"r") as f:
            latest_date, word = f.readlines()
            if latest_date.strip() != f"{date:%Y-%m-%d}":
                _API_write_word_to_disk(url,PATH,date)
            else:
                pass
        
    word_pos = [(letter,i) for i,letter in enumerate(word)]
    counts = Counter(word)
    
    return word,word_pos,counts

if __name__ == "__main__":
    _,_,counter = get_today_solution()
    print(set({letter:i for letter,i in counter.items() if i > 0}.keys()))
