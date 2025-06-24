from ariadne import QueryType, MutationType, make_executable_schema
from app.api.graphql.mutations.create_user import mutation as create_user_mutation
from app.api.graphql.mutations.update_profile import mutation as update_profile_mutation
from app.api.graphql.queries.get_user_by_id import query as get_user_query

# Creamos resolvers globales
query = QueryType()
mutation = MutationType()

# Asignamos resolvers manualmente desde los módulos
for field, resolver in create_user_mutation._resolvers.items():
    mutation.set_field(field, resolver)

for field, resolver in update_profile_mutation._resolvers.items():
    mutation.set_field(field, resolver)

for field, resolver in get_user_query._resolvers.items():
    query.set_field(field, resolver)

# Definición del esquema GraphQL
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

schema = make_executable_schema(type_defs, [query, mutation])
