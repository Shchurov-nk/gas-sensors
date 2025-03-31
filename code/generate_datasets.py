import pandas as pd
from config import raw_data_path, interim_data_path, processed_data_path, corr_xx_path, corr_xy_path

num_timesteps_sensor = 1201 # Num of timesteps (columns) for each sensor
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

raw_trn = raw_data_path / 'Linear_long_1_merged_cnt_trn.csv'
raw_vld = raw_data_path / 'Linear_long_1_merged_cnt_vld.csv'
raw_tst = raw_data_path / 'Linear_long_1_merged_cnt_tst.csv'

# Create directories if not exists
interim_data_path.mkdir(parents=True, exist_ok=True)
processed_data_path.mkdir(parents=True, exist_ok=True)
corr_xx_path.mkdir(parents=True, exist_ok=True)
corr_xy_path.mkdir(parents=True, exist_ok=True)

df_trn = pd.read_csv(raw_trn)
df_vld = pd.read_csv(raw_vld)
df_tst = pd.read_csv(raw_tst)

dataframes = {
    'trn' : df_trn,
    'vld': df_vld,
    'tst': df_tst
}

for subset_name, df in dataframes.items():
    df.drop(columns=cols_to_drop, inplace=True)
    df.to_feather(interim_data_path / f'{subset_name}.feather')

    X = df.drop(columns=targets)
    y = df[targets]

    sensors_one_by_one = []
    X_cols = X.columns.tolist()
    prefixes = [i.split('_')[0]+'_' for i in X_cols[::num_timesteps_sensor]]
    for prefix in prefixes:
        one_sensor_cols = [i for i in X_cols if i.startswith(prefix)]
        sensor_name = prefix[:-1]
        X_sensor = X[one_sensor_cols]
        X_sensor.to_feather(interim_data_path / f'{sensor_name}-{subset_name}.feather')

        if subset_name == 'trn':
            corr_XX = X_sensor.corr()
            corr_XX.to_feather(
                corr_xx_path / f'corr_XX-{sensor_name}.feather'
                )
            
            corr_XY = pd.DataFrame()
            for y_col in y.columns:
                corr_XY[y_col] = X_sensor.corrwith(y[y_col])
            corr_XY.to_feather(
                corr_xy_path / f'corr_XY-{sensor_name}.feather'
                )