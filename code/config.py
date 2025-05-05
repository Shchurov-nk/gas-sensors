from pathlib import Path

project_path = Path(__file__).parent.parent

data_path = project_path / 'data'

raw_data_path = data_path / 'raw' / 'Linear_long_1_conv'
interim_data_path = data_path / 'interim'
processed_data_path = data_path / 'processed'
corr_xx_path = data_path / 'corr' / 'XX'
corr_xy_path = data_path / 'corr' / 'XY'
masks_path = data_path / 'masks'

# Targets to predict with ML model
targets = [
    'NO_conc',
    'CH4_conc',
    'H2S_conc',
    'SO2_conc',
    'HCOH_conc',
    'CO_conc',
    'H2_conc',
    'NO2_conc',
    'NH3_conc'
    ]

# Drop columns from raw dataset. 
# Add unused targets here (otherwise they will be added to train dataset)
cols_to_drop = [
    'Source_file', 
    'Cycle', 
    'Time_0', 
    'purge', 
    'air', 
    'NO', 'CH4', 'H2S', 'SO2', 'HCOH', 'CO', 'H2', 'NO2', 'NH3', 
    'After_conc_change_No', 
    'Conc_plateau_No', 
    'Subset'
    ]

# Sensor names in raw dataset
sensors = [f'R{i}' for i in range(1,13)]

# Levels of IFS algorithm (mask generation)
level_xx = 0.9999
level_xy = 0.0

# Parameters of ML model
params = {
    'min_delta' : 0.000,
    'patience' : 100,
    'epochs' : 3000,
    'lr' : 0.001,
    'batch_size' : 32
}