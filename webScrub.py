import requests
from bs4 import BeautifulSoup


def get_director_and_stars(soup):
    director = "|"
    stars = "|"
    list = soup.find_all('div', class_ = 'credit_summary_item')
    for arg in list :
        tmp=arg.text
        if 'Director'  in tmp or 'Directors'  in tmp:
           director = "|"+ tmp.strip().split(':')[1].replace("\n","").split("|")[0]
        if 'Stars'  in tmp or'Star'  in tmp :
           stars = "|"+ tmp.strip().split(':')[1].replace("\n","").split("|")[0]
    return director + stars

def get_info(soup):#find all subinforation from vital part
    duration = "|"
    rating = "|"
    genre = "|"
    result = soup.find('div' ,class_='subtext')
    if result is None :
        return "|||"
    if result.find("time") is not None:
        duration= "|" + result.find('time').text.strip()
    rating = rating + result.contents[0].strip()
    a = soup.find('div' ,id = 'titleStoryLine')
    subtitle=[item.replace("\n","") for item in result.text.split("|")]
    if rating == "|" :
        if duration == "|":
            genre = "|" + subtitle[0]
        else:genre = "|" +  subtitle[1]
    else: genre = "|" + subtitle[2]
    return genre + rating + duration + get_director_and_stars(soup)
#check name function if the requirement for name is only for each word to exist in title
def check_aka(name,movie):
    if movie.find('i') is  None:
        return False
    a=name.split(' ')
    for i in a :
        if i.lower() in movie.find('i').contents[0].lower():
            continue
        else:return False
    return True    

def check_name(name ,movie):
    a=name.split(' ')
    for i in a :
        if i.lower() in movie.find('a').contents[0].lower() or check_aka(name,movie):
            continue
        else:return False
    return True


def primary(name):
    URL = 'https://www.imdb.com/find?q=' + name.strip() + '&s=tt&ttype=ft&ref_=fn_ft'
    file = open(name + ".txt", "w")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td' ,class_='result_text')

    if results is None:  #search didn't find a single movie
        file.close()
        quit()

    imdb = 'https://www.imdb.com'
    for movie in results :
        if check_name(name,movie):#name of movie 
            if "in development"  in movie.contents[2]  :#check for in devolpment tag before making a get request
                continue
            page= requests.get(imdb+movie.find('a')['href'])#get specific movie URL
            soup = BeautifulSoup(page.content, 'html.parser')
            file.write(movie.find('a').contents[0] + get_info(soup) + "\n")

    file.close()
    
primary(input("Enter Movie Name:"))