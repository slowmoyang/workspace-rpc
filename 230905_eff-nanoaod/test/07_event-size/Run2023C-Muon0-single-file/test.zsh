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

DATA_FILE=/pnfs/knu.ac.kr/data/cms/store/user/seyang/rpc/tnp-nanoaod/crab/231008-531615/Muon0/muRPCTnPFlatTableProducer_cfg__Muon0__Run2023C-PromptReco-v4/231008_075330/0000/output_372.root

edmEventSize -o event-size.txt -s event-size.png -v -d ${DATA_FILE}
