# subbasin_to_dss

Reads the model's `*.csv` output and writes one HEC-DSS daily time series per data column.

## Requirements

HEC-DSSVue (provides Jython + the `hec.*` classes). Run with its `jython.exe`, not standalone Python. Output is DSS version 7.

## Run

```bat
C:\bin\HEC-DSSVue-4.2.3\jython.exe subbasin_to_dss.py output.dss <input_dir>
```

- `output.dss` - DSS file to create/append.
- `<input_dir>` - directory of `*.csv` files to read.

Each column becomes its own series with path `/Superior/<Lake> <Subbasin>/<column>//1Day/GLSHFS-OPERATIONAL-HISTORIC/`.

## Notes

- Units come from the CSV; `NA`/blank are written as DSS missing.
- Series type (`INST-VAL`/`PER-CUM`) is set by `DSS_TYPE_BY_COLUMN` near the top of `subbasin_to_dss.py`.
