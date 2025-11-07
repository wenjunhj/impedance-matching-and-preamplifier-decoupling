"""This file contain the core functions that compute matching-preamplifier-decoupling networks. 

References: 
[1] Wang, W. Trade-off between preamplifier noise figure and decoupling. Mag Reson Med, 2023.
[2] Wang, W. Cryogenic Array Coil for Brain Magnetic Resonance Imaging, p. 15. Technical University of Denmark, 2022.

Update log: 
V1, 2024-02-19: Fixed the bug converting Z to Y. Switched from D. Pozar's conversion to that in [2].
"""

import numpy as np
import itertools
import pandas


def power_reflection(z, z_ref):
    """Power reflection coefficient.    
    """
    return (z - np.conj(z_ref)) / (z + z_ref)

def power_swr(z, z_ref):
    """Power standing wave ratio"""
    s = power_reflection(z, z_ref)
    return (1 + np.abs(s)) / (1 - np.abs(s))

def max_preamplifier_decoupling(z_out, z_amp):
    """Maximum preamplifier decoupling in linear scale"""
    reflection = power_reflection(z_out, z_amp)
    return 1 - np.abs(reflection)

def gain_relative_to_maximum_available(z_out, z_amp):
    """Transistor gain relative to the maximum availabel gain"""
    reflection = power_reflection(z_out, z_amp)
    return 1 - np.abs(reflection) ** 2


def impedance_matrix_hz(z_coil, z_amp, z_transfer_to):
    r"""Z matrix to exhibit $Z_\mathrm{in}^\mathrm{HZ}$ to the coil. It returns a positive $X_\varnothing$.
    The function will throw an error if the validity condition is not met.
    """
    assert np.all(np.real(z_transfer_to) > 0) and np.all(np.real(z_amp) > 0), "Must not have negative resistance."
    assert np.all(
        np.logical_or(
            np.logical_not(np.isclose(np.imag(z_amp + z_transfer_to), 0)),
            np.real(z_transfer_to) > np.real(z_amp)
        )
    ), "Validity condition is violated."
    # ¬a∨(a∧b) = (¬a∨a)∧(¬a∨b) = ¬a∨b   https://en.wikipedia.org/wiki/Boolean_algebra  see "Monotone laws"
    beta = power_swr(z_transfer_to, z_amp)
    eta_hz = np.imag(z_amp + z_transfer_to) / (np.real(z_amp) - beta * np.real(z_transfer_to))
    x11 = -np.imag(z_coil) + beta * np.real(z_coil) * eta_hz
    x22 = -np.imag(z_amp) + np.real(z_amp) * eta_hz
    xø_sq = np.real(z_coil) * np.real(z_transfer_to) * (1 + beta ** 2 * eta_hz ** 2)
    xø = np.sqrt(xø_sq)
    return x11, xø, x22

def impedance_matrix_lz(z_coil, z_amp, z_transfer_to):
    r"""Z matrix to exhibit $Z_\mathrm{in}^\mathrm{LZ}$ to the coil. It returns a positive $X_\varnothing$.
    The function will throw an error if the validity condition is not met.
    """
    assert np.all(np.real(z_transfer_to) > 0) and np.all(np.real(z_amp) > 0), "Must not have negative resistance."
    assert np.all(
        np.logical_or(
            np.logical_not(np.isclose(np.imag(z_amp + z_transfer_to), 0)),
            np.real(z_transfer_to) < np.real(z_amp)
        )
    ), "Validity condition is violated."
    # ¬a∨(a∧b) = (¬a∨a)∧(¬a∨b) = ¬a∨b   https://en.wikipedia.org/wiki/Boolean_algebra  see "Monotone laws"
    beta = power_swr(z_transfer_to, z_amp)
    eta_lz = np.imag(z_amp + z_transfer_to) / (np.real(z_amp) * beta - np.real(z_transfer_to))
    x11 = -np.imag(z_coil) + np.real(z_coil) * eta_lz
    x22 = -np.imag(z_amp) + beta * np.real(z_amp) * eta_lz
    xø_sq = np.real(z_coil) * np.real(z_transfer_to) * (1 + eta_lz ** 2)
    xø = np.sqrt(xø_sq)
    return x11, xø, x22

def reactance_matrix_to_susceptance_matrix(x11, xø, x22):
    r"""X matrix elements to B matrix elements. An X matrix is the imaginary part of a Z impedance matrix. $\mathbf{X}=\Im \mathbf{Z}\,$.
    Return order: B_{11}, B_\varnothing, B_{22}
    Note in [2], p. 15, (2.7), "B_\varnothing" on the right side should be "X_\varnothing"
    """
    denom = xø ** 2 - x11 * x22
    b11 = x22 / denom
    b22 = x11 / denom
    bø  = -xø / denom
    return b11, bø, b22

def reactance_matrix_to_T(z11, zø, z22):
    """Converts an X matrix to a T equivalent. Only supports reciprocal X matrices."""
    return z11 - zø, zø, z22 - zø

def reactance_matrix_to_Pi(x11, xø, x22):
    """Converts an X matrix to a Π equivalent. Only supports reciprocal X matrices."""
    b11, bø, b22 = reactance_matrix_to_susceptance_matrix(x11, xø, x22)
    return b11 + bø, -bø, b22 + bø

def reactance_to_LC(x, freq):
    """Converts a reactance value to positive inductance if positive or positive capacitance if negative. 
        
    :param x: reactance, ohm
    :param freq: frequency, Hz
    :return: the corresponding positive inductance or positive capacitance.
    """
    assert freq > 0
    assert np.size(freq) == 1 or np.size(x) == 1 or np.size(x) == np.size(freq)
    freq = 2 * np.pi * freq
    loc_negative,  = np.where(x < 0)
    values = x / freq
    values[loc_negative] = -1 / (x[loc_negative] * freq)
    units = ["H"] * np.size(x)
    for d in loc_negative:
        units[d] = "F"
    return values, units

def susceptance_to_LC(b, freq):
    """Converts a susceptance value to positive inductance if negative or positive capacitance if positive. 
    
    :param b: susceptance, S
    :param freq: frequency, Hz
    :return: the corresponding positive inductance or positive capacitance.
    """
    assert freq > 0
    assert np.size(freq) == 1 or np.size(b) == 1 or np.size(b) == np.size(freq)
    freq = 2 * np.pi * freq
    loc_negative,  = np.where(b < 0)
    values = b / freq
    values[loc_negative] = -1 / (b[loc_negative] * freq)
    units = ["F"] * np.size(b)
    for d in loc_negative:
        units[d] = "H"
    return values, units

# Generates 

# 
def filter_out_networks_of_too_many_inductors(df: pandas.core.frame.DataFrame, upper_limit: np.integer) -> pandas.core.frame.DataFrame:
    """Filters out networks with too many inductors.
    Note! An inductor split into two for differential (balanced) designs counts as 1.

    :param df: pandas data frame that contains the component values
    :param upper_limit: maximum inductor count (inclusive); e.g. upper_limit=2 means two inductors are allowed in total.
    :return: a filtered data frame of networks
    """
    sv = df.eq("H").sum(1)
    return df[sv <= upper_limit]
    

# Filters capacitors and inductors out of range
def threshold_component_values(dtf: pandas.core.frame.DataFrame, l_min_H: np.double, l_max_H: np.double, c_min_F: np.double, c_max_F: np.double) -> pandas.core.frame.DataFrame:
    """Ticks out networks that have capacitors and inductors out of range

    :param dtf: pandas data frame that contains the component values
    :param l_min_H: the minimum inductance allowed in henry (inclusive)
    :param l_max_H: the maximum inductance allowed in henry (inclusive)
    :param c_min_F: the minimum capacitance allowed in farad (inclusive)
    :param c_max_F: the maximum capacitance allowed in farad (inclusive)
    :return: a filtered data frame of networks
    """
    n_row, n_col = dtf.shape
    # print(dtf.shape)
    sv = (dtf["uE1"] == "F") * (dtf["E1"] <= c_max_F) * (dtf["E1"] >= c_min_F) + (dtf["uE1"] == "H") * (dtf["E1"] <= l_max_H) * (dtf["E1"] >= l_min_H)
    # print(dtf[sv])
    for i in range(2, int(n_col) // 2 + 1):
        sv = sv * ((dtf[f"uE{i}"] == "F") * (dtf[f"E{i}"] <= c_max_F) * (dtf[f"E{i}"] >= c_min_F) + (dtf[f"uE{i}"] == "H") * (dtf[f"E{i}"] <= l_max_H) * (dtf[f"E{i}"] >= l_min_H))
    return dtf[sv]