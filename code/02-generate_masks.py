import pandas as pd
import numpy as np
from multiprocessing import Pool
from config import corr_xx_path, corr_xy_path, masks_path, level_xx, level_xy
import pathlib

def IFS(corXX, corXY, level_xx, level_xy):
    """Feature selection algorithm"""
    corXY = corXY.copy().values
    mask = [False] * len(corXX)
    while np.max(corXY) > level_xy:
        i_bestXY = np.argmax(corXY)
        mask[i_bestXY] = True
        corXY[i_bestXY] = 0
        for i in range(corXX.shape[0]):
            if not mask[i] and corXY[i] > 0 and corXX.iloc[i_bestXY, i] > level_xx:
                corXY[i] = 0
    return mask

def process_file_pair(file_pair):
    """Process a single pair of correlation files"""
    xx_file, xy_file = file_pair
    
    # Read data files
    corr_xx = pd.read_feather(xx_file)
    corr_xy = pd.read_feather(xy_file)
    
    # Get sensor name from filename
    sensor_name = xx_file.name.removeprefix('corr_XX-')
    elem_names = corr_xy.columns.tolist()
    
    # Process all elements for this sensor
    masks = []
    for element in elem_names:
        ifs_result = IFS(corr_xx, corr_xy[element], level_xx, level_xy)
        print(f"Processed {sensor_name} - {element}, selected {sum(ifs_result)} features")
        masks.append(ifs_result)
    
    # Save results
    result_df = pd.DataFrame(masks, index=elem_names, columns=corr_xx.columns).T
    result_df.to_feather(masks_path / sensor_name)
    return sensor_name  # Return value not used, but helpful for tracking

if __name__ == '__main__':
    # Create output directory if needed
    masks_path.mkdir(parents=True, exist_ok=True)
    
    # Get and sort file pairs to ensure proper matching
    xx_files = sorted(corr_xx_path.glob('*R*.feather'))
    xy_files = sorted(corr_xy_path.glob('*R*.feather'))
    corr_paths = list(zip(xx_files, xy_files))
    
    # Create multiprocessing pool
    with Pool() as pool:
        # Process files in parallel with progress tracking
        results = []
        for result in pool.imap(process_file_pair, corr_paths):
            results.append(result)
    print(f'Processed sensors: {results}')