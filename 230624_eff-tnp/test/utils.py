from dataclasses import dataclass
from typing import Optional


@dataclass
class RPCDetId:
    region: int
    sector: Optional[int]
    station: Optional[int]
    roll: str
    wheel: Optional[int]
    layer: Optional[int]
    disk: Optional[int]
    ring: Optional[int]
    channel: Optional[int]

    @classmethod
    def parse_barrel_name(cls, name: str):
        # name = "W-2_RB1in_S01_Backward"
        # ("W-2", "RB1in", "S01", "Backward")
        wheel, station_str, sector, roll = name.split('_')

        wheel = int(wheel[1: ]) # -2
        sector = int(sector[1:].lstrip('0')) # 1
        roll = roll[0] # B

        station = int(station_str[2]) # 1
        if station <= 2:
            layer = (station - 1) * 2 + 1
            if 'out' in station_str:
                layer += 1
        else:
            layer = 4 + (station - 2)
             ## There are suffix, +, -, ++, --, etc
            roll += station_str[3:]

        return cls(region=0, sector=sector, station=station, roll=roll,
                   wheel=wheel, layer=layer, disk=None, ring=None,
                   channel=None)

    @classmethod
    def parse_endcap_name(cls, name):
        d, r, ch, roll = name.split('_')
        signed_disk, ring, channel = int(d[2:]), int(r[1:]), int(ch[2:])

        disk = abs(signed_disk)
        region = 1 if signed_disk > 0 else -1
        return cls(region=region, sector=None, station=None, roll=roll,
                   wheel=None, layer=None, disk=disk, ring=ring,
                    channel=channel)

    @classmethod
    def from_name(cls, name: str):
        if name.startswith("W"):
            return cls.parse_barrel_name(name)
        elif name.startswith("RE"):
            return cls.parse_endcap_name(name)
        else:
            raise RuntimeError

    @property
    def is_barrel(self) -> bool:
        return self.region == 0

    @property
    def is_endcap(self) -> bool:
        return abs(self.region) == 1

    @property
    def is_irpc(self) -> bool:
        return self.is_endcap and self.disk in (3, 4) and self.ring == 1
