export PROJECT_HOME=$(readlink -f $(dirname ${(%):-%N}))

TMP_CMSSW_VERSION=${1:-CMSSW_13_3_0_pre2}
TMP_CMSSW_BASE=${PROJECT_HOME}/${TMP_CMSSW_VERSION}

if [ ! -d ${TMP_CMSSW_BASE} ]; then
    print -- "CMSSW_BASE NOT FOUND: ${TMP_CMSSW_BASE}"
    return 1
fi

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/cms.cern.ch/common/crab-setup.sh

cd ${TMP_CMSSW_BASE}
eval `scramv1 runtime -sh`
cd -

source /cvmfs/grid.cern.ch/umd-c7ui-latest/etc/profile.d/setup-c7-ui-example.sh
voms-proxy-init -voms cms -rfc --valid 192:00

typeset -m SCRAM_ARCH
typeset -m CMSSW_VERSION
typeset -m CMSSW_BASE
