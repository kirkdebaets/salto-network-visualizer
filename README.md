# Salto Network Visualizer

# *EXPERIMENTAL*

First iteration of a Python script to generate a network diagram of the outputs from [Salto](https://github.com/salto-io/salto).

install:
[preferably in a virtualenv] - pip install -r requirements.txt

usage: app.py [-h] -d DIRECTORY_ROOT [-o OUTPUT_FILE]

options:
  -h, --help            show this help message and exit
  -d DIRECTORY_ROOT, --directory_root DIRECTORY_ROOT
                        Top level of the Salto tree you want to visualize
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file name. Default:network.html


Open the resulting page in a browser (*e.g.*, open network.html) to view the network diagram.

To get interactive control of the map, comment out the *set_options* line and uncomment one of the *show_buttons* lines.
