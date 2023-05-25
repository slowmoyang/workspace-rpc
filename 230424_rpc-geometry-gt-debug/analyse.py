import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import asdict, dataclass
import numpy as np
np.set_printoptions(precision=3, suppress=True)

# we define a relatively large tolerance because we are hunting flipped
# chambers.
ATOL = 1e-2

@dataclass
class RecoIdealGeometry:
    """
    adapted from
    https://github.com/cms-sw/cmssw/blob/master/CondFormats/GeometryObjects/interface/RecoIdealGeometry.h
    """
    pDetIds: list[int]
    pPars: list[float]
    pParsIndex: list[int]
    pNumShapeParms: list[int]
    strPars: list[str]
    sParsIndex: list[int]
    sNumsParms: list[int]

    ###########################################################################
    # parser
    ###########################################################################
    @classmethod
    def from_xml(cls, path):
        tree = ET.parse(path)
        root = tree.getroot()

        tag2dtype = {
            'pDetIds': int,
            'pPars': float,
            'pParsIndex': int,
            'pNumShapeParms': int,
            'strPars': str,
            'sParsIndex': int,
            'sNumsParms': int
        }

        kwargs = {}
        for child in root[0]:
            tag = child.tag

            dtype = tag2dtype[tag]
            if tag == 'pDetIds':
                get = lambda each: dtype(each[0].text)
            else:
                get = lambda each: dtype(each.text)

            kwargs[tag] = [get(each) for each in child if each.tag == 'item']
        return cls(**kwargs)

    ###########################################################################
    # methods adapted from cmssw
    ###########################################################################
    def tranStart(self, ind):
        return self.pParsIndex[ind]

    def transEnd(self, ind):
        return self.pParsIndex[ind] + 3

    def rotStart(self, ind):
        return self.pParsIndex[ind] + 3

    def rotEnd(self, ind):
        return self.pParsIndex[ind] + 3 + 9

    def shapeStart(self, ind):
        return self.pParsIndex[ind] + 3 + 9

    def shapeEnd(self, ind):
        return self.pParsIndex[ind] + 3 + 9 + self.pNumShapeParms[ind]

    def strStart(self, ind):
        return self.sParsIndex[ind]

    def strEnd(self, ind):
        return self.sParsIndex[ind] + self.sNumsParms[ind]

    ###########################################################################
    # utils
    ###########################################################################
    def get_trans(self, ind):
        return self.pPars[self.tranStart(ind): self.transEnd(ind)]

    def get_rot(self, ind):
        return self.pPars[self.rotStart(ind): self.rotEnd(ind)]

    def get_shape(self, ind):
        return self.pPars[self.shapeStart(ind): self.shapeEnd(ind)]

    def get_str(self, ind):
        return self.strPars[self.strStart(ind): self.strEnd(ind)]

    def __len__(self):
        return len(self.pDetIds)

    def __getitem__(self, ind):
        return Detector(
            id=self.pDetIds[ind],
            trans=self.get_trans(ind),
            rot=self.get_rot(ind),
            shape=self.get_shape(ind),
            name=self.get_str(ind)[0] # NOTE
        )

    def __iter__(self):
        for ind in range(len(self)):
            yield self[ind]

@dataclass
class Detector:
    id: int
    name: str
    trans: list[float]
    rot: list[float]
    shape: list[float]

    def __eq__(self, other):
        return (self.id == other.id) and \
               (self.name == other.name) and \
               np.allclose(self.trans, other.trans, atol=ATOL) and \
               np.allclose(self.rot, other.rot, atol=ATOL) and \
               np.allclose(self.shape, other.shape, atol=ATOL)

    def __getitem__(self, key):
        return getattr(self, key)

data_dir = Path(__file__).parent / 'data'
old_path = data_dir / 'payload-accd477271bd4aeeae63444d03fe5fa8f54324dc.xml'
new_path = data_dir / 'payload-0429f37b6663d8a4075f1d9a761f79cb7c73b91d.xml'

print(f'{old_path=}')
print(f'{new_path=}')

old_geoemtry = RecoIdealGeometry.from_xml(old_path)
new_geometry = RecoIdealGeometry.from_xml(new_path)

old_detector_dict = {each.name: each for each in old_geoemtry}
new_detector_dict = {each.name: each for each in new_geometry}

print('-' * 79)
inconsistent_name_list = []
for key in old_detector_dict:
    old_detector = old_detector_dict[key]
    new_detector = new_detector_dict[key]
    if old_detector != new_detector:
        print(f'{key} is inconsistent!')

        for property_key in ['trans', 'rot', 'shape']:
            old = old_detector[property_key]
            new = new_detector[property_key]

            if isinstance(old, list):
                old = np.array(old)
                new = np.array(new)
                same = np.allclose(old, new, atol=ATOL)
            else:
                same = old == new

            if not same:
                print(f'  {property_key}:')
                print(f'    - {old=}')
                print(f'    - {new=}')
        print()

print('-' * 79)
print('checking misisng or added detectors')
old_name_set = set(old_detector_dict.keys())
new_name_set = set(new_detector_dict.keys())

print(f'{old_name_set - new_name_set=}')
print(f'{new_name_set - old_name_set=}')
