import numpy as np


def Q_to_coil_impedance(Q: np.ndarray, cap: np.ndarray, freq: np.ndarray) -> np.ndarray:
    """
    Coil impedance for a parallel RLC resonator given its Q, capacitor
    value, and frequency.

    Parameters
    ----------
    Q    : array_like – Q factor(s).
    cap  : array_like – Capacitance in Farads.
    freq : array_like – Frequency in Hertz.

    Returns
    -------
    z_coil : ndarray (complex) – Coil impedance in Ohms.
    """
    omega0 = np.asarray(freq) * 2 * np.pi
    Y_L_para = -omega0 * np.asarray(cap)
    G_para   = -Y_L_para / np.asarray(Q)
    return 1.0 / (G_para + 1j * Y_L_para)


def gamma_to_impedance(gamma: np.ndarray, z0: complex) -> np.ndarray:
    """
    Convert reflection coefficient(s) Γ to impedance.

        Z = z0 * (1 + Γ) / (1 − Γ)   [real z0]
        Z = (z0·Γ + z0*) / (1 − Γ)   [complex z0, general form]

    Parameters
    ----------
    gamma : array_like (complex) – Reflection coefficient(s).
    z0    : complex              – Reference impedance.

    Returns
    -------
    impedance : ndarray (complex)
    """
    gamma = np.asarray(gamma, dtype=complex)
    return (z0 * gamma + np.conj(z0)) / (-gamma + 1)


def impedance_to_gamma(z: np.ndarray, z0: complex) -> np.ndarray:
    """
    Convert impedance(s) to reflection coefficient.

        Γ = (Z − z0*) / (Z + z0)

    Parameters
    ----------
    z  : array_like (complex) – Impedance(s) in Ohms.
    z0 : complex              – Reference impedance.

    Returns
    -------
    gamma : ndarray (complex)
    """
    z = np.asarray(z, dtype=complex)
    return (z - np.conj(z0)) / (z + z0)


def noise_figure_dB_to_lin(dNF: np.ndarray, NFmin_dB: float) -> np.ndarray:
    """
    Convert an excess noise figure (dB above NFmin) to a linear noise
    factor.

        F = 10^( (NFmin_dB + dNF) / 10 )

    Parameters
    ----------
    dNF      : array_like, 1-D – Excess NF in dB (row or column vector).
    NFmin_dB : float            – Minimum noise figure in dB (scalar).

    Returns
    -------
    vFlin : ndarray, shape (N,) – Linear noise factor.
    """
    assert np.isscalar(NFmin_dB), "Only one NFmin_dB is accepted"
    dNF = np.asarray(dNF, dtype=float)
    assert dNF.ndim <= 1, "dNF must be a scalar or a 1-D array"
    dNF = np.atleast_1d(dNF).ravel()
    return 10 ** ((NFmin_dB + dNF) / 10)
