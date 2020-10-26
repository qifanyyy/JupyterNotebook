# -*- coding: UTF-8 -*-
"""
This module runs the SDSS color selection algorithm on input photometry
in the 5-filter SDSS system (u, g, r, i, z). Input magnitudes are assumed
to be corrected for Galactic extinction.
"""

__author__ = 'Jens-Kristian Krogager'
__version__ = '1.0'

import numpy as np

from locus_selection import run_locus_selection


def color_selection(sample, sample_error, verbose=True):
    """
    Run full SDSS quasar candidates selection as specified in
    Richards et al. (2002, AJ 123, 2945-2975).
    All the color and photometric criteria are implemented.
    The returned arrays contain `True` if the given set of
    photometry has passed the criteria, and `False` otherwise.

    Parameters
    ----------

    sample : array_like, shape (N, 5)
        Input photometry in five SDSS bands: u, g, r, i, z
        The array should contain a column for each filter.

    sample_error : array_like, shape (N, 5)
        Input 1-sigma uncertainty for photometry in five bands.
        Should be same dimensions as `sample`.

    verbose : bool   [default = True]
        If `True`, print status messages.

    Returns
    -------

    output : dict
        Dictionary containing the following keys:

        'QSO_FULL' :
            Boolean array of full combined ugri and griz selection.
            Identical to `QSO_UGRI * QSO_UGRI_PHOT + QSO_GRIZ * QSO_GRIZ_PHOT`.

        'QSO_COLOR' :
            Boolean array of pure `ugri` + `griz` color selection, i.e., neglecting the
            i-band criteria for `ugri` and `griz`.

        'QSO_PHOT' :
            Boolean array of pure `ugri` + `griz` photometric selection,
            i.e., only i < 20.2. Identical to `QSO_GRIZ_PHOT`.

        'QSO_GRIZ' :
            Boolean array of full `griz` color selection.

        'QSO_UGRI' :
            Boolean array of full `ugri` color selection.

        'QSO_GRIZ_PHOT' :
            Boolean array of griz i<20.2 criterion only.

        'QSO_UGRI_PHOT' :
            Boolean array of ugri i<19.1 criterion only.

        'QSO_GRIZ_COLOR' :
            Boolean array of pure griz color criterion only.

        'QSO_UGRI_COLOR' :
            Boolean array of pure ugri color criterion only.

        'REJECT' :
            Boolean array of targets fulfilling the rejection criteria.
            These are made up by white dwarf, A-star and red-blue pair
            exclusion regions. See Richards et al. 2002.

    """

    sample = np.array(sample)
    sample_error = np.array(sample_error)

    # For ugri, use first 4 filters:
    ugri_points = sample[:, :4]
    ugri_errors = sample_error[:, :4]
    # For griz, use last 4 filters:
    griz_points = sample[:, 1:]
    griz_errors = sample_error[:, 1:]

    # Unpack separate bands and errors:
    u_mag = sample[:, 0]
    g_mag = sample[:, 1]
    r_mag = sample[:, 2]
    i_mag = sample[:, 3]
    z_mag = sample[:, 4]

    u_err = sample_error[:, 0]
    g_err = sample_error[:, 1]
    # r_err = sample_error[:, 2]
    i_err = sample_error[:, 3]
    # z_err = sample_error[:, 4]

    # Container for target rejection:
    # targets start out as TRUE and if they fail a criterion they are turned to FALSE
    N_targets = len(u_mag)
    is_quasar = np.ones(N_targets, dtype=bool)

    if verbose:
        print("\n  Running SDSS Color Selection Algorithm")
        print("  Implemented in Python by J.-K. Krogager")
        print("  Reference: Richards et al. 2002, AJ 123, 2945\n")
        if N_targets == 1:
            print("  Running on %i target" % N_targets)
        else:
            print("  Running on %i targets" % N_targets)

    # ==========================================================================
    # --- EXCLUSION REGIONS:

    # white dwarf exclusion region:
    WD_ex = (u_mag - g_mag > -0.8) & (u_mag - g_mag < 0.7)
    WD_ex &= (g_mag - r_mag > -0.8) & (g_mag - r_mag < -0.1)
    WD_ex &= (r_mag - i_mag > -0.6) & (r_mag - i_mag < -0.1)
    WD_ex &= (i_mag - z_mag > -1.0) & (i_mag - z_mag < -0.1)

    # A star exclusion region:
    A_ex = (u_mag - g_mag > 0.7) & (u_mag - g_mag < 1.4)
    A_ex &= (g_mag - r_mag > -0.5) & (g_mag - r_mag < 0.0)
    A_ex &= (r_mag - i_mag > -0.5) & (r_mag - i_mag < 0.2)
    A_ex &= (i_mag - z_mag > -0.4) & (i_mag - z_mag < 0.2)

    # WD+M pair exclusion region:
    WDM_ex = (g_mag - r_mag > -0.3) & (g_mag - r_mag < 1.25)
    WDM_ex &= (r_mag - i_mag > 0.6) & (r_mag - i_mag < 2.0)
    WDM_ex &= (i_mag - z_mag > 0.4) & (i_mag - z_mag < 1.2)
    WDM_ex &= g_err < 0.2

    # Test if photometry is in exclusion region:
    reject = WD_ex + A_ex + WDM_ex
    is_quasar = is_quasar & ~reject
    # ==========================================================================

    # ==========================================================================
    #     UGRI SELECTION:
    ugri_cand = is_quasar.copy()

    # not in ugri stellar locus (4 sigma)
    in_ugri = run_locus_selection(ugri_points[~reject], ugri_errors[~reject],
                                  locus='ugri')
    # in_ugri = np.array(in_ugri, dtype=bool)
    ugri_cand[~reject] = ~in_ugri

    # or in UVX box:
    UVX = (u_err < 0.1) & (g_err < 0.1)
    UVX &= (u_mag - g_mag < 0.6)
    ugri_cand = ugri_cand | (UVX & ~reject)

    # or in mid-z region:
    # 2.5 < z < 3 inclusion, 2-sigma locus:
    midz_in = (u_mag - g_mag > 0.6) & (u_mag - g_mag < 1.5)
    midz_in &= (g_mag - r_mag > 0.0) & (g_mag - r_mag < 0.2)
    midz_in &= (r_mag - i_mag > -0.1) & (r_mag - i_mag < 0.4)
    midz_in &= (i_mag - z_mag > -0.1) & (i_mag - z_mag < 0.4)
    midz_in &= ~reject

    in_2sig_ugri = run_locus_selection(ugri_points[midz_in], ugri_errors[midz_in],
                                       midz=True, locus='ugri')
    # in_2sig_ugri = np.array(in_2sig_ugri, dtype=bool)
    midz_selected = ~in_2sig_ugri

    # Select only 10% of the objects in this region:
    midz_qso = midz_selected == 1
    if np.sum(midz_qso) > 10:
        qso_subset = midz_selected[midz_qso]
        random10 = np.random.choice(len(qso_subset), len(qso_subset)/10, replace=False)
        qso_subset[:] = False
        qso_subset[random10] = True
        midz_selected[midz_qso] = qso_subset
        ugri_cand[midz_in] |= midz_selected
    else:
        pass

    # magnitude criteria 15 < i < 19.1:
    ugri_mag_cut = (i_mag > 15.0) & (i_mag < 19.1)
    ugri_cand_magcut = ugri_cand & ugri_mag_cut

    # ==========================================================================
    #     GRIZ SELECTION:
    griz_cand = is_quasar.copy()

    # not in griz stellar locus (4 sigma)
    in_griz = run_locus_selection(griz_points[~reject], griz_errors[~reject],
                                  locus='griz')
    # in_griz = np.array(in_griz, dtype=bool)
    griz_cand[~reject] = ~in_griz

    ## reject low-z interlopers:
    ## The description of et al. (2002) incorrectly states the criteria
    ## of the low-redshift exclusion region:
    # lowz_rej = g_mag - r_mag < 1.0
    # lowz_rej *= u_mag - g_mag >= 0.8
    # lowz_rej *= ((i_mag >= 19.1) + (u_mag - g_mag < 2.5))

    ## From Gordon Richards, priv comm.:
    # lowz_rej = g_mag - r_mag < 1.0
    # low_rej1 = (u_mag - g_mag < 0.8) * (i_mag >= 19.1)
    # low_rej1 += (u_mag - g_mag >= 0.8)*(u_mag - g_mag < 2.5)
    # lowz_rej *= low_rej1

    ## Reconstruction from color-color space:
    lowz_rej1 = (u_mag - g_mag <= 0.6) & (g_mag - r_mag > 0.5*(u_mag - g_mag) + 0.15) & (g_mag - r_mag < 1.0)
    lowz_rej3 = (u_mag - g_mag <= 0.6) & (i_mag >= 19.1) & (g_mag - r_mag < 1.0)
    lowz_rej = lowz_rej1 | lowz_rej3

    griz_cand = griz_cand & ~lowz_rej

    ## The only way to get the right number of targets
    ## is through randomly discarding targets:
    ## Only select 1 in 5:
    ug = u_mag - g_mag
    if np.sum(griz_cand & (i_mag < 19.1) & (ug < 0.6)) > 0:
        N_subset = int(len((griz_cand & (i_mag < 19.1) & (ug < 0.8)).nonzero()[0])*0.2)
        subset = np.random.choice((griz_cand & (i_mag < 19.1) & (ug < 0.8)).nonzero()[0], N_subset, replace=False)
        griz_cand[(i_mag < 19.1) & (ug < 0.6)] = False
        griz_cand[subset] = True

    ## or in gri inclusion for z>3.6; (6) of Richards et al. 2002
    gri_in = i_err < 0.2
    gri_in *= (u_mag - g_mag > 1.5) + (u_mag > 20.6)
    gri_in *= g_mag - r_mag > 0.7
    gri_in *= (g_mag - r_mag > 2.1) + (r_mag - i_mag < 0.44*(g_mag - r_mag) - 0.358)
    gri_in *= i_mag - z_mag < 0.25
    gri_in *= i_mag - z_mag > -1.0
    griz_cand = griz_cand + gri_in * ~reject

    ## riz inclusion for z>4.5; (7) of Richards et al. 2002
    riz_in = i_err < 0.2
    riz_in *= u_mag > 21.5
    riz_in *= g_mag > 21.0
    riz_in *= r_mag - i_mag > 0.6
    riz_in *= i_mag - z_mag > -1.0
    riz_in *= (i_mag - z_mag < 0.52*(r_mag - i_mag) - 0.412)
    griz_cand = griz_cand + riz_in * ~reject

    ## ugr red outliers for z>3.0; (8) of Richards et al. 2002
    ugr_red1 = u_mag > 20.6
    ugr_red1 *= u_mag - g_mag > 1.5
    ugr_red1 *= g_mag - r_mag < 1.2
    ugr_red1 *= r_mag - i_mag < 0.3
    ugr_red1 *= i_mag - z_mag > -1.0
    ugr_red1 *= (g_mag - r_mag < 0.44*(u_mag - g_mag) - 0.56)

    ## ugri outliers from the stellar locus can be selected in griz if:
    ugr_red2 = is_quasar.copy()
    ugr_red2[~reject] = ~in_ugri
    ugr_red2 *= u_err < 0.2
    ugr_red2 *= g_err < 0.2
    ugr_red2 *= u_mag - g_mag > 1.5

    ugr_red = ugr_red1 + ugr_red2
    griz_cand = griz_cand + ugr_red * ~reject

    # magnitude criteria 15 < i < 20.2:
    griz_mag_cut = (i_mag < 20.2) * (i_mag > 15.0)
    griz_cand_magcut = griz_cand * griz_mag_cut
    # griz_cand_magcut = griz_cand * ~lowz_rej * griz_mag_cut
    # ==========================================================================

    # Combine candidates from ugri and griz selections:
    is_quasar_col = ugri_cand + griz_cand
    is_quasar_phot = ugri_mag_cut + griz_mag_cut
    is_quasar_full = ugri_cand_magcut + griz_cand_magcut

    # Pack output:
    output = dict()
    output['QSO_FULL'] = is_quasar_full
    output['QSO_COLOR'] = is_quasar_col
    output['QSO_PHOT'] = is_quasar_phot
    output['QSO_GRIZ'] = griz_cand_magcut
    output['QSO_UGRI'] = ugri_cand_magcut
    output['QSO_GRIZ_COLOR'] = griz_cand
    output['QSO_UGRI_COLOR'] = ugri_cand
    output['QSO_GRIZ_PHOT'] = griz_mag_cut
    output['QSO_UGRI_PHOT'] = ugri_mag_cut
    output['REJECT'] = reject

    if verbose:
        N_qso = np.sum(is_quasar_full)
        if N_qso == 1:
            print("\n  Identified %i target as quasar candidates." % N_qso)
        else:
            print("\n  Identified %i targets as quasar candidates." % N_qso)

    return output
