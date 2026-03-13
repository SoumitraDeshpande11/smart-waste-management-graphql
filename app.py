from flask import Flask, request, jsonify
from schema import schema

app = Flask(__name__)

GRAPHIQL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Waste Management GraphQL API</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/3.0.6/graphiql.min.css" />
</head>
<body style="margin: 0;">
    <div id="graphiql" style="height: 100vh;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/3.0.6/graphiql.min.js"></script>
    <script>
        const fetcher = GraphiQL.createFetcher({ url: '/graphql' });
        ReactDOM.render(
            React.createElement(GraphiQL, { fetcher: fetcher }),
            document.getElementById('graphiql'),
        );
    </script>
</body>
</html>
"""


@app.route("/graphql", methods=["GET"])
def graphiql():
    return GRAPHIQL_HTML


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(
        data.get("query", ""),
        variables=data.get("variables"),
        operation_name=data.get("operationName"),
    )
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [{"message": str(e)} for e in result.errors]
    return jsonify(response)


if __name__ == "__main__":
    print("Server running at http://localhost:4000/graphql")
    print("GraphiQL interface available in your browser")
    app.run(debug=True, port=4000)
