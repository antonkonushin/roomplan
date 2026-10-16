import {Pass,FullScreenQuad as SharedFullScreenQuad} from 'three/addons/postprocessing/Pass.js';

// The tracer disposes temporary quads while resizing texture arrays. Three's default
// quad shares a module-level geometry, also used by the editor's post-processing.
// Give each tracer quad its own geometry so disposal cannot affect the editor.
class FullScreenQuad extends SharedFullScreenQuad {
 constructor(material){super(material);this._mesh.geometry=this._mesh.geometry.clone();}
}
export {Pass,FullScreenQuad};
