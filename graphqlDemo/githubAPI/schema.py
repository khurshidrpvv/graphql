import graphene
from django.core.cache import cache
from graphene_django.types import DjangoObjectType

from .resolvers import (
	repoLicenseResolver, 
	resolveUserRepos,
	resolveUser
)

from .apiMethods import convertJsonToObject

CACHE_TIME = 86400

class License(graphene.ObjectType):
	key = graphene.String()
	name = graphene.String()
	spdx_id = graphene.String()
	url = graphene.String()
	node_id = graphene.String()

class RepositoryType(graphene.ObjectType):
	id = graphene.ID()
	node_id = graphene.String()
	name = graphene.String()
	full_name = graphene.String()
	private = graphene.Boolean()
	description = graphene.String()
	url = graphene.String()
	git_url = graphene.String()
	homepage = graphene.String()
	language = graphene.String()
	forks_count = graphene.Int()
	open_issues_count =graphene.Int()
	has_issues = graphene.Boolean()
	has_wiki = graphene.Boolean()
	pushed_at = graphene.String()
	created_at = graphene.String()
	updated_at = graphene.String()
	subscribers_count = graphene.Int()
	default_branch = graphene.String()
	archived = graphene.Boolean()
	license = graphene.Field(License)

	def resolve_license(self, info, **kwargs):
		cached_license = cache.get(self.license)
		if cached_license:
			return cached_license

		resolved_license =  repoLicenseResolver(self.license)
		cache.set(self.license, resolved_license, CACHE_TIME)
		return resolved_license

class githubUserType(graphene.ObjectType):
	login = graphene.String()
	id = graphene.ID()
	node_id = graphene.String()
	type = graphene.String()
	site_admin = graphene.String()
	name = graphene.String()
	company = graphene.String()
	blog = graphene.String()
	location = graphene.String()
	email = graphene.String()
	bio = graphene.String()
	public_repos = graphene.Int()
	followers = graphene.Int()
	following = graphene.Int()
	created_at = graphene.String()
	updated_at = graphene.String()
	username = graphene.String() #used for input
	repos =  graphene.List(RepositoryType)

	def resolve_repos(self, info, **kwargs):
		cached_login = cache.get(self.login)
		if cached_login:
			return cached_login

		resolved_repos = resolveUserRepos(self.login)
		cache.set(self.login, resolved_repos, CACHE_TIME)
		return resolved_repos

class Query(graphene.ObjectType):
	user = graphene.Field(
			githubUserType,
			username = graphene.NonNull(graphene.String)
		)

	repo = graphene.List(
			RepositoryType,
			username = graphene.NonNull(graphene.String)
		)
	
	def resolve_user(self, info, username):
		cached_username = cache.get(username)
		print("cached data>>>>>>>", cached_username)
		if cached_username:
			return convertJsonToObject(cached_username, "user")

		return resolveUser(username)
		# cac?he.set(username, resolved_user, CACHE_TIME)
		# return resolved_user

	def resolve_repo(self, info, username):
		# cached_repo = cache.get(username)
		# if cached_repo:
		# 	return cached_repo

		return resolveUserRepos(username)
		# cache.set(username, resolved_repos, CACHE_TIME)
		# return resolved_repos
