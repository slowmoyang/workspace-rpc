#!/usr/bin/env zsh
# TARGET_FILE=./Make_Cls2Dhist.py
# # gROOT.ProcessLine(".L %s/src/SUSYBSMAnalysis/HSCP/test/ICHEP_Analysis/tdrstyle.C" % os.environ["CMSSW_RELEASE_BASE"])
# sd \
#     'gROOT.ProcessLine\(".L %s/src/SUSYBSMAnalysis/HSCP/test/ICHEP_Analysis/tdrstyle.C" % os.environ\["CMSSW_RELEASE_BASE"\]\)' \
#     'from RPCDPGAnalysis.SegmentAndTrackOnRPC.tdrstyle import set_tdr_style' \
#     ${TARGET_FILE}
# sd setTDRStyle set_tdr_style ${TARGET_FILE}
# git diff ${TARGET_FILE}
# git restore ${TARGET_FILE}

# gROOT.ProcessLine(".L %s/src/SUSYBSMAnalysis/HSCP/test/ICHEP_Analysis/tdrstyle.C" % os.environ["CMSSW_RELEASE_BASE"])
sd \
    'gROOT.ProcessLine\(".L %s/src/SUSYBSMAnalysis/HSCP/test/ICHEP_Analysis/tdrstyle.C" % os.environ\["CMSSW_RELEASE_BASE"\]\)' \
    'from RPCDPGAnalysis.SegmentAndTrackOnRPC.tdrstyle import set_tdr_style' \
    $(fd . ./ -t f -e .py)
sd setTDRStyle set_tdr_style $(fd . ./ -t f -e .py)
git diff
