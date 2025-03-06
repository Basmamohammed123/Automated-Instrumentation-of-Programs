import sys
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import tempfile

# Ensure Matplotlib uses the TkAgg backend for visualization in VS Code
matplotlib.use("TkAgg")

# Dictionary to store the call graph dynamically
call_graph = defaultdict(list)
call_stack = []
MAX_DEPTH = 50  # Limit recursion depth to prevent infinite loops

def trace_calls(frame, event, arg):
    """Tracks function calls and constructs the call graph dynamically."""
    filename = frame.f_code.co_filename

    # Only trace functions inside the user script; ignore system functions.
    if TARGET_FILE not in filename:
        return

    if event == "call":
        caller = call_stack[-1] if call_stack else "Program Start"
        callee = frame.f_code.co_name

        # Exclude built-in and unwanted functions.
        if callee.startswith("__") or callee in {"decode", "encode", "display_call_graph", "visualize_call_graph"}:
            return

        # Prevent infinite recursion.
        if len(call_stack) >= MAX_DEPTH:
            print(f"Maximum recursion depth ({MAX_DEPTH}) reached. Possible infinite loop in {callee}.")
            return

        # Store call relationships (preserving duplicates).
        call_graph[caller].append(callee)
        call_stack.append(callee)

    elif event == "return":
        if call_stack:
            call_stack.pop()

    return trace_calls

def display_call_graph(graph):
    """Displays the function call graph in text format."""
    print("\nTrace-Based Call Graph:")
    for caller, callees in graph.items():
        if caller == "<module>":  # Exclude <module> from the output
            continue
        for callee in callees:
            if callee != "<module>":
                print(f"  {caller} -> {callee}")

def visualize_call_graph(graph):
    """Generates and displays a function call graph using Graphviz for automatic centering."""
    G = nx.DiGraph()

    # Build the graph
    for caller, callees in graph.items():
        if caller == "<module>":
            continue
        for callee in callees:
            if callee != "<module>":
                G.add_edge(caller, callee)

    if "Program Start" in G.nodes:
        G.remove_node("Program Start")  # Remove Program Start node

    # Convert NetworkX graph to a Graphviz AGraph
    A = nx.nx_agraph.to_agraph(G)

    # Use Graphviz's `dot` layout for automatic centering
    A.layout(prog="dot")

    # 🔹 Save to a temporary file to avoid the "embedded null byte" error
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        temp_filename = tmpfile.name  # Get file path
        A.draw(temp_filename, format="png")  # Save the graph image

    # Load and display the saved image
    img = plt.imread(temp_filename)
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.axis("off")  # Hide axis for a clean output
    plt.title("Program Call Graph", fontsize=15, fontweight="bold", pad=30)
    plt.show()

def run_program(target_script):
    """Runs the target script with tracing enabled to build the call graph."""
    sys.settrace(trace_calls)
    with open(target_script) as f:
        code = compile(f.read(), target_script, 'exec')
        exec(code, {})

# Target Python file to analyze.
TARGET_FILE = "test_code_call_graph.py"

# Run the program to generate the trace-based call graph.
run_program(TARGET_FILE)

# Display the call graph in text format.
display_call_graph(call_graph)

# Visualize the call graph.
visualize_call_graph(call_graph)
