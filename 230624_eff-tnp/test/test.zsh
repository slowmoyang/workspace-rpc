#!/usr/bin/env zsh
cd ../CMSSW_12_4_9/src
# scram b distclean
# scram b vclean
# scram b clean
scram b -j4
cd -
cmsRun analyzeRPCwithTnP_Z_cfg.py > test.log 2>&1 & tail -f test.log
