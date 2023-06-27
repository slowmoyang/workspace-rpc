from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class RPCDetId:
    region: Optional[int]
    sector: Optional[int]
    station: Optional[int]
    roll: str
    wheel: Optional[int]
    layer: Optional[int]
    disk: Optional[int]
    ring: Optional[int]
    channel: Optional[int]

    @staticmethod
    def parse_barrel_name(name):
        # name = "W-2_RB1in_S01_Backward"
        region = 0
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

        return dict(region=region, wheel=wheel, sector=sector, station=station,
                    roll=roll, layer=layer)

    @staticmethod
    def parse_endcap_name(name):
        d, r, ch, roll = name.split('_')
        signed_disk, ring, channel = int(d[2:]), int(r[1:]), int(ch[2:])

        disk = abs(signed_disk)
        region = 1 if signed_disk > 0 else -1
        return dict(region=region, disk=disk, roll=roll, ring=ring,
                    channel=channel)

    @classmethod
    def from_name(cls, name: str):
        if name.startswith("W"):
            fields = cls.parse_barrel_name(name)
            fields |= {key: None for key in ['disk', 'ring', 'channel']}
        elif name.startswith("RE"):
            fields = cls.parse_endcap_name(name)
            fields |= {key: None for key in ['sector', 'station', 'wheel', 'layer']}
        else:
            raise RuntimeError
        return cls(**fields)

    @property
        def is_barrel(self) -> bool:
        return self.region == 0

    @property
    def is_endcap(self) -> bool:
        return abs(self.region) == 1

    @property
    def is_irpc(self) -> bool:
        return self.is_endcap() and self.disk in (3, 4) and self.ring == 1


