import scraper

TOTAL_HEROES = 111
MAX_ADVANTAGE = 20

def run_tests(results):
    all_ok = True

    if(ensure_all_heroes_loaded(results) == False):
        all_ok = False
    if(ensure_advantages_within_expected_boundaries(results) == False):
        all_ok = False
    if(ensure_correct_number_roaming_heroes(results) == False):
        all_ok = False

    return all_ok

def ensure_all_heroes_loaded(all_data):
    all_ok = True

    if(len(all_data) != TOTAL_HEROES):
        print("ERROR: Only loaded data for {} heroes.".format(len(all_data)))
        all_ok = False

    for data_for_one_hero in all_data:
        if(len(data_for_one_hero.advantages_data) != TOTAL_HEROES - 1):
            print("ERROR: " + data_for_one_hero.name + " has advantage data for {} heroes!".format(len(data_for_one_hero.advantages_data)))
            all_ok = False

    if(all_ok == True):
        print("PASS: All heroes have advantage data for {} heroes.".format(TOTAL_HEROES))
    return all_ok

def ensure_advantages_within_expected_boundaries(all_data):
    all_ok = True
    for data_for_one_hero in all_data:
        for line in data_for_one_hero.advantages_data:
            if(line.advantage > MAX_ADVANTAGE or line.advantage < -1 * MAX_ADVANTAGE):
                print("ERROR: {} has {} advantage over {}, which seems excessive".format(data_for_one_hero.name, line.advantage, line.name))
                all_ok = False

    if(all_ok == True):
        print("PASS: All heroes have advantage no more or less than {}.".format(MAX_ADVANTAGE))
    return all_ok

def ensure_correct_number_roaming_heroes(all_data):
    roaming_heroes_count = 0
    for data_for_one_hero in all_data:
        if data_for_one_hero.is_roaming == 1:
            roaming_heroes_count = roaming_heroes_count + 1

    all_ok = (len(scraper.AdvantageDataForAHero.ROAMING_HEROES) == roaming_heroes_count)

    if(all_ok == True):
        print("PASS: Identified {} roaming heroes.".format(len(scraper.AdvantageDataForAHero.ROAMING_HEROES)))
    else:
        print("ERROR: Expected {} roaming heroes, but found{}.".format(len(scraper.AdvantageDataForAHero.ROAMING_HEROES), roaming_heroes_count))
        
    return all_ok
                
