from bs4 import BeautifulSoup
import re
import requests
import data_verification

ALL_HERO_NAMES_URL = "http://www.dota2.com/heroes/"

class HeroAndAdvantage:
    name = ""
    advantage = ""

    def __init__(self, name, advantage):
      self.name = name
      self.advantage = advantage


class AdvantageDataForAHero:
    ADVANTAGES_URL_START = "http://www.dotabuff.com/heroes/"
    ADVANTAGES_URL_END = "/matchups"

    name = ""
    data = []

    def __init__(self, name):
        self.name = name
        url = self.ADVANTAGES_URL_START + self.name_to_url_name(name) + self.ADVANTAGES_URL_END
        web_content = load_url(url)
        self.data = self.get_advantages_from_string(web_content)

    @staticmethod
    def name_to_url_name(name):
        name = name.lower()
        name = name.replace(" ", "-")
        name = name.replace("'", "")
        return name

    @staticmethod
    def get_advantages_from_string(content):
        soup = BeautifulSoup(content, "html.parser")
        soup = soup.find("table", class_="sortable")

        list = []

        for line in soup.find_all(AdvantageDataForAHero.has_data_link_to_attr):
            name = line.find(class_="cell-xlarge").get_text()
            advantage = AdvantageDataForAHero.get_num_from_percent(
                line.find(string=re.compile("%")))
            list.append(HeroAndAdvantage(name, advantage))

        return list

    @staticmethod
    def has_data_link_to_attr(tag):
        return tag.has_attr("data-link-to") 

    @staticmethod
    def get_num_from_percent(string):
        string = string.replace("%", "")
        if(len(string) == 0):
            return 0
        return float(string)


def load_file(filename):
    with open(filename, "r") as content_file:
        return content_file.read()

def load_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    r = requests.get(url, headers=headers)
    return r.text

def get_hero_names_from_string(content):
    soup = BeautifulSoup(content, "html.parser")
    soup = soup.find(id="filterName")

    list = []

    for line in soup.find_all("option"):
        text = line.get_text()
        if(text != "HERO NAME" and text != "All"):
            list.append(text)

    return list

def load_all_hero_data():
    web_content = load_url(ALL_HERO_NAMES_URL)
    hero_list = get_hero_names_from_string(web_content)
    results = []
    for hero in hero_list:
        print("Loading " + hero)
        results.append(AdvantageDataForAHero(hero))
        
    return results

if __name__ == "__main__":
    results = load_all_hero_data()
    data_verification.ensure_all_heroes_loaded(results)
    data_verification.ensure_advantages_within_expected_boundaries(results)

    


