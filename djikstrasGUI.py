
import tkinter as tk
from tkinter import messagebox
import heapq

class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Path Finder")

        self.graph = {}
        self.nodes = set()

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.add_node_button = tk.Button(self.root, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.add_edge_button = tk.Button(self.root, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(side=tk.LEFT)

        self.shortest_path_button = tk.Button(self.root, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_path_button.pack(side=tk.LEFT)

        self.start_node_label = tk.Label(self.root, text="Start Node:")
        self.start_node_label.pack(side=tk.LEFT)

        self.start_node_entry = tk.Entry(self.root)
        self.start_node_entry.pack(side=tk.LEFT)

        self.end_node_label = tk.Label(self.root, text="End Node:")
        self.end_node_label.pack(side=tk.LEFT)

        self.end_node_entry = tk.Entry(self.root)
        self.end_node_entry.pack(side=tk.LEFT)

        self.node_positions = {}
        self.edge_lines = []

    def add_node(self):
        node_id = len(self.nodes)
        x, y = (100 + 100 * (node_id % 5), 100 + 100 * (node_id // 5))
        self.node_positions[node_id] = (x, y)
        self.nodes.add(node_id)
        self.graph[node_id] = []
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 16))

    def add_edge(self):
        self.canvas.bind("<Button-1>", self.get_first_node)

    def get_first_node(self, event):
        x, y = event.x, event.y
        first_node = self.find_node(x, y)
        if first_node is not None:
            self.canvas.bind("<Button-1>", lambda event, first_node=first_node: self.get_second_node(event, first_node))

    def get_second_node(self, event, first_node):
        x, y = event.x, event.y
        second_node = self.find_node(x, y)
        if second_node is not None and first_node != second_node:
            weight = self.get_edge_weight()
            if weight is not None:
                self.graph[first_node].append((second_node, weight))
                self.graph[second_node].append((first_node, weight))
                self.draw_edge(first_node, second_node, weight)
            self.canvas.unbind("<Button-1>")

    def find_node(self, x, y):
        for node, (nx, ny) in self.node_positions.items():
            if (nx - 20) <= x <= (nx + 20) and (ny - 20) <= y <= (ny + 20):
                return node
        return None

    def get_edge_weight(self):
        weight = tk.simpledialog.askinteger("Edge Weight", "Enter weight for the edge:")
        return weight

    def draw_edge(self, first_node, second_node, weight):
        x1, y1 = self.node_positions[first_node]
        x2, y2 = self.node_positions[second_node]
        self.edge_lines.append(self.canvas.create_line(x1, y1, x2, y2, fill="black"))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(mx, my, text=str(weight), font=("Arial", 12), fill="red")

    def find_shortest_path(self):
        start_node = int(self.start_node_entry.get())
        end_node = int(self.end_node_entry.get())
        if start_node not in self.nodes or end_node not in self.nodes:
            messagebox.showerror("Error", "Start or End node does not exist.")
            return

        path, dist = self.dijkstra(start_node, end_node)
        if path is None:
            messagebox.showinfo("Result", "No path found.")
        else:
            self.highlight_path(path)
            messagebox.showinfo("Result", f"Shortest path: {' -> '.join(map(str, path))}\nDistance: {dist}")

    def dijkstra(self, start, end):
        queue = [(0, start, [])]
        seen = set()
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in seen:
                continue
            path = path + [node]
            seen.add(node)
            if node == end:
                return path, cost
            for (next_node, weight) in self.graph.get(node, []):
                if next_node not in seen:
                    heapq.heappush(queue, (cost + weight, next_node, path))
        return None, float("inf")

    def highlight_path(self, path):
        self.canvas.delete("highlight")
        for i in range(len(path) - 1):
            x1, y1 = self.node_positions[path[i]]
            x2, y2 = self.node_positions[path[i+1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, tags="highlight")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
