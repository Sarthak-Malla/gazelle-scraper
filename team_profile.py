# Uses selenium and beautiful soup to scrape the profile for every team member in The Gazelle
from bs4 import BeautifulSoup
from selenium import webdriver
import json

team_profile_json = {}
team_profile_json["profiles"] = []

def getArticleList(staff_articles):
    articles = []
    for article in staff_articles:
        # get thumbnail image of the article
        article_image = article.find('a').find('img', attrs={'class': 'article-preview__featured-image'})['src']
        article_link = article.find('a')['href']

        article_content = article.find('div', attrs={'class': 'article-preview__content'})
        article_authors = article_content.find('div', attrs={'class': 'article-preview__content__authors'}).div.find_all('li')

        # get the authors of the article
        authors = []
        for author in article_authors:
            authors.append(author.a.text)
        
        article_category = article_content.find('p', attrs={'class': 'article-preview__content__category-header'}).text
        article_title = article_content.find('h3', attrs={'class': 'article-preview__content__title'}).text

        article_teaser = article_content.find('p', attrs={'class': 'article-preview__content__teaser'}).text

        articles.append({
            "title": article_title,
            "authors": authors,
            "category": article_category,
            "teaser": article_teaser,
            "image": article_image,
            "link": article_link
        })

    return articles

def getStaffInfo(staff_profile_div):
    # get the staff information
    profile_div = staff_profile_div.find('div', attrs={'class': 'staff__header'})
    profile_image = profile_div.find('img', attrs={'class': 'staff__header__staff-image'})['src']
    profile_text = profile_div.find('div', attrs={'class': 'staff__header__staff-info'})

    profile_name = profile_text.find('h1', attrs={'class': 'staff__header__staff-info__name'}).text
    profile_role = profile_text.find('h2', attrs={'class': 'staff__header__staff-info__role'}).text
    profile_bio = profile_text.find('p', attrs={'class': 'staff__header__staff-info__biography'}).text

    # get staff articles if any
    staff_articles = staff_profile_div.find('div', attrs={'class': 'article-list'}).find_all('div', attrs={'class': 'article-preview'})
    
    articles = getArticleList(staff_articles)

    team_profile_json["profiles"].append({
        "name": profile_name,
        "role": profile_role,
        "biography": profile_bio,
        "image": profile_image,
        "articles": articles
    })


if __name__ == '__main__':
    # access the profile-links.txt file
    with open('./assets/profile-links.txt', 'r') as file:
        # read each line of the file
        while (profile_link := file.readline()):
            # get the url of the page
            url = f"https://www.thegazelle.org{profile_link}"

            # get the html of the page
            driver = webdriver.Chrome()
            driver.get(url)
            html = driver.page_source

            # parse the html
            soup = BeautifulSoup(html, 'html.parser')

            # getting the staff profile div
            staff_profile_div = soup.find('div', attrs={'class': 'staff'})

            getStaffInfo(staff_profile_div);

    driver.close()

    # write the json to a file
    with open('./outputs/team-profile.json', 'w') as file:
        json.dump(team_profile_json, file, indent=4)

