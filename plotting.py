import hist
import time
import json
import numpy as np
import awkward as ak
from functools import reduce
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import mplhep as hep
import operator
from coffea.util import load
import matplotlib as mpl
from cycler import cycler
import argparse
import os

parser = argparse.ArgumentParser(
    description="Get input file"
)
parser.add_argument("--file", help="Name of the input .pkl file", required=True)
parser.add_argument("--vars", nargs="+", help="Variables to plot", required=True)

args = parser.parse_args()
file_name = args.file
var_to_plot = args.vars

def getHist(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def draw_hist1d(hist_in, ax, trigger, label='', rebin=1, norm=False):
    hist_in = hist_in[:, trigger, hist.rebin(rebin)]
    counts, _, bins = hist_in.to_numpy()
    if len(counts)>0: # check that there are events to plot
        _counts = counts[0]/(np.sum(counts[0])*np.diff(bins)) if norm else counts[0]
        errs = np.sqrt(counts[0])/(np.sum(counts[0])*np.diff(bins)) if norm else np.sqrt(counts[0])
        _errs = np.where(_counts==0, 0, errs)
        bin_centres = 0.5*(bins[1:] + bins[:-1])
        l = ax.errorbar(x=bin_centres,y=_counts,yerr=_errs,linestyle='')
        color = l[0].get_color()
        ax.errorbar(x=bins[:-1],y=_counts,drawstyle='steps-post',label=label,color=color)

    else:
        l = ax.errorbar(x=[],y=[],yerr=[],drawstyle='steps-post') # plot nothing
        color = l[0].get_color()
        ax.errorbar(x=[],y=[],drawstyle='steps-post',label=label,color=color)

def main(file_name, var_to_plot):
    plt.style.use('seaborn-v0_8-white')
    plt.rcParams['figure.dpi'] = 200
    hep.style.use('CMS')
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=[
            '#3f90da', 
            '#ffa90e', 
            '#bd1f01', 
            '#94a4a2', 
            '#832db6', 
            '#a96b59', 
            '#e76300', 
            '#b9ac70', 
            '#717581', 
            '#92dadd'
        ]
    )
 
    # which triggers to plot (comment out unwanted)
    triggers = [
        # 'DST_PFScouting_AXONominal',
        # 'DST_PFScouting_AXOTight',
        # 'DST_PFScouting_AXOVTight',
        # 'DST_PFScouting_CICADAMedium',
        # 'DST_PFScouting_CICADATight',
        # 'DST_PFScouting_CICADAVTight',
        'DST_PFScouting_ZeroBias'
    ]
    trigger_names = {
        # 'DST_PFScouting_AXONominal': 'AXO Nominal',
        # 'DST_PFScouting_AXOTight': 'AXO Tight',
        # 'DST_PFScouting_AXOVTight': 'AXO VTight',
        # 'DST_PFScouting_CICADAMedium': 'CICADA Medium',
        # 'DST_PFScouting_CICADATight': 'CICADA Tight',
        # 'DST_PFScouting_CICADAVTight': 'CICADA VTight',
        'DST_PFScouting_ZeroBias': 'Zero Bias'
    }
    axis_labels = {
        'l1ht': 'L1 HT',
        'l1met': 'L1 MET',
        'total_l1mult': 'L1 multiplicity',
        'anomaly_score': 'Anomaly Score'
    }

    hist_result = load(file_name) 
    for dataset, hists in hist_result.items():
        histpath = [dataset, 'hists']
        for key in var_to_plot:
            hist_name = key
            fig, ax = plt.subplots(1, 2, figsize=(24, 10))
            norm = False

            for trigger in triggers:
                hist_current = getHist(hist_result, histpath+[hist_name])
                draw_hist1d(hist_current, ax[0], trigger, label=trigger_names[trigger], rebin=1, norm=norm)
                plt.savefig(f'{hist_name}_{dataset}.png')
                if os.path.exists(f'{hist_name}_{dataset}.png'):
                    print(f"File {hist_name}_{dataset}.png created")
                else:
                    print(f"Failed to create file {hist_name}_{dataset}.png")

            hep.cms.label('', ax=ax[0], data=True, lumi=None, year=dataset, com=13.6)
            ax[0].set_xlim(0,250)
            ax[0].set_ylabel(f'Events{" [A.U.]" if norm else ""}', loc='top')
            ax[0].set_xlabel(axis_labels[key], loc='right')
            # ax[0].set_yscale('log')
            ax[0].legend();
            ax[1].set_visible(False)
 

if __name__=="__main__":
    print("Plotting variables:", var_to_plot)

    main(file_name, var_to_plot)
