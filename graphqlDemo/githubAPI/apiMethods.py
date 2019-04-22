import json
import requests
from collections import namedtuple
from django.core.cache import cache

BASE_URL = 'https://api.github.com/'
CACHE_TIME = 86400

def getUser(username):
	try:
		url = BASE_URL + 'users/{}'.format(username)
		user = requests.get(url)
		user = user.json()

		cache_key = 'user-{}'.format(username)
		cache.set(cache_key, user, CACHE_TIME)

		userObject = convertJsonToObject(user, "user")
		return userObject
	except Exception as e:
		error = convertJsonToObject({"error": e}, "error")

def getUsers():
	try:
		url = BASE_URL + 'users'
		users = requests.get(url)
		users = users.json()
		usersObject = convertJsonToObject(users, "users")
		return usersObject
	except Exception as e:
		error = convertJsonToObject({"error": e}, "error")

def getUserRepos(username):
	try:
		url = BASE_URL + 'users/{}/repos'.format(username)
		repos = requests.get(url)
		repos = repos.json()

		cache_key = 'repo-{}'.format(username)
		cache.set(cache_key, repos, CACHE_TIME)

		reposObject = convertJsonToObject(repos, "repos")
		return reposObject
	except Exception as e:
		error = convertJsonToObject({"error": e}, "error")

def getUserProjects(username):
	try:
		url = BASE_URL + 'users/{}/projects'.format(username)
		projects = requests.get(url, headers={'Accept': 'application/vnd.github.inertia-preview+json'})
		projects = projects.json()
		print(">>>>>>>>>>>>>", projects)
		cache_key = 'project-{}'.format(username)
		cache.set(cache_key, projects, CACHE_TIME)

		projectObject = convertJsonToObject(projects, "project")
		return projectObject
	except Exception as e:
		print("errro>>>>>>>>>>>",e)
		error = convertJsonToObject({"error": e}, "error")

def convertJsonToObject(jsonData, name):
	if type(jsonData) is list:
		objectData = [namedtuple(name, data.keys())(*data.values()) for data in jsonData]
	else:
		objectData = namedtuple(name, jsonData.keys())(*jsonData.values())

	return objectData