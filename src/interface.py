# Internal dependencies
from src.file import File
from src.directory import Directory

# External dependencies
import matplotlib.pyplot as plt
import networkx as nx

class Interface:
    
    def __init__(self, root: Directory) -> None:
        self.root = root
        
    def make_tree(self, root, graph: nx.DiGraph):
        """
        Navigate between the directories

        Args:
            root_directory (Directory): The root directory of the sub-tree
            graph (nx.DiGraph): Graph representing the directory tree.
        """
        for file in root.file_childrens:
            graph.add_node(file.name, type='file')  # Adicionando atributo 'type' para identificar arquivos
            graph.add_edge(root.name, file.name)
        
        for subdir in root.directory_childrens:
            graph.add_node(subdir.name, type='directory')  # Adicionando atributo 'type' para identificar diretórios
            self.make_tree(subdir, graph)
            graph.add_edge(root.name, subdir.name)
        
    def create_graph(self):
        """
        Visualize the directory tree.
        
        Args:
            root_directory (Directory): The root directory of the tree.
            
        Returns:
            nx.DiGraph: Graph representing the directory tree.
        """
        G = nx.DiGraph()
        G.add_node(self.root.name, type='directory')  # Adicionando atributo 'type' para identificar o nó raiz como diretório
        self.make_tree(self.root, G)
        
        return G
            
    def display_tree(self):
        """
        Display the directory tree
        
        Args:
            tree (nx.DiGraph): Graph representing the directory tree.
        """
        tree = self.create_graph()
        pos = nx.nx_pydot.graphviz_layout(tree, prog="dot")
        
        # Definindo cores com base no tipo de nó
        node_colors = {'directory': 'lightgreen', 'file': 'skyblue'}
        colors = [node_colors[data['type']] for node, data in tree.nodes(data=True)]
        
        
        nx.draw(tree, pos, with_labels=True, font_weight='bold', node_size=2000, node_color=colors, font_size=10)
        plt.title("Directory Tree")
        plt.show()