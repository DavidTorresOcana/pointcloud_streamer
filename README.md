# Flask pointcloud streamer

This is demo of pointcloud streaming from a Flask based back-end to Three.js running front-end using websockets for low latency.

For demo purposes the open source [KITTI raw data](http://www.cvlibs.net/datasets/kitti/raw_data.php) is used, but this framework can be adapted to any other pointcloud type of data.

For the back-end, Flask is used in conjunction with [Flask-socketio](https://flask-socketio.readthedocs.io/en/latest/) to enable connectivity with [Socket.io](https://socket.io/) client.
On the front-end, [Three.js](https://threejs.org/) is used as rendering engine.

Stream pointclouds from anywhere!
<p align="center">
  <img src="assets/demo.gif" alt="Example demo" width="950" />
</p>

## Get started:

The main files are:
* ```app.py```: back-end Flask application
* ```static/js/three_app.js```: front-end Three.js based application
* ```templates/points.html```: page html

If you are looking for developing/adapting your application, those are the main files to look at. Comments should guide you through the code. E.g. you can choose the streaming mode by un/commenting ```templates/points.html``` lines 20/21.

### Dependencies and installation:

* python 3.6+
    * gevent
    * gevent-websocket
    * flask-socketio>=5.1.1
    * Flask
    * numpy
    * uwsgi
    * pykitti

To get started, install all requirements with
```pip3 install -r requirements.txt```

Make sure ```eventlet``` library is not installed in your system by ```pip3 uninstall eventlet```

This application was tested on Ubuntu 18, but it should not be complicated to make it run in other OS.

### Get sample data:

Download any KITTI raw sequence's (synced+rectified) data and calibrations from [here](http://www.cvlibs.net/datasets/kitti/raw_data.php) and uncompress into ```data/```

To configure your KITTI sequence, read [pykitti docs](https://github.com/utiasSTARS/pykitti) and modify ```app.py``` to run your specific sequence. By default *2011_09_26* sequence *0001* is used.


## Run application:

To execute the back-end execute:
```uwsgi --http :9002 --gevent 5 --http-websockets --master --wsgi-file app.py --callable app```

You can then open the front-end in your web-browser ```localhost:9002``` to visualize the streaming.

## LICENSE:
MIT License

Copyright (c) 2020 David Torres Ocana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
