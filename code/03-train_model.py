import time
start_time = time.time()

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # To supress "This TensorFlow binary is optimized..." message

from tqdm import tqdm
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
import tensorflow as tf
# from keras.models import load_model
import joblib
from config import interim_data_path, masks_path, data_path, sensors, targets, params

# My CPU is i5 12400 (6 physical, 12 logical cores)
# Use 6 threads for intra-op parallelism (1 per physical core)
tf.config.threading.set_intra_op_parallelism_threads(6)
# Use 2 threads for inter-op parallelism (to leverage Hyper-Threading)
tf.config.threading.set_inter_op_parallelism_threads(2)

# tf.config.threading.set_intra_op_parallelism_threads(8)
# tf.config.threading.set_inter_op_parallelism_threads(8)

def fit_my_model(X_trn, y_trn, X_vld, y_vld, params):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(32, activation='sigmoid'))
    model.add(tf.keras.layers.Dense(1,  activation='linear'))
    
    adam = tf.keras.optimizers.Adam(learning_rate=params['lr'])
    model.compile(optimizer=adam, loss='mean_squared_error')

    callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        min_delta=params['min_delta'],
        patience=params['patience'],
        verbose=0,
        mode='min',
        baseline=None,
        restore_best_weights=True,
    )

    model.fit(X_trn, y_trn, 
              batch_size=params['batch_size'],
              epochs=params['epochs'],
              verbose=0,
              callbacks=callback,
              validation_data=(X_vld, y_vld),
             )
    return model


y_trn = pd.read_feather(interim_data_path / 'trn_targets.feather') / 100
y_vld = pd.read_feather(interim_data_path / 'vld_targets.feather') / 100

nn_models_path = data_path / 'models' / 'NN'
nn_models_path.mkdir(parents=True, exist_ok=True)

result = []
progr_bar_sensors = tqdm(sensors)
for sensor in progr_bar_sensors:
    progr_bar_sensors.set_postfix_str(f'sensor : {sensor}')

    X_trn = pd.read_feather(interim_data_path / f'{sensor}-trn.feather')
    X_vld = pd.read_feather(interim_data_path / f'{sensor}-vld.feather')

    scalers_path = data_path / 'scalers' / f'{sensor}_scaler.joblib'
    scaler = MinMaxScaler()
    X_trn = pd.DataFrame(scaler.fit_transform(X_trn), columns=X_trn.columns)
    X_vld = pd.DataFrame(scaler.transform(X_vld), columns=X_vld.columns)
    joblib.dump(scaler, scalers_path)

    masks_df = pd.read_feather(masks_path / f'{sensor}.feather')

    progr_bar_targets = tqdm(targets, leave=False)
    for target in progr_bar_targets:
        progr_bar_targets.set_postfix_str(f'target : {target}')
        for to_mask in tqdm([True, False], postfix='mask on/off', leave=False):
            if to_mask == True:
                selected_columns = masks_df.index[masks_df[target]]
            elif to_mask == False:
                selected_columns = masks_df.index
            
            model = fit_my_model(
                X_trn[selected_columns], 
                y_trn[target], 
                X_vld[selected_columns], 
                y_vld[target], 
                params
                )

            model_name = nn_models_path / f'NN_{sensor}_{target}_{to_mask}.keras'
            model.save(model_name)

            y_pred = model.predict(X_vld[selected_columns], verbose=0)

            mae = mean_absolute_error(y_vld[target], y_pred)
            r2 = r2_score(y_vld[target], y_pred)
            result.append([sensor, target, to_mask, mae, r2])

final_result = pd.DataFrame(result, columns=['sensor', 'target', 'mask', 'mae', 'r2'])

final_result.to_excel('final_result.xlsx')

with open('time.txt', 'w') as file_time:
    file_time.write(f"total time: {time.time() - start_time} seconds")