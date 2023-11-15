# edmEventSize [options] data_file
# Allowed options:
#   -h [ --help ]              produce help message
#   -a [ --auto-loader ]       automatic library loading (avoid root warnings)
#   -d [ --data-file ] arg     data file
#   -n [ --tree-name ] arg     tree name (default "Events")
#   -o [ --output ] arg        output file
#   -A [ --alphabetic-order ]  sort by alphabetic order (default: sort by size)
#   -F [ --format-names ]      format product name as "product:label (type)"
#                              (default: use full branch name)
#   -p [ --plot ] arg          produce a summary plot
#   -t [ --plot-top ] arg      plot only the <arg> top size branches
#   -s [ --save-plot ] arg     save plot into root file <arg>
#   -v [ --verbose ]           verbose printout

DATA_FILE=./Run2023C-Muon0.root

edmEventSize -o event-size.txt -s event-size.png -v -d ${DATA_FILE}
