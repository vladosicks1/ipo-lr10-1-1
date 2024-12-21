import requests
from bs4 import BeautifulSoup as bs
import json
from bs4 import Tag

url = 'https://news.ycombinator.com/'

response = requests.get(url)
if response.status_code != 200:
    print("Ошибка.")
    exit()

soup = bs(response.text, 'html.parser')

rows = soup.find_all('tr', class_='athing')

print(f"Найдено строк таблицы: {len(rows)}")

list_titles = []
list_comments = []

for row in rows:
    title_tag = row.select_one('span.titleline > a')
    if title_tag:
        title = title_tag.get_text(strip=True)
        list_titles.append(title)
    else:
        list_titles.append("No title")
    
    subtext_row = row.find_next_sibling('tr')
    if subtext_row:
        subtext = subtext_row.find('td', class_='subtext')
        if subtext:
            comments_tag = subtext.find_all('a')[-1]
            if comments_tag and 'comment' in comments_tag.get_text():
                comments = comments_tag.get_text(strip=True).split()[0]
    list_comments.append(comments)

for i in range(len(list_titles)):
    print(f"{i + 1}. Title: {list_titles[i]}; Comments: {list_comments[i]};")

file_json = "data.json"
writer_list = []

for i in range(len(list_titles)):
    writer = {'Title': list_titles[i], 'Comments': list_comments[i]}
    writer_list.append(writer)

with open(file_json, "w", encoding='utf-8') as file:
    json.dump(writer_list, file, indent=4, ensure_ascii=False)

with open('template.html', 'r', encoding='utf-8') as file:
    filedata = file.read()

soup = bs(filedata, "html.parser")

element_to_paste = soup.find("bodytable", id="bodytable")

data = []


for idx, item in enumerate(writer_list, start=1):
    new_el = Tag(name="tr")
    new_el['class'] = 'Title'
    new_el.append(Tag(name="td"))
    new_el.contents[0].string = str(idx)
    new_el.append(Tag(name="td"))
    new_el.contents[1].string = item["Title"]
    new_el.append(Tag(name="td"))
    new_el.contents[2].string = item["Comments"]
    
    element_to_paste.append(new_el)


with open("Index.html", "w+", encoding="utf-8") as file:
    file.write(soup.prettify())