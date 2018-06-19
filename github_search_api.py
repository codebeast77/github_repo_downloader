# Import required modules
import requests
import math
import pandas as pd

# Paste your Access token here
# To create an access token - https://github.com/settings/tokens
token = "access_token=" + "27badd9b5583986a813e7fe3e8b207d4be1e77be"

# Base API Endpoint
base_api_url = 'https://api.github.com/'

# Additional headers
additional_headers = {'Accept': 'application/vnd.github.mercy-preview+json'}


def github_search(query, no_of_repos, sort_type):
    github_data_list = []

    # GitHub returns information of only 30 repositories with every request

    # The Search API Endpoint only allows upto 1000 results, hence the no of pages required would be calculated as below
    pages = int(math.ceil(no_of_repos / 30.0))

    counter = 0
    for page in range(1, pages + 1):

        # Building the Search API URL
        search_final_url = base_api_url + 'search/repositories?q=' + \
                           query + '&page=' + str(page) + '&sort=' + sort_type + '&' + token

        # try-except block just incase you set up the range in the above for loop beyond 35
        try:
            response = requests.get(search_final_url, headers=additional_headers).json()
        except:
            print("Issue with GitHub API, Check your token")

        # Parsing through the response of the search query
        for item in response['items']:
            if counter <= no_of_repos:
                repo_name = item['name']
                repo_description = item['description']
                repo_stars = item['stargazers_count']
                repo_watchers = item['watchers_count']
                repo_forks = item['forks_count']
                repo_issues_count = item['open_issues_count']
                repo_main_language = item['language']
                repo_clone_url = item['clone_url']
                repo_topics = item['topics']
                repo_license = None

                # repo_score is the relevancy score of a repository to the search query
                # Reference - https://developer.github.com/v3/search/#ranking-search-results
                repo_score = item['score']

                # Many Repositories don't have a license, this is to filter them out
                if item['license']:
                    repo_license = item['license']['name']
                else:
                    repo_license = "NO LICENSE"

                # Just in-case, you face any issue with GitHub API Rate Limiting, use the sleep function as a workaround
                # Reference - https://developer.github.com/v3/search/#rate-limit

                # time.sleep(10)

                # Languages URL to access all the languages present in the repository
                language_url = item['url'] + '/languages?' + token
                language_response = requests.get(language_url).json()

                repo_languages = {}

                # Calculation for the percentage of all the languages present in the repository
                count_value = sum([value for value in language_response.values()])
                for key, value in language_response.items():
                    key_value = round((value / count_value) * 100, 2)
                    repo_languages[key] = key_value
                print("Repo Name = ", repo_name, "\tDescription", repo_description, "\tStars = ", repo_stars,
                      "\tWatchers = ", repo_watchers, "\tForks = ", repo_forks,
                      "\tOpen Issues = ", repo_issues_count, "\tPrimary Language = ", repo_main_language,
                      "\tRepo Languages =", repo_languages, '\tRepo Score', repo_score)

                # Appending the data extracted to a list
                github_data_list.append(
                    [repo_name, repo_description, repo_topics, repo_stars, repo_watchers, repo_forks,
                     repo_license, repo_issues_count, repo_score, repo_clone_url, repo_main_language,
                     repo_languages])

                print('==========')
            counter += 1

    return github_data_list


if __name__ == '__main__':
    print('Enter the Search Query, No. of Repos and Sort Type to get the Data ')

    # Enter multiple word queries with a '+' sign
    # Ex: machine+learning to search for Machine Learning

    query_given = input()
    print('\n Query entered is', query_given, '\n')

    # A CSV file containing the data would be saved with the name as the query
    # Ex: machine+learning.csv
    filename = query_given + '.csv'

    # Enter the no. of repos required
    print('\n Enter the no. of repos required')
    no_of_repos_required = int(input())
    print('\n No. of Repos required are ', no_of_repos_required, '\n')

    # Enter the sort type required
    print('\n Enter the condition your results should be sorted accordingly')
    sort_type_required = input()
    print('\n The sorting required is according to ', sort_type_required, '\n')

    data = github_search(query_given, no_of_repos_required, sort_type_required)
    github_search_data = pd.DataFrame(data, columns=['repository_name', 'repository_description', 'repository_topics',
                                                     'repository_stars', 'repository_watchers', 'repository_forks',
                                                     'repository_license', 'repository_issues_count',
                                                     'repository_score',
                                                     'repository_clone_url', 'repository_main_language',
                                                     'repository_languages'])

    # Creating a csv file
    github_search_data.to_csv(filename, index=False)

