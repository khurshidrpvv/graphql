from .apiMethods import getUserRepos, getUser, convertJsonToObject

def repoLicenseResolver(license):
  if license is None:
    return
  return convertJsonToObject(license, "license")

def resolveUserRepos(username):
  return getUserRepos(username)

def resolveUser(username):
  return getUser(username)