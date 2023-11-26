<template>
    <div>
        <div>Opa2</div>
        <div ref="mount"></div>
        {{ consumos }}
    </div>
</template>

<script>
import * as THREE from 'three';


export default {
    data: () => ({
        consumos: {
            '1050': 1.0,
            '1060': 2.0,
            '1070': 3.0,
        }
    }),

    mounted() {
        // Criação da cena
        var scene = new THREE.Scene();

        // Criação da câmera
        var camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
        
        // Criação do renderizador
        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        this.$refs.mount.appendChild(renderer.domElement);
        
        var cupMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
        var waterMaterial = new THREE.MeshBasicMaterial({color: 0x0000ff, transparent: true, opacity: 0.6});

        var i = 0;
        for (var key in this.consumos) {
            // Criação da geometria do copo
            var geometry = new THREE.CylinderGeometry(1, 1, this.consumos[key], 32);
            var cup = new THREE.Mesh(geometry, cupMaterial);
            cup.position.x = i * 3;
            scene.add(cup);
            
            // Criação da geometria da água
            var waterGeometry = new THREE.CylinderGeometry(0.9, 0.9, (this.consumos[key]) - 0.2, 32);
            var water = new THREE.Mesh(waterGeometry, waterMaterial);
            water.position.y = -0.1; // Posicione a água um pouco abaixo do topo do copo
            water.position.x = i * 3;
            scene.add(water);

            i++;
        } 
        
        
        // Função de renderização
        var animate = function () {
            requestAnimationFrame(animate);
            
            // Rotação dos cilindros
            scene.children.forEach(function (child) {
                if (child instanceof THREE.Mesh) {
                    child.rotation.y += 0.001;
                }
            });
                    
            renderer.render(scene, camera);
        };

        animate();
    },
    
    beforeDestroy() {
        // Parar o loop de animação
        cancelAnimationFrame(this.animationFrameId);

        // Limpar a cena
        while(scene.children.length > 0){ 
            scene.remove(scene.children[0]); 
        }

        // Remover o renderizador do div "mount"
        this.$refs.mount.removeChild(renderer.domElement);
    }
}
</script>