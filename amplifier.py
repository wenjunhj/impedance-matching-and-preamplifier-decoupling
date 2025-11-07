"""The original code was written in May 2021 in MATLAB by Wénjùn Wáng. The file was converted to Python using Claude Sonnet 4.6 on Mar 2026.

References: 
1. W. Wang, V. Zhurbenko, J. D. Sánchez-Heredia, and J. H. Ardenkjær-Larsen. “Trade-off between preamplifier noise figure and decoupling in MRI detectors”. In: Magnetic Resonance in Medicine 89 (2 Feb. 2023), pp. 859–871. ISSN: 15222594. DOI: 10.1002/mrm.29489. 
"""

import numpy as np
import conversion


class Amplifier:
    """
    Two-port amplifier described by S-parameters and noise parameters.

    Parameters
    ----------
    S : array_like, shape (2, 2)
        S-parameter matrix (complex), referece impedance 50 Ω.
    NFmin_dB : float
        Minimum noise figure in dB.
    GammaOpt : complex
        Optimum source reflection coefficient.
    Rn : float
        Equivalent noise resistance (ohms).
    """

    _STEP_PHASE_DEG: float = 0.02  # phase step used when tracing noise circles

    def __init__(self, S: np.ndarray, NFmin_dB: float, GammaOpt: complex, Rn: float):
        S = np.asarray(S, dtype=complex)
        assert S.ndim == 2 and S.shape == (2, 2), "S must be a 2×2 matrix"
        assert np.isscalar(NFmin_dB), "Only one NFmin_dB value is accepted"
        assert np.isscalar(GammaOpt),  "Only one GammaOpt value is accepted"
        assert np.isscalar(Rn),        "Only one Rn value is accepted"

        # S-parameter to Z-parameter conversion (Z0 = 50 Ω)
        zn1A = (1 + S[0, 0]) * (1 - S[1, 1]) + S[0, 1] * S[1, 0]
        zn1B = (1 - S[0, 0]) * (1 + S[1, 1]) + S[0, 1] * S[1, 0]
        zn2  = (1 - S[0, 0]) * (1 - S[1, 1]) - S[0, 1] * S[1, 0]
        self.matrix_Z: np.ndarray = 50 * np.array([
            [zn1A / zn2,          2 * S[0, 1] / zn2],
            [2 * S[1, 0] / zn2,   zn1B / zn2       ],
        ], dtype=complex)

        self.Fmin:  float   = 10 ** (NFmin_dB / 10)
        self.Rn:    float   = float(Rn)
        self.Znopt: complex = conversion.gamma_to_impedance(GammaOpt, 50)

    # ------------------------------------------------------------------
    # Impedance helpers
    # ------------------------------------------------------------------

    def output_impedance(self, source_Z: np.ndarray) -> complex:
        """Z_out seen at port 2 for a given source impedance at port 1."""
        assert np.ndim(source_Z) == 1 or np.ndim(source_Z) == 0, "Only one source_Z value or an array of dimension (x,) is accepted"
        Z = self.matrix_Z
        return Z[1, 1] - Z[0, 1] * Z[1, 0] / (Z[0, 0] + source_Z)

    def input_impedance(self, load_Z: np.ndarray) -> complex:
        """Z_in seen at port 1 for a given load impedance at port 2."""
        assert np.ndim(load_Z) == 1 or np.ndim(load_Z) == 0, "Only one source_Z value or an array of dimension (x,) is accepted"
        Z = self.matrix_Z
        return Z[0, 0] - Z[0, 1] * Z[1, 0] / (Z[1, 1] + load_Z)

    # ------------------------------------------------------------------
    # Stability criteria and optimal small-signal simultaneously complex conjugate matching
    # ------------------------------------------------------------------
    def stability_factor(self) -> float:
        """Rollet stability factor K and delta. See Jens Vidkjær's book, chapter 3 "Linear Active Two-Ports", eq. 46 and eq. 101.
        An amplifier is unconditionally stable if K > 1.
        [Link](https://rftoolbox.dtu.dk/#book)"""
        Z = self.matrix_Z
        rollet_k = (2 * np.real(Z[0, 0]) * np.real(Z[1, 1]) - np.real(Z[1, 0] * Z[0, 1])) / np.abs(Z[1, 0] * Z[0, 1])
        return rollet_k

    def simultaneous_complex_conjugate_impedances(self) -> tuple[complex, complex]:
        """The source and load impedances for the amplifier when it is simulatenously complex conjugate matched. 
        This function is valid only when the stability factor K > 1.
        
        Return: 
        
        z_in_source: complex; it's Z_out of the impedance transform network
        z_amp_load: complex; it equals np.conj(Z_amp_out)
        """
        assert self.stability_factor() > 1, "Not unconditionally stable, simultaneous complex conjugate matching impossible"
        Z = self.matrix_Z
        m = np.sqrt(1 - np.real(Z[1, 0] * Z[0, 1]) / (np.real(Z[0, 0]) * np.real(Z[1, 1])) - (np.imag(Z[1, 0] * Z[0, 1]) / (2 * np.real(Z[0, 0]) * np.real(Z[1, 1]))) ** 2)
        r_g_opt = np.real(Z[0, 0]) * m
        x_g_opt = np.imag(Z[0, 1]* Z[1, 0]) / (2 * np.real(Z[1, 1])) - np.imag(Z[0, 0])
        r_l_opt = np.real(Z[1, 1]) * m
        x_l_opt = np.imag(Z[0, 1]*Z[1, 0]) / (2 * np.real(Z[0, 0])) - np.imag(Z[1, 1])
        return r_g_opt + 1j * x_g_opt, r_l_opt + 1j * x_l_opt

    # ------------------------------------------------------------------
    # Noise circles in the source-impedance (Z_s) plane
    # ------------------------------------------------------------------

    def constant_noise_circles(self, dNF: np.ndarray):
        """
        Constant noise-figure circles in the Z plane, corresponding to §2.2 in reference [1], step 1.

        Parameters
        ----------
        dNF : array_like, shape (N,)
            Excess noise figure(s) above NFmin, in dB.

        Returns
        -------
        cF : ndarray, shape (N,)   – circle centres (complex impedances)
        rF : ndarray, shape (N,)   – circle radii (real, ohms)
        """
        dNF = np.atleast_1d(np.asarray(dNF, dtype=float)).ravel()  # column
        vFlin = conversion.noise_figure_dB_to_lin(dNF, 10 * np.log10(self.Fmin))
        vDelta = (vFlin - self.Fmin) * abs(self.Znopt) ** 2 / self.Rn
        cF = self.Znopt + vDelta / 2
        rF = np.sqrt(vDelta * self.Znopt.real + (vDelta / 2) ** 2)
        return cF, rF

    # ------------------------------------------------------------------
    # Mapped noise contours (Z_s plane → Γ_in plane)
    # ------------------------------------------------------------------

    def mapped_noise_contours(self, dNF: np.ndarray):
        """
        Map constant-NF circles from the Z_s plane into the Γ_in plane for varying Z_{amp}, corresponding to §2.2 in reference [1], steps 2, 3.

        Shape convention (matching MATLAB): columns index dNF values,
        rows index the phase samples around each circle.

        Returns
        -------
        contours              : ndarray, shape (N_phase, N_dNF)
        z_out_matching_network: ndarray, shape (N_phase, N_dNF)
        z_in_amp              : ndarray, shape (N_phase, N_dNF)
        """
        cF, rF = self.constant_noise_circles(dNF)
        cF = cF[np.newaxis, :]   # (1, N_dNF)  – broadcast over phase
        rF = rF[np.newaxis, :]

        phases = np.deg2rad(np.arange(-180, 180, self._STEP_PHASE_DEG))
        scattered_phase = np.exp(1j * phases)[:, np.newaxis]  # (N_phase, 1)

        z_out_mn = cF + rF * scattered_phase                  # (N_phase, N_dNF) # Matching network output impedance

        Z = self.matrix_Z
        z_out_amp = Z[1, 1] - Z[0, 1] * Z[1, 0] / (Z[0, 0] + z_out_mn)
        z_in_amp  = Z[0, 0] - Z[0, 1] * Z[1, 0] / (Z[1, 1] + np.conj(z_out_amp))
        contours  = (z_out_mn - np.conj(z_in_amp)) / (z_out_mn + z_in_amp)  # Contours. They are not circles
        return contours, z_out_mn, z_in_amp

    def mapped_noise_contours_for_constant_z_in_amp(self, dNF: np.ndarray, z_in_amp: complex):
        """
        Analytical noise circles in the Γ_in plane for a fixed Z_in_amp, 
        corresponding to Supporting Information A of [1].

        Returns
        -------
        cF : ndarray – circle centres (complex in Γ_in plane)
        rF : ndarray – circle radii (real)
        """
        dNF = np.atleast_1d(np.asarray(dNF, dtype=float)).ravel()
        gamma_n_opt = conversion.impedance_to_gamma(self.Znopt, z_in_amp)
        vFlin  = conversion.noise_figure_dB_to_lin(dNF, 10 * np.log10(self.Fmin))
        vDelta = (vFlin - self.Fmin) * abs(self.Znopt) ** 2 / self.Rn

        denom = z_in_amp.real * vDelta + abs(z_in_amp + self.Znopt) ** 2
        cF = gamma_n_opt * abs(z_in_amp + self.Znopt) ** 2 / denom
        rF = (2 * z_in_amp.real / denom *
              np.sqrt(self.Znopt.real * vDelta + (vDelta / 2) ** 2))
        return cF, rF

    # ------------------------------------------------------------------
    # Optimal noise impedance mapping
    # ------------------------------------------------------------------

    def mapped_optimal_noise_impedance(self):
        """
        First calculate the optimal output load of the amplifier for $Z_\mathrm{out} = Z_\mathrm{n,opt}$, 
        then calculate what the amplifier impedance will be when the amplifier output 
        is terminated by this optimal output load

        Returns
        -------
        gamma_n_opt         : complex
        z_out_matching_network : matching network output impedance Z_{out}, complex
        z_amp               : amplifier input impedance Z_{amp}, complex
        """
        z_out_mn = self.Znopt
        Z = self.matrix_Z
        z_out_amp = Z[1, 1] - Z[0, 1] * Z[1, 0] / (Z[0, 0] + z_out_mn)
        z_amp     = Z[0, 0] - Z[0, 1] * Z[1, 0] / (Z[1, 1] + np.conj(z_out_amp))
        gamma_n_opt = conversion.impedance_to_gamma(z_out_mn, z_amp)
        return gamma_n_opt, z_out_mn, z_amp

    # ------------------------------------------------------------------
    # Current and gain extrema at a given NF
    # ------------------------------------------------------------------

    def min_and_max_I_and_G_at_given_NF(self, dNF: np.ndarray):
        """
        Minimum and maximum current magnitude and gain achievable for each noise figure in *dNF + NF_min*.
        The minimum current magnitude is preamplifier decoupling, as explained in §2.1, §2.2 in reference [1].

        When preamplifier decoupled, min I = 1 − |Γ_in|, so maximising |Γ_in| minimises min I.
        Gain     G = 1 - |Γ_in|^2, so minimising |Γ_in| maximises G.

        Returns
        -------
        min_I, max_I                          : ndarray, shape (N,), min current (preamplifier decoupling) and max current 
        min_G, max_G                          : ndarray, shape (N,), min and max gain relative to maximum available
        z_in_amp_min_I, z_in_amp_max_I        : ndarray, shape (N,), amplifier input Z_{in} that correspond to min_I and max_I respectively
        z_out_mn_min_I, z_out_mn_max_I        : ndarray, shape (N,), matching network Z_{out} that correspond to min_I and max_I respectively

        Even there is almost no use of `max_I` and `min_G` in practice, we return them for completeness. 
        """
        dNF = np.atleast_1d(np.asarray(dNF, dtype=float)).ravel()
        contours, z_out_mn, z_in_amp = self.mapped_noise_contours(dNF)
        # contours shape: (N_phase, N_dNF)

        abs_contours = np.abs(contours)
        max_gamma_idx = np.argmax(abs_contours, axis=0)   # (N_dNF,)
        min_gamma_idx = np.argmin(abs_contours, axis=0)

        max_gamma_abs = abs_contours[max_gamma_idx, np.arange(len(dNF))]
        min_gamma_abs = abs_contours[min_gamma_idx, np.arange(len(dNF))]

        z_out_mn_min_I_G = z_out_mn[max_gamma_idx, np.arange(len(dNF))]
        z_out_mn_max_I_G = z_out_mn[min_gamma_idx, np.arange(len(dNF))]
        z_in_amp_min_I_G = z_in_amp[max_gamma_idx, np.arange(len(dNF))]
        z_in_amp_max_I_G = z_in_amp[min_gamma_idx, np.arange(len(dNF))]

        min_I = 1 - max_gamma_abs
        max_I = 1 - min_gamma_abs
        min_G = 1 - max_gamma_abs ** 2
        max_G = 1 - min_gamma_abs ** 2
        return (min_I, max_I,
                min_G, max_G, 
                z_in_amp_min_I_G, z_in_amp_max_I_G,
                z_out_mn_min_I_G, z_out_mn_max_I_G)

    def min_and_max_I_and_G_at_given_NF_for_constant_z_in_amp(self, dNF: np.ndarray):
        """
        Analytical min/max I and min/max relative gain using the constant-Z_in_amp approximation. 
        Z_in_amp is anchored at the simultaneous small-signal complex conjugate matching point.
        The noise circles correspond to Supporting Information A of reference [1].

        Returns
        -------
        min_I_analytical, max_I_analytical : ndarray, shape (N,), min current (preamplifier decoupling) and max current 
        min_G_analytical, max_G_analytical : ndarray, shape (N,), min and max gain relative to maximum available
        """
        z_out_matching, _ = self.simultaneous_complex_conjugate_impedances()
        z_in_amp = np.conj(z_out_matching)

        cF, rF = self.mapped_noise_contours_for_constant_z_in_amp(dNF, z_in_amp)

        min_I_analytical = 1 - np.abs(cF) - rF
        max_I_analytical = 1 - np.abs(cF) + rF
        min_G_analytical = 1 - np.abs(np.abs(cF) + rF) ** 2
        max_G_analytical = 1 - np.abs(np.abs(cF) - rF) ** 2
        return min_I_analytical, max_I_analytical, min_G_analytical, max_G_analytical
