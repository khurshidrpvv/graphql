from .apiMethods import getUserRepos, getUser, convertJsonToObject
from django.core.cache import cache
CACHE_TIME = 86400

def repoLicenseResolver(license, reponame):
	if license is None:
		return

	cache_key = 'license-{}'.format(reponame)
	cache.set(cache_key, repos, CACHE_TIME)

	return convertJsonToObject(license, "license")

def resolveUserRepos(username):
	return getUserRepos(username)

def resolveUser(username):
	return getUser(username)