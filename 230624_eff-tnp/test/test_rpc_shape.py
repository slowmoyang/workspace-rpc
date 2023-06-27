import ROOT
from ROOT import TGraph
from ROOT import TMultiGraph
import pandas as pd
from utils import RPCDetId

ROOT.gROOT.SetBatch(True)

file_name = './rpcGeom.txt'


# @dataclass
# class RPCShapes:
#     shapes: dict[RPCDetId, TMultiGraph]


new_data = []
df = pd.read_csv(file_name, delimiter=' ', index_col=False)

row = df.iloc[0]

name, raw_id, area = row[['#RollName', 'DetId', 'Area']].to_list()
xs = row[['x1', 'x2', 'x3', 'x4']].to_numpy().astype(np.float64)
ys = row[['y1', 'y2', 'y3', 'y4']].to_numpy().astype(np.float64)
zs = row[['z1', 'z2', 'z3', 'z4']].to_numpy().astype(np.float64)

rpc_id = RPCDetId.from_name(name)

if rpc_id.is_endcap:
    graph_list = [list(zip(xs, ys))]
    graph_list[0].append([xs[0], ys[0]])
elif rpc_id.is_barrel:
    phi_list = []
    for y, x in zip(ys, xs):
        phi = math.atan2(y, x)
        if phi < 0:
            phi += 2 * pi
        phi_list.append(phi)

    ## Regularize the shape in phi
    if abs(phi_list[0] - phi_list[2]) > pi:
        for idx, phi in enumerate(phi_list):
            if phi > pi:
                phi_list[idx] -= 2 * pi

    graph_list = [list(zip(zs, phi_list))]
    graph_list[0].append([zs[0], phi_list[0]])
else:
    raise RuntimeError

shape = TMultiGraph(name, name)
for pts in graph_list:
    graph = TGraph()
    graph.SetTitle(name)
    graph.SetLineColor(ROOT.kGray+2)
    graph.SetLineWidth(1)
    graph.SetEditable(False)
    for idx, (x, y) in enumerate(pts):
        graph.SetPoint(idx, x, y)
    shape.Add(graph)


shape.Draw("APL")
ROOT.gPad.SaveAs('./test.png')
