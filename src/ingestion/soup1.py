from bs4 import BeautifulSoup
html_cont = "<p>Hello <b>World</b></p>"

soup = BeautifulSoup(html_cont, "html.parser")
clean_text = soup.get_text()
print (clean_text)