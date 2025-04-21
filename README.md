Clone this repository
```bash
git clone https://github.com/Shchurov-nk/gas-sensors.git
```

Download miniconda

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
Make it executable
```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```
Run
```bash
./Miniconda3-latest-Linux-x86_64.sh
```
Activate conda in new bash
```
bash
conda --version
```

Create new environment
```bash
cd gas-sensors
conda env create -n gassens -f environment.yml
```
Activate new environment from environment.yml
```bash
conda activate gassens
```
Run python scripts in order

```bash
python 01-generate_datasets.py
python 02-generate_masks.py
python 03-train_model.py
```

TODO: create main.py file and treat all 3 files as modules
```python
# main.py
from generate_datasets import main as generate_datasets
from generate_masks import main as generate_masks
from train_model import main as train_model

if __name__ == "__main__":
    generate_datasets()  # 01
    generate_masks()      # 02
    train_model()         # 03
```
```python
# 01-generate_datasets.py
# ... existing imports ...

def main():
    # Move all existing code here (except imports)
    raw_trn = raw_data_path / 'Linear_long_1_merged_cnt_trn.csv'
    # ... rest of the code ...

if __name__ == "__main__":
    main()
```