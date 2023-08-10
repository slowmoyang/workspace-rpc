import pandas as pd
from RPCDPGAnalysis.SegmentAndTrackOnRPC.RPCGeom import RPCDetId

path = '../CMSSW_12_4_9/src/RPCDPGAnalysis/SegmentAndTrackOnRPC/data/rpcGeom.txt'

df: pd.DataFrame = pd.read_csv(path, delimiter=' ', index_col=False)

seen = set()
for _, row in df.iterrows():
    name = row['#RollName']
    rpc_id = RPCDetId.from_name(name)
    if rpc_id in seen:
        print(rpc_id)
    else:
        seen.add(rpc_id)
