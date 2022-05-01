from flask import Flask, render_template, json, request

app = Flask(__name__)


class Graph:
    def __init__(self, edges):
        self.graph = edges;
        self.amount_of_vertices = len(edges)
        self.path = []
        self.visited = [False for i in range(self.amount_of_vertices)]

    def dfs(self, vertex):
        if self.visited[vertex]:
            return
        self.visited[vertex] = True
        for to in self.graph[vertex]:
            if self.visited[to]:
                continue
            else:
                self.path.append([vertex + 1, to + 1])
                self.dfs(to)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    edges = json.loads(request.form['0'])
    if len(edges) == 0:
        return json.dumps([])
    graph = Graph(edges)
    graph.dfs(0)
    return json.dumps(graph.path)


if __name__ == '__main__':
    app.run(debug=True)
