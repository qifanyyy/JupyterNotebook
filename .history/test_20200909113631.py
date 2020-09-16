import bs4
import requests


response = requests.get("https://en.wikipedia.org/wiki/List_of_algorithms")

if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    titles = html.select("h4")
    # print(len(titles))
    paragraphs = html.select(".mw-headline")
    for para in paragraphs:
        if len(para.text)<50:
            print(para.text)
            subtitles= para.select("ul>li>a")
            # print(subtitles.text)
    # document.getElementsByClassName('project_username')[0].innerHTML
    # just grab the text up to contents as stated in question
    # intro = '\n'.join([ para.text for para in paragraphs[0:5]])
    # print (intro)