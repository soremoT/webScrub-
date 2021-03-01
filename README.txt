The tool  uses pyhon version 3.7.9
First Install needed python version
also install request module 
install beautifulsoup4 module
also install pip3 module to install previuos mentioned modules

experisTest.py uses tkinter for a UI ,alternative option is webScrub.py with command line and input


windows:
https://www.python.org/downloads/windows/ (python version for windows)
python -m pip3 install requests
pip3 install beautifulsoup4
python experisTest.py(if cmd path is in folder)

Linux:
sudo apt-get install python3.8
sudo pip install requests
sudo apt-get install python3-bs4

run the experisTest.py in terminal or cmd with 
python experisTest.py (if u are inside the correct folder otherwise adjust the path) or python3 experisTest.py
and then enter the search term when prompted
enter movie name when asked and file should be produced


the tool finds movies with aka tag and check for that name as well 


(I didnt understand about the fuzzy search requirement at the moment the script only allowes
matches if exact strings are in the title and search ,as long as no critical changes happen on the imdb site the tool should work)
Bugs:when searching for star wars hope the returned html text of title abreviates it as "star wars" didnt find reason for it
as developer tool showed the full title so I guess its a bug...
returned text from HTML for :"star wars hope":
<td class="result_text"> <a href="/title/tt0076759/">Star Wars</a> (1977) </td>
returned html for :"a new hope":
<td class="result_text"> <a href="/title/tt0076759/">Star Wars</a> (1977) <br/>aka <i>"Star Wars: Episode IV - A New Hope"</i> </td>
when checking developer tools in both cases found:
<a href="/title/tt0076759/?ref_=fn_ft_tt_1">Star Wars: Episode IV - A New Hope</a>