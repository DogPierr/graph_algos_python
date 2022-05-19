from flask import Flask, render_template, json, request

app = Flask(__name__)


class Graph:
    def __init__(self, edges):
        self.graph = edges;
        self.amount_of_vertices = len(edges)
        self.path = []
        self.tins_and_rets = []
        self.visited = [False for i in range(self.amount_of_vertices)]
        self.ret = [0 for i in range(self.amount_of_vertices)]
        self.t_in = [0 for i in range(self.amount_of_vertices)]
        self.timer = 0

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

    def bfs(self):
        queue = [0]
        while len(queue) > 0:
            vertex = queue[0]
            del queue[0]
            self.visited[vertex] = True
            for to in self.graph[vertex]:
                if self.visited[to]:
                    continue
                self.visited[to] = True
                self.path.append([vertex + 1, to + 1])
                queue.append(to)

    def bridge_finder(self, vertex, parent):
        self.timer += 1
        self.t_in[vertex] = self.timer
        self.ret[vertex] = self.timer
        self.path.append([vertex + 1, self.t_in[vertex], self.t_in[vertex]])
        self.visited[vertex] = True
        for to in self.graph[vertex]:
            if to != parent:
                if self.visited[to]:
                    self.ret[vertex] = min(self.ret[vertex], self.ret[to])
                    self.path.append([vertex + 1, self.t_in[vertex], self.t_in[vertex]])
                else:
                    self.path.append([vertex + 1, to + 1])
                    self.bridge_finder(to, vertex)
                    self.ret[vertex] = min(self.ret[vertex], self.ret[to])
                    self.path.append([vertex + 1, self.t_in[vertex], self.t_in[vertex]])
                    if self.ret[to] > self.t_in[vertex]:
                        self.path.append(["bridge", vertex + 1, to + 1])





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    edges = json.loads(request.form['0'])
    algo = request.form['1']
    if len(edges) == 0:
        return json.dumps([])
    graph = Graph(edges)
    if algo == "Depth-First Search":
        graph.dfs(0)
    if algo == "Breadth-First Search":
        graph.bfs()
    if algo == "Bridges":
        graph.bridge_finder(0, -1)
    return json.dumps(graph.path)


if __name__ == '__main__':
    app.run(debug=True)
