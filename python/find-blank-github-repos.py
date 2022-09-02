import requests

username='ohidurbappy'
REPO_ENDPOINT=f"https://api.github.com/users/{username}/repos"

list_of_repos = []

response=requests.get(REPO_ENDPOINT)

repos=response.json()

for repo in repos:
    list_of_repos.append(repo['name'])


# check the brances
for repoName in list_of_repos:
    branches_endpoint=f"https://api.github.com/repos/{username}/{repoName}/branches"
    response=requests.get(branches_endpoint)
    branches=response.json()
    if len(branches)==0:
        print(repoName)



