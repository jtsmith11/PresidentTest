import pytest
import requests


# PyTest fixture to get response data from a request of DDG API
@pytest.fixture(scope="session")
def response_data():
    url_ddg = "https://api.duckduckgo.com"
    search_question = "presidents of the united states"

    response = requests.get(url_ddg + "/?q=" + search_question + "&format=json")

    response_data = response.json()

    return response_data


# PyTest fixture to return a correct list of all 45 individual presidents
@pytest.fixture(scope="session")
def president_check_list():
    return ['Washington', 'Adams', 'Jefferson', 'Madison', 'Monroe',
            'Adams', 'Jackson', 'Buren', 'Harrison', 'Tyler', 'Polk',
            'Taylor', 'Fillmore', 'Pierce', 'Buchanan', 'Lincoln',
            'Johnson', 'Grant', 'Hayes', 'Garfield', 'Arthur', 'Cleveland',
            'Harrison', 'McKinley', 'Roosevelt', 'Taft',
            'Wilson', 'Harding', 'Coolidge', 'Hoover', 'Roosevelt', 'Truman',
            'Eisenhower', 'Kennedy', 'Johnson', 'Nixon', 'Ford', 'Carter',
            'Reagan', 'Bush', 'Clinton', 'Bush', 'Obama', 'Trump', 'Biden']


# PyTest fixture to generate a list of all 45 individual presidents from DDG
@pytest.fixture(scope="session")
def president_list(response_data, president_check_list):
    p_list = list()
    repeating_names = ['Adams', 'Harrison', 'Johnson', 'Roosevelt', 'Bush']

    for entry in response_data["RelatedTopics"]:
        text_string = entry["Text"]

        # Checks for which entries are for actual presidents
        if "president of the United States from" or "current president of the United States" in text_string:
            name_bio_split = text_string.split(" - ")
            name_split = name_bio_split[0].split(" ")
            last_name = name_split[-1]

            # Check to make sure only presidents are added to the list
            if last_name in president_check_list:

                # Add to p_list if not already in the list
                if last_name not in p_list:
                    p_list.append(last_name)

                # If repeat name, add it to the list
                elif last_name in p_list and last_name in repeating_names:

                    # If there is a repeating President name, ensure no more than 2 get into the list
                    president_count = {i:p_list.count(i) for i in p_list}
                    if president_count[last_name] < 2:
                        p_list.append(last_name)

    return p_list


# Test to make sure our DDG request is on the correct page
def test_correct_search_page(response_data):
    assert "Presidents of the United States" in response_data["Heading"]


# Test to make sure each president is represented in the DDG list
@pytest.mark.parametrize("president", ['Washington', 'Adams', 'Jefferson', 'Madison', 'Monroe',
            'Adams', 'Jackson', 'Buren', 'Harrison', 'Tyler', 'Polk',
            'Taylor', 'Fillmore', 'Pierce', 'Buchanan', 'Lincoln',
            'Johnson', 'Grant', 'Hayes', 'Garfield', 'Arthur', 'Cleveland',
            'Harrison', 'McKinley', 'Roosevelt', 'Taft',
            'Wilson', 'Harding', 'Coolidge', 'Hoover', 'Roosevelt', 'Truman',
            'Eisenhower', 'Kennedy', 'Johnson', 'Nixon', 'Ford', 'Carter',
            'Reagan', 'Bush', 'Clinton', 'Bush', 'Obama', 'Trump', 'Biden'])
def test_individual_president_check(president, president_list):
    assert president in president_list


# Test to make sure president names that appear more than once are represented
# twice in the DDG list
@pytest.mark.parametrize("repeat_name", ['Adams', 'Harrison', 'Johnson', 'Roosevelt', 'Bush'])
def test_repeat_name_president_check(repeat_name, president_list):
    president_count = {i:president_list.count(i) for i in president_list}
    multiple_president_names = list()

    for item in president_count:
        if president_count[item] > 1:
            multiple_president_names.append(item)

    assert repeat_name in multiple_president_names


# Test to see if the president list acquired from DDG is the correct size (45)
def test_president_list_size(president_list, president_check_list):
    assert len(president_list) == len(president_check_list)
