
```bash
conda env create -f environment-cwms.yml
conda activate env-cwms
pip install cwms-python
pip install pip_system_certs
pip install plotly
pip install -i https://test.pypi.org/simple/ hecdss


# upgrades..
pip install --upgrade hecdss
pip install --upgrade cwms-python
```
