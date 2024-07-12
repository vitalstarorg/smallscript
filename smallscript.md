### Development Runbook

#### Links
- [vitalstarorg/smallscript](https://github.com/vitalstarorg/smallscript)


#### >>>] ------ Now ------

```bash
conda activate nbs
jupyter lab -y --NotebookApp.token='' --notebook-dir=.
```

#### 240712 Change to Apache License 2.0
- Protect users from patent claims

#### 240701 Genesis
- Choose MIT license for simplicity.
```bash
git clone git@github.com:vitalstarorg/smallscript.git

# setup nbs conda
cd nbs
conda create -y --name=nbs "python=3.9"
  # conda deactivate
  # conda remove -y -n nbs --all

conda activate nbs
pip install -r requirements.txt
python -m ipykernel install --user --name=nbs
  # jupyter kernelspec list

jupyter lab -y --NotebookApp.token='' --notebook-dir=.
```

