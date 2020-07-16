/* (c) 2020 David Torres Ocana
 This code is licensed under MIT license (see LICENSE.txt for details)
 */

var scene, renderer, camera;
var controls;
var tgeometry;
var pointCloud, positions, colors, lut;
var MAX_POINTS = 20000; // Same in backend
var width, height;

threejs_init();
animate();
// Synchronous mode
var startTime = Date.now();
socket.on('push_cloud',
          function(data) {
                latency = Date.now() - startTime;
                if ((100. - latency)>0.){ // every 100ms, 10Hz
                    setTimeout(function() {}, 100. - latency);
                }
                if(data[0]!=false){
                    socket.emit('cloud_hungry', 'cloud_hungry');
                    startTime = Date.now();
                    if(data[0]!='pause'){
                        pointCloud.geometry.attributes.position.array = data[0];
                        pointCloud.geometry.attributes.position.needsUpdate = true;
                        pointCloud.geometry.attributes.color.array = data[1];
                        pointCloud.geometry.attributes.color.needsUpdate = true;
                    }
                }
});
// Async mode
socket.on('push_cloud_stream', 
          function(data) {
                if(data[0]!=false){
                    if(data[0]!='pause'){
                        pointCloud.geometry.attributes.position.array = data[0];
                        pointCloud.geometry.attributes.position.needsUpdate = true;
                        pointCloud.geometry.attributes.color.array = data[1];
                        pointCloud.geometry.attributes.color.needsUpdate = true;
                    }
                }
});

function update() {
  controls.update();
  renderer.render(scene, camera);
}

function threejs_init() {
    renderer = new THREE.WebGLRenderer( {antialias:true} );

    // inside div:
    container = document.getElementById('canvas');
    width = window.innerWidth;
    height = window.innerHeight;
    renderer.setSize(width, height);
    container.appendChild( renderer.domElement );
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(45, width/height, 0.1, 200);
    camera.position.x = -40;
    camera.position.y = 35;
    camera.position.z = 35;
    camera.lookAt(new THREE.Vector3(0,0,0));

    console.log(THREE);
    controls = new THREE.OrbitControls(camera, renderer.domElement);

    var tmaterial = new THREE.PointsMaterial({size: 0.3, opacity: 1, vertexColors: THREE.VertexColors}); // color: 0xff0000,  vertexColors: true
    
    tgeometry = new THREE.BufferGeometry();
    positions = new Float32Array( MAX_POINTS * 3 ); // 3 vertices per point
    tgeometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
    
    colors = new Uint8Array( MAX_POINTS * 3 ); // 3 colors RGB per point
    tgeometry.addAttribute( 'color', new THREE.BufferAttribute( colors, 3, true) ); // SET color attributes
    
    pointCloud = new THREE.Points(tgeometry, tmaterial);
    scene.add(pointCloud);
    
    // Add grid helper
    var gridHelper = new THREE.GridHelper( 20, 20);
    gridHelper.colorGrid = 0xE8E8E8;
    gridHelper.position.y -= 1.75; // approx Velo calib
    scene.add( gridHelper );
    
    var radius = 50;
    var radials = 3;
    var circles = 5;
    var divisions = 64;

    var gridHelper2 = new THREE.PolarGridHelper( radius, radials, circles, divisions, 0xE8E8E8, 0xE8E8E8 );
    gridHelper2.position.y -= 1.75; // approx Velo calib
    gridHelper2.geometry.rotateY(Math.PI/2.);
    scene.add( gridHelper2 );

    window.addEventListener ('resize', onWindowResize, false);
}

function onWindowResize () {
    width = window.innerWidth;
    height = window.innerHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize (width, height);
}

function animate() {
    controls.update();
    requestAnimationFrame ( animate );  
    renderer.render (scene, camera);
}
