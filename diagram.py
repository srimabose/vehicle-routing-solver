from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Clarke-Wright Savings Algorithm', format='png')
dot.attr(rankdir='TB', bgcolor='white', fontname='Helvetica')

# Nodes (colorful)
dot.node('Start', 'START\nSeparate route for each customer', shape='oval', color='blue', style='filled', fillcolor='lightblue')
dot.node('Calculate', 'Calculate Savings\nS_ij = d_i0 + d_0j - d_ij', shape='box', color='green', style='filled', fillcolor='lightgreen')
dot.node('Sort', 'Sort Savings\n(Descending Order)', shape='box', color='purple', style='filled', fillcolor='plum')
dot.node('Merge', 'Merge Routes?\n(Capacity Constraints)', shape='diamond', color='orange', style='filled', fillcolor='moccasin')
dot.node('YesMerge', 'Merge Routes\n(Combine Customers)', shape='box', color='blue', style='filled', fillcolor='lightblue')
dot.node('NoMerge', 'Skip Pair', shape='box', color='black', style='filled', fillcolor='lightgray')
dot.node('Terminate', 'More Savings Pairs?', shape='diamond', color='red', style='filled', fillcolor='lightcoral')
dot.node('End', 'END\nOptimized Routes', shape='oval', color='blue', style='filled', fillcolor='lightblue')

# Edges (arrows)
dot.edge('Start', 'Calculate')
dot.edge('Calculate', 'Sort')
dot.edge('Sort', 'Merge')
dot.edge('Merge', 'YesMerge', label='Yes')
dot.edge('Merge', 'NoMerge', label='No')
dot.edge('YesMerge', 'Terminate')
dot.edge('NoMerge', 'Terminate')
dot.edge('Terminate', 'Merge', label='Yes', style='dashed')
dot.edge('Terminate', 'End', label='No')

# Save and render
dot.render('clarke_wright_flowchart', view=True, cleanup=True)
print("Flowchart saved as 'clarke_wright_flowchart.png'")