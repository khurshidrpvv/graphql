import graphene
import graphqlDemo.githubAPI.schema

class GithubAPIQuery(graphqlDemo.githubAPI.schema.Query, graphene.ObjectType):
  pass

schema = graphene.Schema(query=GithubAPIQuery)