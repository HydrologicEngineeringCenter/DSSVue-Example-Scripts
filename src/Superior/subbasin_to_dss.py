"""
subbasin_to_dss.py

Usage:
    jython.exe subbasin_to_dss.py <output.dss> <input_dir>

Reads every ``*.csv`` in <input_dir>, parses each into a plain ``contents``
dictionary, prints that structure to the screen, and writes one DSS time series
per data column to <output.dss>.

The CSV parsing is deliberately kept independent of DSS: the ``hec.*`` classes
are imported lazily inside the writing layer (write_to_dss) only, so read_file
and print_structure never touch DSS.
"""

from __future__ import print_function

import glob
import io
import os
import sys


# Hard-coded pieces of the DSS path (used by the future DSS layer; kept here so
# the intended structure is visible).  See AGENTS.md.
DSS_A_PART = 'Superior'
DSS_E_PART = '1Day'
DSS_F_PART = 'GLSHFS-OPERATIONAL-HISTORIC'

MISSING_TOKENS = ('NA', '')

# --- DSS writing configuration -------------------------------------------
# Daily values are timestamped at end-of-day (24:00); that keeps each value in
# its own calendar-day block (00:00 pushes it into the previous day's block).
DSS_INTERVAL_MINUTES = 1440       # 1Day, matches DSS_E_PART
DSS_TIME_LABEL = '2400'

# DSS data type per column: accumulations over the day are PER-CUM, anything
# not listed falls back to DSS_DEFAULT_TYPE.  Adjust this table as needed.
DSS_TYPE_BY_COLUMN = {
    'Precip': 'PER-CUM',
    'Runoff': 'PER-CUM',
}
DSS_DEFAULT_TYPE = 'INST-VAL'


def determine_type(column_name):
    """DSS time series type for a column (PER-CUM for accumulations, else default)."""
    return DSS_TYPE_BY_COLUMN.get(column_name, DSS_DEFAULT_TYPE)


def _to_float_or_none(token):
    """A Fortran data token -> float, or None for a missing value (NA/blank)."""
    token = token.strip()
    if token in MISSING_TOKENS:
        return None
    return float(token)


def read_file(path):
    """Read one subbasin/lbrm CSV file into a contents dict.

    Returns::

        {
          'header': {
            'title': <str>,
            'Lake': <str>, 'Subbasin': <str>, 'Area': <float>,
            'Starts(YMD)': <str>, 'Ends(YMD)': <str>, 'NewDataStart(YMD)': <str>,
            'column_names': [<str>, ...],   # excludes the Date column
            'units': [<str>, ...],          # excludes the Date column
          },
          'time_series_times':  ['YYYY-MM-DD', ...],
          'time_series_values': [[col0...], [col1...], ...],   # column-major
        }
    """
    with io.open(path, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()

    i = 0
    title = lines[i].strip() if lines else ''
    i += 1

    header = {'title': title}

    # Key/value lines until the column-name line, which begins with 'Date'.
    while i < len(lines) and not lines[i].strip().startswith('Date'):
        line = lines[i]
        if ',' in line:
            label, value = line.split(',', 1)
            label = label.strip().rstrip(':').strip()
            value = value.strip()
            if label:
                header[label] = float(value) if label == 'Area' else value
        # A line with no comma is a free-text note (e.g. the LBRM units note).
        i += 1

    # Column-name line ('Date,...'), then the units line ('YYYY-MM-DD,...').
    column_names = [c.strip() for c in lines[i].split(',')][1:]
    units = [u.strip() for u in lines[i + 1].split(',')][1:]
    i += 2

    times = []
    rows = []
    for line in lines[i:]:
        if not line.strip():
            continue
        fields = line.split(',')
        times.append(fields[0].strip())
        rows.append([_to_float_or_none(f) for f in fields[1:]])

    # Row-major -> column-major, so values[i] aligns with column_names[i].
    time_series_values = [[row[c] for row in rows] for c in range(len(column_names))]

    header['column_names'] = column_names
    header['units'] = units

    return {
        'header': header,
        'time_series_times': times,
        'time_series_values': time_series_values,
    }


def build_path(header, column_name):
    """Build the DSS /a/b/c/d/e/f/ path name for one column (not used in v1)."""
    b = '%s %s' % (header.get('Lake', ''), header.get('Subbasin', ''))
    parts = [DSS_A_PART, b, column_name, '', DSS_E_PART, DSS_F_PART]
    return '/' + '/'.join(parts) + '/'


def print_structure(path, contents):
    """Print the parsed structure of one file to the screen."""
    header = contents['header']
    times = contents['time_series_times']
    values = contents['time_series_values']
    cols = header['column_names']
    units = header['units']
    nrows = len(times)

    print('=' * 72)
    print('FILE     : %s' % path)
    print('TITLE    : %s' % header['title'])
    print('  Lake        = %s' % header.get('Lake'))
    print('  Subbasin    = %s' % header.get('Subbasin'))
    print('  Area        = %s' % header.get('Area'))
    print('  Starts(YMD) = %s' % header.get('Starts(YMD)'))
    print('  Ends(YMD)   = %s' % header.get('Ends(YMD)'))
    print('  NewDataStart(YMD) = %s' % header.get('NewDataStart(YMD)'))
    print('  column_names = %s' % cols)
    print('  units        = %s' % units)
    print('TIME STEPS  : %d   (first=%s  last=%s)'
          % (nrows, times[0] if times else '-', times[-1] if times else '-'))
    print('COLUMNS     : %d' % len(cols))

    preview = 3
    for ci in range(len(cols)):
        series = values[ci] if ci < len(values) else []
        nmissing = sum(1 for v in series if v is None)
        head = series[:preview]
        tail = series[-preview:]
        print('  [%d] %-12s (%s)  n=%d  missing=%d'
              % (ci, cols[ci], units[ci] if ci < len(units) else '?',
                 len(series), nmissing))
        print('        first=%s ... last=%s' % (head, tail))
        print('        dss path = %s' % build_path(header, cols[ci]))


def write_to_dss(dss_filename, contents_list):
    """Write one DSS time series per data column to dss_filename.

    <output.dss> is opened once (created if absent); every column of every file
    is written, then the file is closed.  The ``hec.*`` imports are local so CSV
    parsing stays independent of DSS.  Returns the number of series written.
    """
    from hec.io import TimeSeriesContainer
    from hec.heclib.dss import HecDss
    from hec.heclib.util import HecTime, Heclib
    from hec.script import Constants

    # Quiet the DSS per-record console log (keep genuine errors); the
    # -----DSS--- chatter otherwise interleaves with our own output.
    Heclib.zset("MLVL", "", 1)

    undefined = Constants.UNDEFINED
    written = 0
    dss = HecDss.open(dss_filename)
    try:
        for contents in contents_list:
            header = contents['header']
            cols = header['column_names']
            units = header['units']

            # The Date column is shared by every series in this file.
            times = [HecTime(d, DSS_TIME_LABEL).value()
                     for d in contents['time_series_times']]

            for ci, column_name in enumerate(cols):
                series = contents['time_series_values'][ci]
                values = [undefined if v is None else v for v in series]

                tsc = TimeSeriesContainer()
                tsc.fullName = build_path(header, column_name)
                tsc.interval = DSS_INTERVAL_MINUTES
                tsc.units = units[ci] if ci < len(units) else ''
                tsc.type = determine_type(column_name)
                tsc.times = times
                tsc.values = values
                tsc.numberValues = len(values)
                if times:
                    tsc.startTime = times[0]
                    tsc.endTime = times[-1]

                dss.put(tsc)
                written += 1
                print('  wrote %s  n=%d  missing=%d  units=%s  type=%s'
                      % (tsc.fullName, len(values),
                         sum(1 for v in series if v is None),
                         tsc.units, tsc.type))
    finally:
        dss.close()

    return written


def main(argv):
    if len(argv) < 3:
        program = os.path.basename(argv[0]) if argv else 'subbasin_to_dss.py'
        print('usage: %s <output.dss> <input_dir>' % program)
        return 2

    dss_filename = argv[1]
    input_dir = argv[2]
    files = sorted(glob.glob(os.path.join(input_dir, '*.csv')))

    if not files:
        print('No *.csv files found in: %s' % input_dir)
        return 1

    contents_list = []
    for f in files:
        contents = read_file(f)
        print_structure(f, contents)
        contents_list.append(contents)

    print('=' * 72)
    print('Writing DSS file: %s' % dss_filename)
    written = write_to_dss(dss_filename, contents_list)
    print('=' * 72)
    print('Done. Parsed %d file(s), wrote %d time series to %s'
          % (len(contents_list), written, dss_filename))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
