## (c) 2020 David Torres Ocana
## This code is licensed under MIT license (see LICENSE.txt for details)

from flask import Flask, render_template
import argparse
from matplotlib import cm
from flask_socketio import SocketIO, emit
import time
import threading
import pykitti
import itertools
from utils import *

# App configuration:
app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True, ping_timeout = 600)# use gevent https://flask-socketio.readthedocs.io/en/latest/

# KITTI Velo: Configure here you sequence. Read https://github.com/utiasSTARS/pykitti
basedir = 'data'
date = '2011_09_26'
drive = '0001'
data = pykitti.raw(basedir, date, drive, frames=range(0, 107, 1))
velo_iter = itertools.cycle(data.velo)

# Downsampling params: You can increase this up to Maximum points in your pointcloud (see utils.py) 
#                     but performance may suffer because of Client's computing capability or bandwidth limitations
samples_size = 20000 # Same as in Threejs_app
idx_downsample = get_skew_sample_idx(samples_size, np.array(range(64)))[0]

@app.route('/')
def index():
    return render_template('points.html')

def get_cloud_packed():
    ''' Iterate through Pointcloud generator which provides data in the format [x,y,z,intensity] and packs 
    (pointcloud, colors) into binaries ready for client's renderer'''
    velo_data = next(velo_iter)
    sampling = np.clip(idx_downsample, 0, velo_data.shape[0] - 1 )
    points = velo_data[sampling, :3].astype(np.float32)
    intensities = (255.*velo_data[sampling, -1]).astype(int)
    # change to THREEjs coordinates
    points[:,1] *= -1.
    points[:,1:] = points[:,2:0:-1]

    # Package into binary straight to client's GPU
    points_bin = points.flatten().tobytes()
    color_map = cm.jet(intensities)[:,:3]
#     color_map = cm.jet( (127.*points[:,1] + 255.).astype(int) )[:,:3] # Z as color
    colors_bin = (255.*color_map.flatten()).astype(np.uint8).tobytes()

    return (points_bin, colors_bin) # Return (False, False) to stop the streaming at any time

@socketio.on('socket_ready')
def confirmation_socket(in_data):
    print('       Client says: ', in_data)

def cloud_stream_request_thread():
    '''  Thread pushing data in Async. manner: push at a set frequency'''
    time_before = time.time()
    while True:
        velo_bins = get_cloud_packed()
        if velo_bins[0]==False:
            socketio.emit('push_cloud_stream', False) # send False to stop the streaming at any time
            return 0
        else:
            socketio.emit('push_cloud_stream', [velo_bins[0],velo_bins[1]])
            time_before = time.time()

        while (time.time() - time_before) < 0.1: # 10Hz
            socketio.sleep(0.005)

# Launch Async. push
@socketio.on('cloud_stream_hungry')
def cloud_stream_request(in_data):
    x = threading.Thread(target=cloud_stream_request_thread)
    x.start()
    return 'ok', 200

@socketio.on('cloud_hungry')
def cloud_request(in_data):
    '''Synchronous data pushing: Wait until client request (after receiving) data'''
    velo_bins = get_cloud_packed()
    emit('push_cloud', [velo_bins[0],velo_bins[1]])
    socketio.sleep(0)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Pointcloud streamer', description=" Demo of pointcloud streaming with Flask and Three.js")
    parser.add_argument("--port", type=int, help="port to launch in", default=9001)
    parser.add_argument( '-d', '--debug',
        help="Launch in debug mode",
        action="store_true", required = False, default=False)
    parser.add_argument( '-p', '--production',
        help="Launch in production mode, otherwise development mode",
        action="store_true", required = False)
    args = parser.parse_args()
    
    app.config['ENV'] = 'production' if args.production else 'development'
    app.config['DEBUG'] = args.debug

    socketio.run(app, host='localhost', port=args.port)
