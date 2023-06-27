import pandas as pd
from utils import RPCDetId


class OldRPCDetId:

    def __init__(self, name, rawId=0):
        self.name = name[:]
        #self.rawId = int(rawId)

        self.region = None
        self.sector = None
        self.station = None
        self.roll = None
        self.wheel = None
        self.layer = None
        self.disk = None
        self.ring = None
        self.channel = None

        if name.startswith("W"):
            self.region = 0
            w, sn, sector, roll = name.split('_')

            self.wheel = int(w[1:])
            self.sector = int(sector[1:].lstrip('0'))
            self.roll = roll[0]

            self.station = int(sn[2])
            if self.station <= 2:
                self.layer = (self.station-1)*2+1
                if 'out' in sn: self.layer += 1
            else:
                self.layer = 4+(self.station-2)
                self.roll += sn[3:] ## There are suffix, +, -, ++, --, etc

        elif name.startswith("RE"):
            d, r, ch, self.roll = name.split('_')
            d, self.ring, self.channel = int(d[2:]), int(r[1:]), int(ch[2:])

            self.disk = abs(d)
            self.region = d/self.disk

    def __eq__(self, another):
        for attr in ['region', 'sector', 'station', 'roll', 'wheel', 'layer', 'disk', 'ring', 'channel']:
            if not hasattr(another, attr) or getattr(self, attr) != getattr(another, attr):
                return False
        return True

    def __hash__(self):
        l = []
        for attr in ['region', 'sector', 'station', 'roll', 'wheel', 'layer', 'disk', 'ring', 'channel']:
            l.append(getattr(self, attr))
        return hash(tuple(l))

    def isBarrel(self):
        return self.region == 0

    def isEndcap(self):
        return abs(self.region) == 1

    def isIRPC(self):
        return self.isEndcap() and self.disk in (3,4) and self.ring == 1


df = pd.read_csv('./rpcGeom.txt', delimiter=' ', index_col=False)


for name in ['RE-4_R2_CH19_B', 'W-2_RB1in_S01_Backward']:
    print(name)
    old_id = OldRPCDetId(name)
    new_id = RPCDetId.from_name(name)

    field_name_list = ['region', 'sector', 'station', 'roll', 'wheel', 'layer',
                       'disk', 'ring', 'channel']
    for each in field_name_list:
        assert getattr(old_id, each) == getattr(new_id, each)
    print('-' * 80)
