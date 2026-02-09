# Skill: Canvas & Three.js Basics

## Purpose
To render 2D (Canvas API) or 3D (Three.js/WebGL) graphics in the browser for games, visualizations, or creative effects.

## When to Use
- **Canvas**: Charts, simple games, image editing.
- **Three.js**: 3D models, immersive experiences, complex particle systems.

## Procedure

### 1. HTML Canvas (2D)
```html
<canvas id="myCanvas" width="500" height="500"></canvas>
<script>
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  
  // Draw Rectangle
  ctx.fillStyle = 'red';
  ctx.fillRect(10, 10, 50, 50);
  
  // Animation Loop
  function animate() {
    ctx.clearRect(0, 0, 500, 500);
    // update and draw...
    requestAnimationFrame(animate);
  }
</script>
```

### 2. Three.js (3D)
Install: `npm install three`
```javascript
import * as THREE from 'three';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Object
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

// Loop
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

### 3. React Integration
Use `@react-three/fiber` for declarative 3D in React.

## Constraints
- **Performance**: WebGL is GPU-intensive. Optimize geometry count and texture sizes.
- **Accessibility**: Canvas content is not readable by screen readers. Provide fallback text or ARIA labels.

## Expected Output
High-performance graphical rendering beyond the capabilities of standard DOM elements.
