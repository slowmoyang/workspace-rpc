#!/usr/bin/env zsh
export PROJECT_HOME=$(readlink -f $(dirname ${(%):-%N}))

alias mamba=micromamba
eval "$(mamba shell hook --shell zsh)"
mamba activate /cvmfs/cms-bril.cern.ch/brilconda3
pip install --user brilws
