from django.http import JsonResponse
from graphene_django.views import GraphQLView
from .schema import schema  
from django.urls import path


class MyGraphQLView(GraphQLView):
    def execute_graphql_request(self, request, data, query, 
                    variables, operation_name, show_graphiql=False):
        return super().execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

def graphql_view(request):
    view = MyGraphQLView.as_view(graphiql=True, schema=schema)
    return view(request)

urlpatterns = [
    path('', graphql_view),
]