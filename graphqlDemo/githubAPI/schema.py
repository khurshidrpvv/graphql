from graphene import (
	ObjectType,
	String,
	List,
	Field,
	ID,
	Boolean,
	Int,
	NonNull
)
from django.core.cache import cache
from graphene_django.types import DjangoObjectType

from .resolvers import (
	repoLicenseResolver, 
	resolveUserRepos,
	resolveUser,
	resolveUserProject,
	resolveProjectCreator
)

from .apiMethods import convertJsonToObject

CACHE_TIME = 86400

class License(ObjectType):
	key = String()
	name = String()
	spdx_id = String()
	url = String()
	node_id = String()

class RepositoryType(ObjectType):
	id = ID()
	node_id = String()
	name = String()
	full_name = String()
	private = Boolean()
	description = String()
	url = String()
	git_url = String()
	homepage = String()
	language = String()
	forks_count = Int()
	open_issues_count =Int()
	has_issues = Boolean()
	has_wiki = Boolean()
	pushed_at = String()
	created_at = String()
	updated_at = String()
	subscribers_count = Int()
	default_branch = String()
	archived = Boolean()
	license = Field(License)

	def resolve_license(self, info, **kwargs):
		cache_key = 'license-{}'.format(self.name)
		cached_license = cache.get(cache_key)
		if cached_license:
			return convertJsonToObject(cached_license, "license")

		return repoLicenseResolver(self.license, self.name)

class githubUserType(ObjectType):
	login = String()
	id = ID()
	node_id = String()
	type = String()
	site_admin = String()
	name = String()
	company = String()
	blog = String()
	location = String()
	email = String()
	bio = String()
	public_repos = Int()
	followers = Int()
	following = Int()
	created_at = String()
	updated_at = String()
	username = String() #used for input
	repos =  List(RepositoryType)

	def resolve_repos(self, info, **kwargs):
		cache_key = 'repo-{}'.format(self.login)
		cached_user_repo = cache.get(cache_key)
		if cached_user_repo:
			return convertJsonToObject(cached_user_repo, "repo")

		return resolveUserRepos(self.login)

class projectCreatorType(ObjectType):
	login = String()
	id = Int()
	url = String()
	type = String()
	site_admin = String()
class ProjectType(ObjectType):
	owner_url = String()
	url = String()
	name = String()
	body = String()
	state = String()
	creator = Field(projectCreatorType)
	created_at= String()
	updated_at = String()

	def resolve_creator(self, info, **kwargs):
		cache_key = 'creator-{}'.format(self.name)
		cached_project_creator = cache.get(cache_key)
		if cached_project_creator:
			return convertJsonToObject(cached_project_creator, "creator")

		return resolveProjectCreator(self.creator, self.name)


class Query(ObjectType):
	user = Field(
			githubUserType,
			username = NonNull(String)
		)

	repo = List(
			RepositoryType,
			username = NonNull(String)
		)

	project = List(
			ProjectType,
			username = NonNull(String)
		)
	
	def resolve_user(self, info, username):
		cache_key = 'user-{}'.format(username)
		cached_user = cache.get(cache_key)
		if cached_user:
			return convertJsonToObject(cached_user, "user")

		return resolveUser(username)

	def resolve_repo(self, info, username):
		cache_key = 'repo-{}'.format(username)
		cached_repo = cache.get(cache_key)
		if cached_repo:
			return convertJsonToObject(cached_repo, "user")

		return resolveUserRepos(username)

	def resolve_project(self, info, username):
		cache_key = 'project-{}'.format(username)
		cached_project = cache.get(cache_key)
		if cached_project:
			return convertJsonToObject(cached_project, "project")

		return resolveUserProject(username)