import pandas as pd

file_name = './rpcGeom.txt'

old_data = []
for line in open(file_name).readlines():
    if line.startswith('#'):
        continue
    tokens = line.strip().split()
    if len(tokens) != 15:
        continue

    name, raw_id, area = tokens[0], int(tokens[1]), float(tokens[2])
    xs, ys, zs = [[float(tokens[3:][3*i + j]) for i in range(4)] for j in range(3)]
    # print(f'{name=}, {raw_id=}, {area=}, {xs=}, {ys=}, {zs=}')
    old_data.append(dict(name=name, raw_id=raw_id, area=area, xs=xs, ys=ys, zs=zs))


new_data = []
df = pd.read_csv(file_name, delimiter=' ', index_col=False)
for _, row in df.iterrows():
    name, raw_id, area = row[['#RollName', 'DetId', 'Area']].to_list()
    xs = row[['x1', 'x2', 'x3', 'x4']].to_list()
    ys = row[['y1', 'y2', 'y3', 'y4']].to_list()
    zs = row[['z1', 'z2', 'z3', 'z4']].to_list()
    # print(f'{name=}, {raw_id=}, {area=}, {xs=}, {ys=}, {zs=}')
    new_data.append(dict(name=name, raw_id=raw_id, area=area, xs=xs, ys=ys, zs=zs))


assert len(old_data) == len(new_data)


for idx in range(len(old_data)):
    old = old_data[idx]
    new = new_data[idx]

    for key in old:
        assert old[key] == new[key]
