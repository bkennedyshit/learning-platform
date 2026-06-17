import * as THREE from "three";
import type { SurfaceEvaluator } from "./expression";

export type SpatialScene = {
  element: HTMLDivElement;
  setSurface: (evaluate: SurfaceEvaluator, domain: number, steps: number) => void;
  dispose: () => void;
};

export function createSpatialScene(): SpatialScene {
  const element = document.createElement("div");
  element.className = "sceneMount";

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050814);
  scene.fog = new THREE.FogExp2(0x050814, 0.035);

  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(5.5, 4.4, 6);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  element.appendChild(renderer.domElement);

  const ambient = new THREE.HemisphereLight(0xffffff, 0x1e293b, 1.0);
  scene.add(ambient);

  const directional = new THREE.DirectionalLight(0xe0f2fe, 3.0);
  directional.position.set(5, 10, 7);
  scene.add(directional);

  const blueLight = new THREE.PointLight(0x38bdf8, 4.0, 20);
  blueLight.position.set(-5, -2, -5);
  scene.add(blueLight);

  const purpleLight = new THREE.PointLight(0x8b5cf6, 4.0, 20);
  purpleLight.position.set(5, -2, 5);
  scene.add(purpleLight);

  const grid = new THREE.GridHelper(10, 20, 0x334155, 0x1e293b);
  grid.position.y = -1.45;
  scene.add(grid);

  const axes = new THREE.AxesHelper(3.5);
  scene.add(axes);

  let surface: THREE.Mesh | undefined;
  let frame = 0;
  let width = 0;
  let height = 0;

  const resizeObserver = new ResizeObserver(([entry]) => {
    if (!entry) {
      return;
    }

    width = Math.max(1, Math.floor(entry.contentRect.width));
    height = Math.max(1, Math.floor(entry.contentRect.height));
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    render();
  });

  function setSurface(evaluate: SurfaceEvaluator, domain: number, steps: number): void {
    if (surface) {
      surface.geometry.dispose();
      scene.remove(surface);
    }

    const geometry = buildSurfaceGeometry(evaluate, domain, steps);
    
    surface = new THREE.Mesh(
      geometry,
      new THREE.MeshPhysicalMaterial({
        color: 0x0ea5e9,
        emissive: 0x0284c7,
        emissiveIntensity: 0.15,
        metalness: 0.9,
        roughness: 0.15,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1,
        transparent: true,
        opacity: 0.85,
        side: THREE.DoubleSide,
      }),
    );
    
    const wireframe = new THREE.LineSegments(
      new THREE.WireframeGeometry(geometry),
      new THREE.LineBasicMaterial({
        color: 0x7dd3fc,
        transparent: true,
        opacity: 0.25,
      })
    );
    surface.add(wireframe);
    
    scene.add(surface);
    render();
  }

  function render(): void {
    renderer.render(scene, camera);
  }

  function animate(): void {
    frame = window.requestAnimationFrame(animate);
    if (surface) {
      surface.rotation.y += 0.004;
    }
    render();
  }

  resizeObserver.observe(element);
  animate();

  return {
    element,
    setSurface,
    dispose: () => {
      window.cancelAnimationFrame(frame);
      resizeObserver.disconnect();
      surface?.geometry.dispose();
      renderer.dispose();
      element.remove();
    },
  };
}

function buildSurfaceGeometry(
  evaluate: SurfaceEvaluator,
  domain: number,
  steps: number,
): THREE.BufferGeometry {
  const geometry = new THREE.BufferGeometry();
  const positions: number[] = [];
  const indices: number[] = [];
  const safeSteps = Math.min(Math.max(steps, 12), 96);
  const span = Math.max(1, domain);

  for (let iy = 0; iy <= safeSteps; iy += 1) {
    const y = -span + (2 * span * iy) / safeSteps;

    for (let ix = 0; ix <= safeSteps; ix += 1) {
      const x = -span + (2 * span * ix) / safeSteps;
      const z = clamp(evaluate(x, y), -2.5, 2.5);
      positions.push(x, z, y);
    }
  }

  const row = safeSteps + 1;
  for (let iy = 0; iy < safeSteps; iy += 1) {
    for (let ix = 0; ix < safeSteps; ix += 1) {
      const a = iy * row + ix;
      const b = a + 1;
      const c = a + row;
      const d = c + 1;
      indices.push(a, c, b, b, c, d);
    }
  }

  geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();

  return geometry;
}

function clamp(value: number, min: number, max: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }

  return Math.min(max, Math.max(min, value));
}
