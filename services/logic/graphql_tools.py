import graphql

# build_executable schema
#
# accepts schema_definition (string) and resolvers (object) in style of graphql-tools
# returns a schema ready for execution


def build_executable_schema(schema_definition, resolvers, scalars):
    ast = graphql.parse(schema_definition)
    schema = graphql.build_ast_schema(ast)

    for scalar in scalars:
        type = schema.get_type(scalar)
        type.description = scalars[scalar]['description']
        type.serialize = scalars[scalar]['serialize']
        type.parse_literal = scalars[scalar]['parse_literal']
        type.parse_value = scalars[scalar]['parse_value']

    for typeName in resolvers:
        fieldType = schema.get_type(typeName)

        for fieldName in resolvers[typeName]:
            if fieldType is graphql.GraphQLScalarType:
                fieldType.fields[fieldName].resolver = resolvers[typeName][fieldName]
                continue
            field = fieldType.fields[fieldName]
            field.resolver = resolvers[typeName][fieldName]

        if not fieldType.fields:
            continue

        # for remaining in fieldType.fields:
        #     if not fieldType.fields[remaining].resolver:
        #         if isinstance(get_gql_type_nonull(fieldType.fields[remaining].type), graphql.GraphQLScalarType):
        #             fieldType.fields[remaining].resolver = \
        #                 lambda value, info, _r=remaining, **args: value[_r] if _r in value else None
        #         elif isinstance(get_gql_type_nonull(fieldType.fields[remaining].type), graphql.GraphQLObjectType):
        #             fieldType.fields[remaining].resolver = \
        #                 lambda value, info, _r=remaining, **args: res.add_generic_instance(
        #                     value[_r], info.context['shipping_model_client'], info) if _r in value else None
        #         elif isinstance(get_gql_type_nonull(fieldType.fields[remaining].type), graphql.GraphQLList):
        #             fieldType.fields[remaining].resolver = \
        #                 lambda value, info, _r=remaining, **args: [res.add_generic_instance(
        #                     instance, info.context['shipping_model_client'], info) for instance in value[_r]] if _r in value else []

    return schema
