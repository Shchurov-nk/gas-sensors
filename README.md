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

Optional - use tmux session  
Usefull when running code on a remote host using ssh  
This way connection reset won't affect code execution
```bash
# create new session named "gassens"
tmux new -s gassens
# if connection resets - attach back to the session
tmux attach -t gassens
```

Run python scripts in order
```bash
python 01-generate_datasets.py
python 02-generate_masks.py
python 03-train_model.py
```

If running on a remote host - compress the result
```bash
zip -r gassens_result.zip gas-sensors

```
 Then log out from server and secure copy archive to local host
 ```bash
 scp user@your.server.com:/path/to/gassens_result.zip /home/user/Desktop/
# Note: use your username, server and paths
# You can also use scp to copy raw data to the server
 ```