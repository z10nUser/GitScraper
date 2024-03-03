import requests
import webbrowser

def search_github_projects(keyword, page=1):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&type=Repositories&page={page}"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    projects = []
    for item in data['items']:
        description = item['description'] if item['description'] else ''
        project = {
            'name': item['name'],
            'description': description[:100] + '...',
            'stars': item['stargazers_count'],
            'creator': item['owner']['login'],
            'url': item['html_url']
        }
        projects.append(project)
    return projects

# Prompt the user for input
keyword = input("Enter keyword or phrase to search GitHub projects: ")

# Prompt the user to enter the number of pages to scrape
num_pages = int(input("Enter the number of pages to scrape: "))

# Concatenate the search results from all pages
projects = []
for i in range(num_pages):
    print(f"Scraping page {i+1}...")
    page_projects = search_github_projects(keyword, i+1)
    projects += page_projects

# Print the results
for i, project in enumerate(projects):
    print(f"{i+1}. {project['name']}")
    print(f"   Description: {project['description']}")
    print(f"   Stars: {project['stars']}")
    print(f"   Creator: {project['creator']}")
    print(f"   URL: {project['url']}\n")

# Prompt the user to select a project
project_num = int(input("Enter the number of the project you'd like to view: "))

# Open the selected project's GitHub page in the user's web browser
project_url = projects[project_num-1]['url']
webbrowser.open(project_url)
