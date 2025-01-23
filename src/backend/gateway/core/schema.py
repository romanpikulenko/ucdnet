import graphene
import graphql_jwt
import posts.schema
import posts.schema_relay
import users.schema


class Query(users.schema.Query, posts.schema.Query, posts.schema_relay.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, posts.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
