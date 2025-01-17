"""
SFso4_a1, SFso4_a2, so4_a1_CLXF, so4_a2_CLXF to emiso4 converter
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cmor
import logging
import numpy as np

from e3sm_to_cmip.lib import handle_variables

# list of raw variable names needed
RAW_VARIABLES = [str('SFso4_a1'), str('SFso4_a2'),
                 str('so4_a1_CLXF'), str('so4_a2_CLXF')]
VAR_NAME = str('emiso4')
VAR_UNITS = str('kg m-2 s-1')
TABLE = str('CMIP6_AERmon.json')


def write_data(varid, data, timeval, timebnds, index, **kwargs):
    """
    emiso4 = SFso4_a1 (kg/m2/s) + SFso4_a2 (kg/m2/s) + (so4_a1_CLXF (molec/cm2/s) + \
        so4_a2_CLXF(molec/cm2/s)) x 115.107340 (sulfate mw) / 6.02214e+22
    """
    outdata = data['SFso4_a1'][index, :] + data['SFso4_a2'][index, :] + \
        (data['so4_a1_CLXF'][index, :] + data['so4_a2_CLXF'][index, :]) * \
        115.107340 / 6.02214e22
    if kwargs.get('simple'):
        return outdata
    cmor.write(
        varid,
        outdata,
        time_vals=timeval,
        time_bnds=timebnds)


def handle(infiles, tables, user_input_path, **kwargs):
    return handle_variables(
        metadata_path=user_input_path,
        tables=tables,
        table=TABLE,
        infiles=infiles,
        raw_variables=RAW_VARIABLES,
        write_data=write_data,
        outvar_name=VAR_NAME,
        outvar_units=VAR_UNITS,
        serial=kwargs.get('serial'),
        logdir=kwargs.get('logdir'),
        simple=kwargs.get('simple'),
        outpath=kwargs.get('outpath'))
# ------------------------------------------------------------------
