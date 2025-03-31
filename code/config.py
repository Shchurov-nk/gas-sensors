from pathlib import Path

project_path = Path(__file__).parent.parent

data_path = project_path / 'data'

raw_data_path = data_path / 'Linear_long_1_conv'
interim_data_path = data_path / 'interim'
processed_data_path = data_path / 'processed'
corr_xx_path = data_path / 'corr' / 'XX'
corr_xy_path = data_path / 'corr' / 'XY'