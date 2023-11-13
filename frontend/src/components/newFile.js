import * as THREE from 'three';
import { Water } from 'three/examples/jsm/objects/Water.js';
import { Sky } from 'three/examples/jsm/objects/Sky.js';

export default {
mounted() {
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();

this.$refs.mount.appendChild(renderer.domElement);

// Cria um novo cilindro com:
// - um círculo de raio 5 no topo (1º parâmetro)
// - um círculo de raio 5 na base (2º parâmetro)
// - uma altura de 20 (3º parâmetro)
// - 32 segmentos ao redor de sua circunferência (4º parâmetro)
var geometry = new THREE.CylinderGeometry(5, 5, 20, 32);
var material = new THREE.MeshBasicMaterial({ color: 65280 });
var cylinder = new THREE.Mesh(geometry, material);
scene.add(cylinder);

// Adiciona um plano com textura de água na parte superior do cilindro
var waterGeometry = new THREE.PlaneBufferGeometry(10000, 10000);
var water = new Water(
waterGeometry,
{
textureWidth: 512,
textureHeight: 512,
waterNormals: new THREE.TextureLoader().load('https://threejs.org/examples/textures/waternormals.jpg', function (texture) {
texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
}),
alpha: 1,
sunDirection: new THREE.Vector3(),
sunColor: 16777215,
waterColor: 7695,
distortionScale: 3.7,
fog: scene.fog !== undefined
}
);
water.rotation.x = -Math.PI / 2;
scene.add(water);

// Adiciona um céu
var sky = new Sky();
sky.scale.setScalar(10000);
scene.add(sky);

// Adiciona uma luz solar
var sun = new THREE.Vector3();
var effectController = {
turbidity: 10,
rayleigh: 2,
mieCoefficient: 0.005,
mieDirectionalG: 0.8,
inclination: 0.49,
azimuth: 0.25 // Facing front,
};
var distance = 400000;
var uniforms = sky.material.uniforms;
uniforms['turbidity'].value = effectController.turbidity;
uniforms['rayleigh'].value = effectController.rayleigh;
uniforms['mieCoefficient'].value = effectController.mieCoefficient;
uniforms['mieDirectionalG'].value = effectController.mieDirectionalG;
var theta = Math.PI * (effectController.inclination - 0.5);
var phi = 2 * Math.PI * (effectController.azimuth - 0.5);
sun.x = distance * Math.cos(phi);
sun.y = distance * Math.sin(phi) * Math.sin(theta);
sun.z = distance * Math.sin(phi) * Math.cos(theta);
uniforms['sunPosition'].value.copy(sun);

camera.position.z = 30;

var animate = function () {
requestAnimationFrame(animate);

// Rotação do cilindro
cylinder.rotation.x = 10;
cylinder.rotation.y += 0.01;

// Animação da textura de água
water.material.uniforms['time'].value += 1 / 60;

renderer.render(scene, camera);
};

animate();
}
}

< script /  >
;
