# using selenium and beatifulsoup to scrape data from The Gazelle website
from bs4 import BeautifulSoup
from selenium import webdriver
import json

team_json = {}

# get the url of the page
url = "https://www.thegazelle.org/team"

# get the html of the page
driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source

# parse the html
soup = BeautifulSoup(html, 'html.parser')

# get the div with all the team members
entire_team_div = soup.find('div', attrs={'class': 'team-page'})

# get all the divided into their respective teams
team_divs = entire_team_div.find_all('div', attrs={'class': 'team-page__team'})

for team_div in team_divs:
    # get the name of the team
    team_name = team_div.find('h2', attrs={'class': 'section-header'}).text

    # get the members of the team
    team_members = team_div.find('div', attrs={'class': 'team-page__team__members'}).find_all('a', attrs={'class': 'team-page__team__members__member'})

    # get the name and position of each member
    team_json[team_name] = []
    for team_member in team_members:
        team_member_image = team_member.find('img', attrs={'class': 'team-page__team__members__member__image'})['src']
        team_member_name = team_member.find('h2', attrs={'class': 'team-page__team__members__member__name'}).text
        team_member_position = team_member.find('h3', attrs={'class': 'team-page__team__members__member__job-title'}).text
        team_json[team_name].append({'name': team_member_name, 'position': team_member_position, 'image': team_member_image})


with open('team.json', 'w') as outfile:
    json.dump(team_json, outfile, indent=4)

driver.close()