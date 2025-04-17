from pathlib import Path

project_path = Path(__file__).parent.parent

data_path = project_path / 'data'

raw_data_path = data_path / 'raw' / 'Linear_long_1_conv'
interim_data_path = data_path / 'interim'
processed_data_path = data_path / 'processed'
corr_xx_path = data_path / 'corr' / 'XX'
corr_xy_path = data_path / 'corr' / 'XY'
masks_path = data_path / 'masks'

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

sensors = [f'R{i}' for i in range(1,13)]