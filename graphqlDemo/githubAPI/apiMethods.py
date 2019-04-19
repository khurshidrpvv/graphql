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
		cache.set(username, user, CACHE_TIME)
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
		reposObject = convertJsonToObject(repos, "repos")
		return reposObject
	except Exception as e:
		error = convertJsonToObject({"error": e}, "error")

def convertJsonToObject(jsonData, name):
	if type(jsonData) is list:
		objectData = [namedtuple(name, data.keys())(*data.values()) for data in jsonData]
	else:
		objectData = namedtuple(name, jsonData.keys())(*jsonData.values())

	return objectData