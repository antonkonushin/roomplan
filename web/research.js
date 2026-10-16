import * as THREE from 'three';

/** Build data-backed overlays only. Camera routes/helpers belong to the caller.
 * Input must first pass /api/validate. Metres; x,z horizontal, y up; no transform.
 * The returned root is always visible: the caller owns the research master switch.
 * Child names/userData IDs remain stable across scene rebuilds; Three runtime IDs do not.
 */
export function buildResearchLayers(project) {
  const root = new THREE.Group();
  root.name = 'research-layers';
  root.userData.isResearchLayerRoot = true;
  for (const layer of project.researchLayers || []) {
    if (layer.version !== 1 || !['points', 'lines'].includes(layer.kind) ||
        layer.units !== 'm' || layer.coordinateFrame !== 'project-x-y-z') {
      throw new Error(`Unsupported research layer schema: ${layer.id || '(no id)'}`);
    }
    const group = new THREE.Group();
    group.name = `research:${layer.id}`;
    group.visible = layer.visible;
    group.userData = {
      researchLayerId: layer.id,
      researchLayerName: layer.name,
      researchLayerKind: layer.kind,
      sourceIds: [...layer.sourceIds],
      assetIds: [...layer.assetIds],
      provenance: structuredClone(layer.provenance),
    };
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(layer.positions.flat(), 3));
    let drawable;
    if (layer.kind === 'points') {
      drawable = new THREE.Points(geometry, new THREE.PointsMaterial({
        color: layer.color, size: .055, sizeAttenuation: true,
        depthTest: true, depthWrite: false, toneMapped: false,
      }));
    } else {
      geometry.setIndex(layer.segments.flat());
      drawable = new THREE.LineSegments(geometry, new THREE.LineBasicMaterial({
        color: layer.color, depthTest: true, depthWrite: false, toneMapped: false,
      }));
    }
    geometry.computeBoundingSphere();
    drawable.name = `research-geometry:${layer.id}`;
    drawable.userData.researchLayerId = layer.id;
    drawable.renderOrder = 2;
    group.add(drawable);
    root.add(group);
  }
  return root;
}
