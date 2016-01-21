import scraper

TOTAL_HEROES = 111
MAX_ADVANTAGE = 10

def run_tests(results):
    all_ok = True
    if(ensure_all_heroes_loaded(results) == False):
        all_ok = False
    if(ensure_advantages_within_expected_boundaries(results) == False):
        all_ok = False
    return all_ok

def ensure_all_heroes_loaded(all_data):
    all_ok = True

    if(len(all_data) != TOTAL_HEROES):
        print("ERROR: Only loaded data for {} heroes.".format(len(all_data)))
        all_ok = False

    for data_for_one_hero in all_data:
        if(len(data_for_one_hero.data) != TOTAL_HEROES - 1):
            print("ERROR: " + data_for_one_hero.name + " has advantage data for {} heroes!".format(len(data_for_one_hero.data)))
            all_ok = False

    if(all_ok == True):
        print("PASS: All heroes have advantage data for {} heroes.".format(TOTAL_HEROES))
    return all_ok

def ensure_advantages_within_expected_boundaries(all_data):
    all_ok = True
    for data_for_one_hero in all_data:
        for line in data_for_one_hero.data:
            if(line.advantage > MAX_ADVANTAGE or line.advantage < -1 * MAX_ADVANTAGE):
                print("ERROR: {} has {} advantage over {}, which seems excessive".format(data_for_one_hero.name, line.advantage, line.name))
                all_ok = False

    if(all_ok == True):
        print("PASS: All heroes have advantage no more or less than {}.".format(MAX_ADVANTAGE))
    return all_ok
                
