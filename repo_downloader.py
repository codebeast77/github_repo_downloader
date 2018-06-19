"""
This file downloads the repos listed in .csv file.
"""
import subprocess
import os
import pandas as pd

print('\n enter the .csv filename which consists of git clone url for repositories')
filename = str(input())
final_filename = filename + '.csv'
current_directory = os.getcwd()


print('\n the .csv you are looking for is :', final_filename)
directory_path = current_directory + '/' + filename + '_repos'
os.mkdir(directory_path)


def repo_downloader(repo_url):
    return subprocess.Popen(['git', 'clone',  '--depth', '1', repo_url])


data = pd.read_csv(final_filename)
repo_clone_url = data['repository_clone_url']

for i in repo_clone_url:
    print("Finished cloning the repositories for {}".format(i))
    os.chdir(directory_path)
    repo_downloader(i)

