#!/usr/bin/env zsh

# Beam mode. FLAT TOP,SQUEEZE,ADJUST,STABLE BEAMS
BEAM_STATUS="STABLE BEAMS"

# correction tag or combined correction tag selection file or string
NORMTAG=/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json

# Input selection json file or string
INPUT_FILE=../../data/cert/Cert_Collisions2023_eraD_369803_370790_Golden.json

# Lumi unit. hz/ub,1e30/cm2s,/nb,1e33/cm2 [default: /ub]
UNIT="/pb"

# Service name [default: offline]
CONNECT=/cvmfs/cms.cern.ch/SITECONF/local/JobConfig/site-local-config.xml

# brilcalc lumi -c ${CONNECT} -i ${INPUT_FILE} -b ${BEAM_STATUS} -u ${UNIT}
brilcalc lumi -c ${CONNECT} -i ${INPUT_FILE} -b ${BEAM_STATUS} -u ${UNIT} --normtag ${NORMTAG}
