"""Versioned, metric research overlays independent from CG camera helpers."""
import math
import re

MAX_RESEARCH_LAYERS = 64
MAX_LAYER_POSITIONS = 100_000
MAX_LAYER_SEGMENTS = 100_000
MAX_TOTAL_POSITIONS = 200_000
MAX_TOTAL_SEGMENTS = 200_000


def validate_research_layers(layers, source_ids, asset_ids):
    """Validate without converting coordinates, dropping metadata or mutating input."""
    if not isinstance(layers, list) or len(layers) > MAX_RESEARCH_LAYERS:
        raise ValueError('researchLayers: требуется массив, максимум 64 слоя')
    ids = set()
    total_positions = total_segments = 0
    for layer in layers:
        if not isinstance(layer, dict):
            raise ValueError('researchLayers: слой должен быть объектом')
        if type(layer.get('version')) is not int or layer['version'] != 1:
            raise ValueError('researchLayers: поддерживается версия слоя 1')
        ident = layer.get('id')
        if not isinstance(ident, str) or not ident.strip() or len(ident) > 100 or ident in ids:
            raise ValueError('researchLayers: требуются уникальные непустые строковые id')
        ids.add(ident)
        label = f'researchLayers[{ident}]'
        if not isinstance(layer.get('name'), str) or not layer['name'].strip() or len(layer['name']) > 200:
            raise ValueError(f'{label}: требуется непустое имя до 200 символов')
        if layer.get('kind') not in ('points', 'lines'):
            raise ValueError(f'{label}: неизвестный kind; поддерживаются points и lines')
        if type(layer.get('visible')) is not bool:
            raise ValueError(f'{label}: visible должен быть boolean')
        if layer.get('units') != 'm' or layer.get('coordinateFrame') != 'project-x-y-z':
            raise ValueError(f'{label}: нужны units=m и coordinateFrame=project-x-y-z; преобразуйте данные явно')
        if not isinstance(layer.get('color'), str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', layer['color']):
            raise ValueError(f'{label}: color должен быть #RRGGBB')
        positions = layer.get('positions')
        if not isinstance(positions, list) or not 1 <= len(positions) <= MAX_LAYER_POSITIONS:
            raise ValueError(f'{label}: требуется 1…100000 позиций')
        total_positions += len(positions)
        if total_positions > MAX_TOTAL_POSITIONS:
            raise ValueError('researchLayers: суммарно допускается 200000 позиций')
        for p in positions:
            if not isinstance(p, list) or len(p) != 3 or any(
                isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or abs(v) > 1000
                for v in p
            ):
                raise ValueError(f'{label}: позиция должна содержать три конечные координаты в пределах ±1000 м')
        segments = layer.get('segments', [])
        if not isinstance(segments, list) or len(segments) > MAX_LAYER_SEGMENTS:
            raise ValueError(f'{label}: segments должен быть массивом, максимум 100000 отрезков')
        if layer['kind'] == 'points' and segments:
            raise ValueError(f'{label}: слой points не должен содержать отрезки')
        if layer['kind'] == 'lines' and not segments:
            raise ValueError(f'{label}: lines требует явный непустой массив segments')
        total_segments += len(segments)
        if total_segments > MAX_TOTAL_SEGMENTS:
            raise ValueError('researchLayers: суммарно допускается 200000 отрезков')
        for pair in segments:
            if not isinstance(pair, list) or len(pair) != 2 or any(type(i) is not int or not 0 <= i < len(positions) for i in pair) or pair[0] == pair[1]:
                raise ValueError(f'{label}: отрезок задаётся двумя различными индексами positions')
        for field, available in [('sourceIds', source_ids), ('assetIds', asset_ids)]:
            refs = layer.get(field)
            if not isinstance(refs, list) or len(refs) > 100 or any(not isinstance(ref, str) or ref not in available for ref in refs):
                raise ValueError(f'{label}: {field} должен ссылаться на существующие файлы проекта')
            if len(refs) != len(set(refs)):
                raise ValueError(f'{label}: повторяющиеся ссылки {field}')
        if not isinstance(layer.get('provenance'), dict):
            raise ValueError(f'{label}: provenance должен быть объектом')
    return layers
