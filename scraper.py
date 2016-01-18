from bs4 import BeautifulSoup
import re
import requests

class HeroAndAdvantage:
  name = ""
  advantage = ""

  def __init__(self, name, advantage):
    self.name = name   
    self.advantage = advantage


def has_data_link_to_attr(tag):
    return tag.has_attr('data-link-to') 


def load_file(filename):
    with open(filename, 'r') as content_file:
        return content_file.read()


def load_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def get_num_from_percent(string):
    string = re.sub(r'%', '', string)
    if(len(string) == 0):
        return 0
    return float(string)


def get_advantages_from_string(content):
  soup = BeautifulSoup(content, 'html.parser')
  soup = soup.find("table", class_="sortable")

  list = []

  for line in soup.find_all(has_data_link_to_attr):
    name = line.find(class_="cell-xlarge").get_text()
    advantage = get_num_from_percent(
      line.find(string=re.compile("%")))
    list.append(HeroAndAdvantage(name, advantage))

  return list


def get_advantages_from_url(url):
    file_string = load_url('http://www.dotabuff.com/heroes/disruptor/matchups')
    return get_advantages_from_string(file_string)


# def get_hero_names_from_string(string):
#     list = [1, 4]
#     return list


list = get_advantages_from_url('http://www.dotabuff.com/heroes/disruptor/matchups')
for item in list:
    print("")
    print(item.name)
    print(item.advantage)
