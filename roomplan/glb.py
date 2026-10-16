"""Structural checks for self-contained GLB v2 mesh results from local providers.

Based on the Khronos glTF 2.0 GLB layout. This checks container integrity,
embedded storage bounds and mesh accessor references; it is not the full Khronos
semantic/material validator and does not assess inferred shape quality.
https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#glb-file-format-specification
"""
import json
import struct

JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def _integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'GLB: invalid {label}')
    return value


def _index(value, sequence, label):
    index = _integer(value, label)
    if index >= len(sequence):
        raise ValueError(f'GLB: out-of-range {label}')
    return sequence[index]


def _objects(document, field):
    items = document.get(field, [])
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise ValueError(f'GLB: invalid {field}')
    return items


def validate_glb(raw):
    """Return decoded JSON after validating a portable, nonempty GLB mesh.

No bytes are changed. Unknown additional chunks are skipped as required by the
container format. External buffers/images are refused because this provider
contract must return one portable GLB rather than unresolved sidecar files.
"""
    if not isinstance(raw, (bytes, bytearray)) or not 20 <= len(raw) <= 100 * 1024 * 1024:
        raise ValueError('GLB: truncated or oversized container')
    magic, version, declared = struct.unpack_from('<III', raw)
    if magic != 0x46546C67 or version != 2 or declared != len(raw):
        raise ValueError('GLB: invalid magic, version or total length')
    chunks = []; offset = 12
    while offset < len(raw):
        if offset + 8 > len(raw):
            raise ValueError('GLB: truncated chunk header')
        length, kind = struct.unpack_from('<II', raw, offset); offset += 8
        if length % 4 or offset + length > len(raw):
            raise ValueError('GLB: misaligned or out-of-bounds chunk')
        chunks.append((kind, raw[offset:offset + length])); offset += length
    if not chunks or chunks[0][0] != JSON_CHUNK or sum(k == JSON_CHUNK for k, _ in chunks) != 1:
        raise ValueError('GLB: exactly one leading JSON chunk is required')
    bins = [(i, data) for i, (kind, data) in enumerate(chunks) if kind == BIN_CHUNK]
    if len(bins) > 1 or (bins and bins[0][0] != 1):
        raise ValueError('GLB: BIN chunk must occur once immediately after JSON')
    try:
        def reject_constant(value): raise ValueError(f'Invalid JSON constant {value}')
        document = json.loads(chunks[0][1].decode('utf-8'), parse_constant=reject_constant)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ValueError('GLB: invalid JSON chunk') from error
    if not isinstance(document, dict) or not isinstance(document.get('asset'), dict) or document['asset'].get('version') != '2.0':
        raise ValueError('GLB: asset.version must be 2.0')
    buffers = _objects(document, 'buffers')
    if len(buffers) != 1 or not bins or 'uri' in buffers[0]:
        raise ValueError('GLB: provider mesh requires one embedded buffer')
    byte_length = _integer(buffers[0].get('byteLength'), 'buffer byteLength', 1)
    if not byte_length <= len(bins[0][1]) <= byte_length + 3:
        raise ValueError('GLB: embedded buffer length mismatch')
    views = _objects(document, 'bufferViews')
    for view in views:
        _index(view.get('buffer'), buffers, 'bufferView.buffer')
        start = _integer(view.get('byteOffset', 0), 'bufferView.byteOffset')
        length = _integer(view.get('byteLength'), 'bufferView.byteLength', 1)
        if start + length > byte_length:
            raise ValueError('GLB: bufferView exceeds embedded buffer')
        if 'byteStride' in view:
            stride = _integer(view['byteStride'], 'bufferView.byteStride', 4)
            if stride > 252 or stride % 4:
                raise ValueError('GLB: invalid bufferView stride')
    accessors = _objects(document, 'accessors')
    component_sizes = {5120:1, 5121:1, 5122:2, 5123:2, 5125:4, 5126:4}
    dimensions = {'SCALAR':(1,1), 'VEC2':(2,1), 'VEC3':(3,1), 'VEC4':(4,1), 'MAT2':(2,2), 'MAT3':(3,3), 'MAT4':(4,4)}
    for accessor in accessors:
        component = accessor.get('componentType'); shape = accessor.get('type')
        if type(component) is not int or component not in component_sizes or not isinstance(shape, str) or shape not in dimensions:
            raise ValueError('GLB: invalid accessor component or type')
        count = _integer(accessor.get('count'), 'accessor.count', 1)
        component_size = component_sizes[component]; rows, columns = dimensions[shape]
        element_size = rows * component_size if columns == 1 else ((rows * component_size + 3) // 4 * 4) * columns
        if 'bufferView' in accessor:
            view = _index(accessor['bufferView'], views, 'accessor.bufferView')
            start = _integer(accessor.get('byteOffset', 0), 'accessor.byteOffset')
            stride = view.get('byteStride', element_size)
            if start % component_size or stride < element_size or start + (count - 1) * stride + element_size > view['byteLength']:
                raise ValueError('GLB: accessor exceeds bufferView or has invalid alignment')
        elif 'sparse' not in accessor:
            raise ValueError('GLB: accessor has no storage')
        if 'sparse' in accessor:
            sparse = accessor['sparse']
            if not isinstance(sparse, dict): raise ValueError('GLB: invalid sparse accessor')
            sparse_count = _integer(sparse.get('count'), 'sparse.count', 1)
            if sparse_count > count: raise ValueError('GLB: sparse count exceeds accessor count')
            for field in ('indices', 'values'):
                part = sparse.get(field)
                if not isinstance(part, dict): raise ValueError('GLB: invalid sparse storage')
                view = _index(part.get('bufferView'), views, f'sparse.{field}.bufferView')
                start = _integer(part.get('byteOffset', 0), f'sparse.{field}.byteOffset')
                unit = element_size
                if field == 'indices':
                    index_type = part.get('componentType')
                    if type(index_type) is not int or index_type not in (5121, 5123, 5125):
                        raise ValueError('GLB: invalid sparse index component type')
                    unit = component_sizes[index_type]
                if 'byteStride' in view or start + sparse_count * unit > view['byteLength']:
                    raise ValueError('GLB: sparse storage exceeds bufferView')
    meshes = _objects(document, 'meshes')
    if not meshes:
        raise ValueError('GLB: no mesh geometry')
    for mesh in meshes:
        primitives = _objects(mesh, 'primitives')
        if not primitives: raise ValueError('GLB: empty mesh')
        for primitive in primitives:
            attributes = primitive.get('attributes')
            if not isinstance(attributes, dict) or 'POSITION' not in attributes:
                raise ValueError('GLB: mesh primitive has no POSITION')
            for index in attributes.values(): _index(index, accessors, 'primitive attribute')
            if _index(attributes['POSITION'], accessors, 'POSITION')['type'] != 'VEC3':
                raise ValueError('GLB: POSITION must be VEC3')
            if 'indices' in primitive: _index(primitive['indices'], accessors, 'primitive.indices')
    for image in _objects(document, 'images'):
        if 'uri' in image and not str(image['uri']).startswith('data:'):
            raise ValueError('GLB: external image is not portable')
        if 'bufferView' in image: _index(image['bufferView'], views, 'image.bufferView')
    return document
