import sys
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict

# Ensure Matplotlib uses the TkAgg backend for visualization in VS Code
matplotlib.use("TkAgg")

# Dictionary to store the call graph dynamically
call_graph = defaultdict(list)  
call_stack = []
MAX_DEPTH = 50  # Limit recursion depth to prevent infinite loops
USER_SCRIPT = "test_code_call_graph.py"  

def trace_calls(frame, event, arg):
    """Tracks function calls and constructs the call graph dynamically."""
    
    filename = frame.f_code.co_filename
    
    # Only trace functions inside the user script, ignore system functions
    if USER_SCRIPT not in filename:
        return

    if event == "call":
        caller = call_stack[-1] if call_stack else "Program Start"
        callee = frame.f_code.co_name  # Get function name

        # Exclude built-in and unwanted functions
        if callee.startswith("__") or callee in {"decode", "encode", "display_call_graph", "visualize_call_graph"}:
            return

        # Prevent infinite recursion
        if len(call_stack) >= MAX_DEPTH:
            print(f"Maximum recursion depth ({MAX_DEPTH}) reached. Possible infinite loop in {callee}.")
            return

        # Store call relationships (preserve duplicate calls)
        call_graph[caller].append(callee)
        call_stack.append(callee)

    elif event == "return":
        if call_stack:
            call_stack.pop()  # Remove function from stack on exit

    return trace_calls

def display_call_graph(graph):
    """Displays the function call graph in text format."""
    print("\nTrace-Based Call Graph:")
    for caller, callees in graph.items():
        if caller == "<module>":  # Ignore module-level calls
            continue  
        for callee in callees:
            if callee != "<module>":
                print(f"  {caller} -> {callee}")

def visualize_call_graph(graph):
    """Generates and displays a directed function call graph using NetworkX and Matplotlib."""
    G = nx.DiGraph()

    # Remove <module> from the graph structure before adding edges
    graph_snapshot = {caller: callees for caller, callees in graph.items() if caller != "<module>"}

    for caller, callees in graph_snapshot.items():
        for callee in callees:
            if callee != "<module>":
                G.add_edge(caller, callee)

    plt.figure(figsize=(8, 8))

    # Ensure "Program Start" is included in the graph
    if "Program Start" not in G.nodes:
        G.add_node("Program Start")

    # Assign hierarchical levels before calling multipartite_layout
    levels = {}
    visited = set()

    def assign_levels(node, depth):
        """Recursively assigns levels to enforce top-down structure."""
        if node in visited:
            return
        visited.add(node)
        levels[node] = depth
        for successor in G.successors(node):
            assign_levels(successor, depth + 1)

    # Assign levels starting from "Program Start"
    assign_levels("Program Start", 0)

    # **Manually arrange nodes in a strict top-down structure**
    pos = {}
    x_spacing = 1.0  # Horizontal spacing between nodes
    y_spacing = -1.5  # Vertical spacing between layers
    level_nodes = defaultdict(list)

    # Organize nodes into layers
    for node, level in levels.items():
        level_nodes[level].append(node)

    # Assign positions to each node
    for level, nodes in sorted(level_nodes.items()):
        num_nodes = len(nodes)
        x_start = -0.5 * (num_nodes - 1) * x_spacing  # Center horizontally
        for i, node in enumerate(nodes):
            pos[node] = (x_start + i * x_spacing, level * y_spacing)

    # Draw the graph with manually assigned positions
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2500, font_size=10, font_weight="bold", arrows=True)
    
    # Draw edge labels (function call relationships)
    edge_labels = {(caller, callee): "" for caller, callee in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.3)

    plt.title("Runtime Function Call Graph (Top-Down)")
    plt.show()

def run_program(target_script):
    """Runs the target script with tracing enabled and generates the call graph."""
    sys.settrace(trace_calls)
    with open(target_script) as f:
        code = compile(f.read(), target_script, 'exec')
        exec(code, {})

def main():
    # Target Python file to analyze
    TARGET_FILE = "test_code.py"

    # Run program and generate trace-based call graph
    run_program(TARGET_FILE)

    # Display the call graph in text format
    display_call_graph(call_graph)

    # Visualize the call graph
    visualize_call_graph(call_graph)

    print("Call graph generation complete!")

if __name__ == "__main__":
    main()