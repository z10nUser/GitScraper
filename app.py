from flask import Flask, render_template, request
import requests
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        num_pages = int(request.form['num_pages'])

        # Concatenate the search results from all pages
        projects = []
        for i in range(num_pages):
            print(f"Scraping page {i+1}...")
            page_projects = search_github(keyword, i+1)
            projects += page_projects

        return render_template('results.html', projects=projects)

    return render_template('index.html')

def search_github(keyword, page):
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

if __name__ == '__main__':
    app.run()
