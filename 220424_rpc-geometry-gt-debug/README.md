# RPC Geometry GT Debug
- [`125X_dataRun3_relval_v1`](https://cms-conddb.cern.ch/cmsDbBrowser/list/Prod/gts/125X_dataRun3_relval_v1)
    - [`RecoIdealGeometry_RPC_v2_hlt`](https://cms-conddb.cern.ch/cmsDbBrowser/list/Prod/tags/RecoIdealGeometry_RPC_v2_hlt)
- [`125X_dataRun3_relval_v4`](https://cms-conddb.cern.ch/cmsDbBrowser/list/Prod/gts/125X_dataRun3_relval_v4)
    - [`RecoIdealGeometry_RPC_v3_hlt`](https://cms-conddb.cern.ch/cmsDbBrowser/list/Prod/tags/RecoIdealGeometry_RPC_v3_hlt)

- [diff 125X_dataRun3_relval_v1 125X_dataRun3_relval_v4](https://cms-conddb.cern.ch/cmsDbBrowser/diff/Prod/gts/125X_dataRun3_relval_v1/125X_dataRun3_relval_v4)
- [diff RecoIdealGeometry_RPC_v2_hlt RecoIdealGeometry_RPC_v3_hlt](https://cms-conddb.cern.ch/cmsDbBrowser/diff/Prod/tags/RecoIdealGeometry_RPC_v2_hlt/RecoIdealGeometry_RPC_v3_hlt)

## Recipe
First, create a local dev area.
```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_12_6_0_pre5
cd CMSSW_12_6_0_pre5/src
cmsenv
cd -
```

The second step is to retrieve RPC payloads from conddb.
```zsh
zsh ./run-conddb-import.zsh
```

The third step is to dump a payload from a sqlite file to an xml file.
Since `RecoIdealGeometry_RPC_v3_hlt` contains all payloads stored in `RecoIdealGeometry_RPC_v2_hlt`, we use `v3` here to extract two payloads of interest.
```zsh
zsh ./run-conddb-dump.zsh
```

Finally, run a simple python code to check the detector differences between two payloads.
```zsh
python3 analyse.py > data/analysis.txt
```
