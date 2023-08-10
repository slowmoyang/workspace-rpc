#!/usr/bin/env python
from pathlib import Path
from dataclasses import dataclass
import argparse
import ROOT
import pandas as pd
import tqdm
from ROOT import TFile
from ROOT import THnSparseF
from ROOT import gStyle
from RPCDPGAnalysis.SegmentAndTrackOnRPC.ProjectTHnSparse import THnSparseSelector


gStyle.SetOptStat(0)


@dataclass
class AxisInfo:
    index: int
    name: str
    title: str
    nbins: int
    min: float
    max: float


class THnSparseSelector:
    hist: THnSparseF
    axis_info: dict[str, AxisInfo]

    def __init__(self, hist):
        self.hist = hist
        self.axis_info = {}
        for index in range(hist.GetNdimensions()):
            axis = hist.GetAxis(index)
            name = axis.GetName()
            self.axis_info[name] = AxisInfo(
                index=index,
                name=name,
                title=axis.GetTitle(),
                nbins=axis.GetNbins(),
                min=axis.GetXmin(),
                max=axis.GetXmin()
            )

    def _set_range(self,
                   axisRanges: dict[str, tuple[float, float]]
    ) -> None:
        for name, (lo, hi) in axisRanges.items():
            index = self.axis_info[name].index
            axis = self.hist.GetAxis(index)
            binLo, binHi = axis.FindBin(lo), axis.FindBin(hi)
            self.hist.GetAxis(index).SetRange(binLo, binHi)

    def _recover_range(self, axisRanges: dict[str, tuple[float, float]]):
        for name in axisRanges.keys():
            index = self.axis_info[name].index
            self.hist.GetAxis(index).SetRange(1, self.axis_info[name].nbins)

    def _copy_axis_label(self,
                        source_axis_name: str,
                        target_hist,
                        target_axis_name: str
    ):
        index = self.axis_info[source_axis_name].index
        source_axis = self.hist.GetAxis(index)

        if target_axis_name == 'x':
            target_axis = target_hist.GetXaxis()
        elif target_axis_name == 'y':
            target_axis = target_hist.GetYaxis()
        else:
            raise ValueError('unknown axis name:')

        for bin in range(0, target_axis.GetNbins() + 2):
            label = source_axis.GetBinLabel(bin)
            if label == '':
                continue
            target_axis.SetBinLabel(bin, label)

    def Project1D(self,
                  axisName,
                  axisRanges,
                  suffix: str = '',
                  copyAxisLabel: bool = False
    ):
        if axisName not in self.axis_info:
            raise RuntimeError(f'AxisNotFound: {axisName}. the following axes'
                               f' are avaible: {list(self.axis_info.keys())}')


        self._set_range(axisRanges)
        index = self.axis_info[axisName].index
        h = self.hist.Projection(index)
        name = f"h_{axisName}"
        if len(suffix) > 0:
            name = f'{name}_{suffix}'
        h.SetName(name)
        self._recover_range(axisRanges)
        if copyAxisLabel:
            self._copy_axis_label(axisName, h, 'x')
        return h

    def Project2D(self,
                  axisName1: str,
                  axisName2: str,
                  axisRanges: dict[str, tuple[float, float]],
                  suffix: str = '',
                  copyXAxisLabel: bool = False,
                  copyYAxisLabel: bool = False,
    ):
        self._set_range(axisRanges)
        index1 = self.axis_info[axisName1].index
        index2 = self.axis_info[axisName2].index

        h = self.hist.Projection(index2, index1)
        name = f"h_{axisName1}_{axisName2}"
        if len(suffix) > 0:
            name = f'{name}_{suffix}'
        h.SetName(name)
        self._recover_range(axisRanges)
        if copyXAxisLabel:
            self._copy_axis_label(axisName1, h, 'x')
        if copyYAxisLabel:
            self._copy_axis_label(axisName1, h, 'y')
        return h


def run(input_path: Path,
        common_selection: dict[str, tuple[float, float]],
        output_dir: Path,
        hist_path: str = 'rpcExt/hInfo'
):

    output_dir.mkdir(parents=True, exist_ok=True)

    input_file = TFile(str(input_path))
    hist = input_file.Get(hist_path)

    selector = THnSparseSelector(hist)

    h_run = selector.Project1D('run', {'isFiducial': (1, 1)})
    run_list = [int(h_run.GetBinLowEdge(bin))
                for bin in range(1, 1 + h_run.GetNbinsX())
                if h_run.GetBinContent(bin) > 0]

    h_roll_name = selector.Project1D("roll_name", {}, copyAxisLabel=True)
    roll_name_list = [(bin, h_roll_name.GetXaxis().GetBinLabel(bin))
                      for bin in range(0, 2 + h_roll_name.GetNbinsX())
                      if h_roll_name.GetXaxis().GetBinLabel(bin) != ""]

    for run in (progress_bar := tqdm.tqdm(run_list)):
        selection = common_selection | {'run': (run, run)}

        den_selection = selection
        num_selection = selection | {'isMatched': (1, 1)}

        h_den = selector.Project1D('roll_name', den_selection, suffix='_den')
        h_num = selector.Project1D('roll_name', num_selection, suffix='_num')

        count = {name: [0, 0] for _, name in roll_name_list}
        for bin, name in roll_name_list:
            den = h_den.GetBinContent(bin)
            num = h_num.GetBinContent(bin)

            count[name][0] += int(den)
            count[name][1] += int(num)

        h_den.Delete()
        h_num.Delete()

        df = pd.DataFrame([{'roll_name': name, 'denominator': den, 'numerator': num}
                           for name, (den, num) in count.items()])
        df.to_csv(output_dir / f'run-{run}.csv', index=False)

        progress_bar.set_description(f'Processing {run=}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-path', type=Path, required=True,
                        help='Help text')
    parser.add_argument('--hist-path', type=str,
                        default='muonHitFromTrackerMuonAnalyzer/hInfo',
                        help='Help text')
    parser.add_argument('-o', '--output-dir', type=Path,
                        default=(Path.cwd() / 'data' / 'count'),
                        help='Help text')
    args = parser.parse_args()

    # TODO fiducial
    common_selection = {
        'isFiducial': (1.0, 1.0)
    }

    run(args.input_path, common_selection, args.output_dir, hist_path=args.hist_path)



if __name__ == "__main__":
    main()
