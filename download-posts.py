import requests
from bs4 import BeautifulSoup
from datetime import datetime
import string
from xhtml2pdf import pisa  

def remove_non_ascii(a_str):
    ascii_chars = set(string.printable)
    return ''.join(e for e in a_str if e.isalpha())


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(
            source_html,      
            dest=result_file)
    result_file.close()
    return pisa_status.err


def page_numbers():
    """Infinite generate of page numbers"""
    num = 1
    while True:
        yield num
        num += 1

posts = []
for page in page_numbers():
    posts_page = requests.get("https://blogmaverick.com/wp-json/wp/v2/posts", params={"page": page, "per_page": 100}).json()
    if isinstance(posts_page, dict) and posts_page["code"] == "rest_post_invalid_page_number": # Found last page
        break
    posts += posts_page
    for x in posts_page:
        date = str(x['date']).split("T")[0]
        title = x['title']['rendered']
        page = x['content']['rendered']
        soup = BeautifulSoup(title, "html.parser")
        soup2 = BeautifulSoup(page, "html.parser")
        fileName = "posts/%s-%s.pdf" % (date, remove_non_ascii(soup.text))
        convert_html_to_pdf(page,fileName)

#print("posts:", len(posts))