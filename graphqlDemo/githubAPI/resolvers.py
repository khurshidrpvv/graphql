from .apiMethods import (
	getUserRepos, 
	getUser,
	getUserProjects, 
	convertJsonToObject
)

from django.core.cache import cache
CACHE_TIME = 86400

def repoLicenseResolver(license, reponame):
	if license is None:
		return

	cache_key = 'license-{}'.format(reponame)
	cache.set(cache_key, license, CACHE_TIME)

	return convertJsonToObject(license, "license")

def resolveUserRepos(username):
	return getUserRepos(username)

def resolveUser(username):
	return getUser(username)

def resolveUserProject(username):
	return getUserProjects(username)

def resolveProjectCreator(creator, projectName):
	if creator is None:
		return

	cache_key = 'creator-{}'.format(projectName)
	cache.set(cache_key, creator, CACHE_TIME)

	return convertJsonToObject(creator, "creator")