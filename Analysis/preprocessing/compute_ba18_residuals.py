#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 11:54:38 2025

@author: glavrent
"""
import os
import pathlib
import numpy as np
import pandas as pd
from pygmm.model import Scenario
from pygmm import BaylessAbrahamson2019


def compute_ba19_fas_residuals(
    flatfile_path: str,
    *,
    region: str = "california",
    vs_source: str = "inferred",
    mechanism_from_sof: bool = True,
    min_amp: float = 1e-20,
) -> pd.DataFrame:
    """
    Read NGA2West FAS file and compute ln residuals to Bayless & Abrahamson EAS GMM.

    Parameters
    ----------
    csv_path : str
        Path to `NGA2West_FAS_CA.csv`.
    region : str, optional
        Region flag to pass into the GMM (default "california").
    vs_source : str, optional
        Vs30 source flag if used by the model (e.g. "measured" or "inferred").
    mechanism_from_sof : bool, optional
        If True, map the `SOF` column to mechanism; otherwise use "U" for all.
    min_amp : float, optional
        Floor applied before taking logs to avoid log(0).

    Returns
    -------
    df_out : pandas.DataFrame
        Original dataframe plus additional columns
        `ln_resid_f<freq>` for each frequency column, where:
        ln_resid = ln(FAS_obs) − ln(FAS_pred).
    """

    # Read CSV and select FAS frequency columns
    # ------------------------------------------------------------------
    df = pd.read_csv(flatfile_path)

    #EAS columns
    freq_cols = [c for c in df.columns if c.startswith("freq")]
    if not freq_cols:
        raise ValueError("No 'freq*' columns found in input file.")

    #extract frequencies values
    freqs = np.array([float(c[4:]) for c in freq_cols])
    sort_idx = np.argsort(freqs)
    freqs = freqs[sort_idx]
    freq_cols = [freq_cols[i] for i in sort_idx]

    #determine SOF
    def _mechanism(sof_val: float | int) -> str:
        if not mechanism_from_sof:
            return "U"
        if abs(sof_val) < 0.5:
            return "SS"
        elif sof_val <= -0.5:
            return "NS"
        elif sof_val >= 0.5:
            return "RS"
        return "U"

    # Iterate over frequencies
    # ------------------------------------------------------------------
    ln_resid_all = []

    for _, row in df.iterrows():
        mech = _mechanism(row["SOF"])

        # Build a Scenario; adjust kwargs if your BA-FAS implementation
        # expects a slightly different set.
        s = Scenario(
            mag=float(row["mag"]),
            dist_rup=float(row["Rrup"]),
            v_s30=float(row["Vs30"]),
            depth_1_0=float(row["Z1.0"]),
            depth_tor=float(row["Ztor"]),
            mechanism=mech,
            region=region,
            vs_source=vs_source
        )
        
        #evaluate the FAS model for scenario
        m = BaylessAbrahamson2019(s)

                
        #compute eas frequencies
        ln_pred = np.interp(np.log(freqs), np.log(m.freqs),  m.ln_eas)

        #extract observations
        obs = row[freq_cols].to_numpy(dtype=float)
        
        #compute log observations
        ln_obs = np.full_like(obs, np.nan, dtype=float)
        valid = np.isfinite(obs) & (obs > 0.0)
        ln_obs[valid] = np.log(np.clip(obs[valid], min_amp, None))

        #compute residuals
        ln_resid = ln_obs - ln_pred
        ln_resid_all.append(ln_resid)

    ln_resid_all = np.vstack(ln_resid_all)  # (n_records, n_freq)

    # Assemble output dataframe with residual columns 
    # ------------------------------------------------------------------
    resid_cols = ["resid_freq%0.6f" % f for f in freqs]
    df_resid = pd.DataFrame(ln_resid_all, columns=resid_cols, index=df.index)

    df_out = pd.concat([df, df_resid], axis=1)
    return df_out


#input dataframe filename
fn_df_nga = '../../Raw_files/NGA2West_FAS_CA.csv'

#output 
dir_out = '../../Data/residuals/'
fn_df = 'NGA2West_FAS_CA_residual.csv'


#compute residuals
df_res = compute_ba19_fas_residuals(fn_df_nga)

#write out file
if not os.path.isdir(dir_out): pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True)
df_res.to_csv(dir_out + fn_df)
