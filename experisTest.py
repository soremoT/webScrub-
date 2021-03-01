import requests
import sys
from bs4 import BeautifulSoup
import tkinter as tk


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


def primary(name,label):
    URL = 'https://www.imdb.com/find?q=' + name.strip() + '&s=tt&ttype=ft&ref_=fn_ft'
    file = open(name + ".txt", "w")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td' ,class_='result_text')

    if results is None:  #search didn't find a single movie
        file.close()
        sys.exit()

    imdb = 'https://www.imdb.com'
    for movie in results :
        if check_name(name,movie):#name of movie 
            if "in development"  in movie.contents[2]  :#check for in devolpment tag before making a get request
                continue
            page= requests.get(imdb+movie.find('a')['href'])#get specific movie URL
            soup = BeautifulSoup(page.content, 'html.parser')
            file.write(movie.find('a').contents[0] + get_info(soup) + "\n")

    file.close()
    label.config(text = "File is ready")     
def center_GUI(root):
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
def gui_input(root):
    center_GUI(root)
    var = tk.StringVar()
    # create the GUI
    label = tk.Label(root,font=22,fg="#0000FF", text="Enter Movie Name")
    entry = tk.Entry(root, textvariable=var )
    
    label2=tk.Label(root,font=22,fg="#0000FF", text="press Enter or search button")
    label2.pack(side="bottom", padx=(20, 20), pady=20)
    
    label.pack(side="top", padx=(20, 0), pady=20)
    entry.pack(side="bottom", fill="x", padx=(20, 20), pady=20, expand=True)
    
    btn1= tk.Button(root,command=lambda: primary(var.get(),label), height=1, width=10, text="search")
    btn1.pack()
    btn2= tk.Button(root,command=lambda: root.destroy(), height=1, width=10, text="close")
    btn2.pack()
    root.bind('<Return>', lambda event: primary(var.get(),label))

    root.mainloop()
    name = var.get()
    return name

root = tk.Tk()
gui_input(root)





