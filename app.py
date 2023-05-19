import networkx as nx
import pandas as pd
import argparse
import os
import re
from collections import defaultdict
from glob import iglob
from pyvis.network import Network

## parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory_root', type=str, required=True, help='Top level of the Salto tree you want to visualize')
parser.add_argument('-o', '--output_file', type=str, required=False, default='network.html', help='Output file name.  Default:network.html')
args = parser.parse_args()
rootdir = args.directory_root
output_file = args.output_file
print(rootdir)

## globals
data = []
options_from_visjs = '''{
  "physics": {
    "minVelocity": 0.75
  }
}'''

def process_nacl(nacl_file):
    product = ''
    source = ''
    first_line_re = re.compile(r"((^\w+)\.\w+)\s(\w+.*)\s\{", re.MULTILINE)
    with open(nacl_file, 'r') as nacl:
        lines = [line.rstrip() for line in nacl]
    for line in lines:
        fl_match = first_line_re.search(line)
        if fl_match:
            product = fl_match.group(2) 
            prefix = fl_match.group(1)
            suffix = fl_match.group(3)
            source = str(prefix + ".instance." + suffix)
            continue
        if len(product) > 0:
            nacl_re_string = "\s" + product + "\.\w+\.instance\.[\w@.]+"
            nacl_re = re.compile(nacl_re_string)
            nacl_matches = nacl_re.findall(line)
            for nacl_match in nacl_matches:
                if nacl_match:
                    if '"' in nacl_match:
                        continue 
                    data.append((source,nacl_match.lstrip()))

rootdir_glob = rootdir + "/**/*nacl"
file_list = [f for f in iglob(rootdir_glob, recursive=True) if os.path.isfile(f)]
for file in file_list:
    process_nacl(file)

# Create the network graph
df = pd.DataFrame(data, columns=['source', 'target'])
A = list(df["source"])
B = list(df["target"])
node_list = defaultdict(int)
for node in A + B:
    node_list[node] += 1
G = nx.Graph() #Use the Graph API to create an empty network graph object

#Add nodes and edges to the graph object
for i in node_list.keys(): 
    G.add_node(i, size=node_list[i], title=str(i) + ':' + str(node_list[i]), label=None)
for i,j in df.iterrows(): 
    G.add_edges_from([(j["source"],j["target"])])    

net = Network(notebook=False, select_menu=True, filter_menu=True, font_color='#10000000')
net.from_nx(G)
net.set_options(options_from_visjs)
# net.show_buttons(filter_=['physics'])
# net.show_buttons()
net.show(output_file)
