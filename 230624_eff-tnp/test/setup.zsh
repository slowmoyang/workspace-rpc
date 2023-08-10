#!/usr/bin/env zsh
cd ../CMSSW_12_4_9/src
eval `scramv1 runtime -sh`
cd -
typeset -m SCRAM_ARCH
typeset -m CMSSW_VERSION
typeset -m CMSSW_BASE

