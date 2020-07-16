import numpy as np

def get_skew_sample_idx(num_samples, velo_vertical_channel_shuffle):
    ''' Generate non-uniform Velodyne HDL-64 Poincloud sampling idxs'''
    H_velo = int(132864/64) # 132864 is aprox the maximum points for a Velodyne HDL-64
    uniform_probs = np.random.uniform(0,1,(64,H_velo))

    x = np.linspace(0, H_velo-1, H_velo)
    y = np.linspace(0, 1, 64)
    xv, yv = np.meshgrid(x, y)

    skew_probs = uniform_probs*np.log((1 - yv + 2))
    # normalize
    skew_probs = skew_probs*0.5/skew_probs.mean()

    sample_grid = skew_probs>(1 - num_samples/(64*H_velo))

    while np.sum(sample_grid)<num_samples: # Fill up to required sample size
        sample_grid[int(np.random.uniform(64)), int(np.random.uniform(H_velo))] = True
        
    return np.where(sample_grid[velo_vertical_channel_shuffle[::-1], :].T.flatten())[0], sample_grid

