import pandas as pd
import numpy as np
from tqdm import tqdm
from config import corr_xx_path, corr_xy_path, masks_path

def IFS(corXX, corXY, level_xx, level_xy):
    corXY = corXY.copy().values
    mask = [False] * len(corXX)
    while np.max(corXY) > level_xy:
        i_bestXY = np.argmax(corXY)
        # print("Лучший:", i_bestXY, "\nПохожие:")
        mask[i_bestXY] = True
        corXY[i_bestXY] = 0
        for i in range(corXX.shape[0]):
            if mask[i] == False:
                if corXY[i]>0:
                    if corXX.iloc[i_bestXY, i]>level_xx:
                        corXY[i] = 0
                        # print(i)
    return mask

level_xx = 0.995
level_xy = 0.0
masks_path.mkdir(parents=True, exist_ok=True)
corr_paths = list(zip(list(corr_xx_path.glob('*R*.feather')), list(corr_xy_path.glob('*R*.feather'))))
for xx_file, xy_file in tqdm(corr_paths):
    corr_xx = pd.read_feather(xx_file)
    corr_xy = pd.read_feather(xy_file)
    sensor_name = xx_file.name.removeprefix('corr_XX-')
    elem_names = [i for i in corr_xy.columns]
    masks = []
    for element in elem_names:
        ifs_result = IFS(corr_xx, corr_xy[element], level_xx, level_xy)
        # print(sensor_name, element, sum(ifs_result))
        masks.append(ifs_result)
    result_df = pd.DataFrame(masks, index=elem_names, columns=corr_xx.columns).T
    result_df.to_feather(masks_path / sensor_name)