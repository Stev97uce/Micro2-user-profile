from ariadne import QueryType, MutationType, make_executable_schema
from app.api.graphql.mutations.create_user import mutation as create_user_mutation
from app.api.graphql.mutations.update_profile import mutation as update_profile_mutation
from app.api.graphql.queries.get_user_by_id import query as get_user_query

query = QueryType()
mutation = MutationType()

# Enlazar resolvers manualmente a mutation
mutation.set_field("createUser", create_user_mutation._resolver_map["createUser"])
mutation.set_field("updateProfile", update_profile_mutation._resolver_map["updateProfile"])

type_defs = """
    type User {
        id: Int!
        email: String!
        full_name: String!
        phone: String
        address: String
    }

    input UserInput {
        email: String!
        password: String!
        full_name: String!
        phone: String
        address: String
    }

    input UserUpdateInput {
        full_name: String
        phone: String
        address: String
    }   

    type Mutation {
        createUser(input: UserInput!): User
        updateProfile(id: Int!, input: UserUpdateInput!): User
    }

    type Query {
        getUserById(id: Int!): User
    }
"""

query.set_field("getUserById", get_user_query._resolver_map["getUserById"])
schema = make_executable_schema(type_defs, [query, mutation])
