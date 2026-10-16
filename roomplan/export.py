import html
import math
from .model import CATALOG, polygon_area, validate_project

def esc(x): return html.escape(str(x),quote=True)

def label_anchor(room, objects, scale):
    """Place listing labels in free floor space, avoiding furniture footprints."""
    poly=room['polygon'];xmin=min(v[0] for v in poly);xmax=max(v[0] for v in poly)
    zmin=min(v[1] for v in poly);zmax=max(v[1] for v in poly)
    halfw=min(110,len(room['name'])*4.1)/scale+.05
    halfh=26/scale
    def inside(x,z):
        odd=False
        for a,b in zip(poly,poly[1:]+poly[:1]):
            if (a[1]>z)!=(b[1]>z) and x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]: odd=not odd
        return odd
    boxes=[]
    for o in objects:
        if o.get('kind')=='rug': continue
        c=abs(math.cos(o['rotation']));s=abs(math.sin(o['rotation']))
        rx=(c*o['size'][0]+s*o['size'][2])/2
        rz=(s*o['size'][0]+c*o['size'][2])/2
        boxes.append((o['position'][0],o['position'][2],rx,rz))
    for fz in [.84,.68,.52,.36,.20]:
        for fx in [.5,.3,.7,.15,.85]:
            x=xmin+(xmax-xmin)*fx;z=zmin+(zmax-zmin)*fz
            if not all(inside(x+dx,z+dz) for dx in [-halfw,halfw] for dz in [-halfh,halfh]): continue
            if not any(abs(x-bx)<halfw+rx+.05 and abs(z-bz)<halfh+rz+.05 for bx,bz,rx,rz in boxes): return x,z
    return (xmin+xmax)/2,zmax-.28

def export_svg(project):
    p,_=validate_project(project)
    points=[v for r in p['rooms'] for v in r['polygon']]+[w[k] for w in p['walls'] for k in ('a','b')]
    if not points: raise ValueError('Нет геометрии для экспорта')
    x0=min(v[0] for v in points);x1=max(v[0] for v in points);z0=min(v[1] for v in points);z1=max(v[1] for v in points)
    width=max(.1,x1-x0);depth=max(.1,z1-z0);scale=min(100,1000/width,760/depth)
    ox=100-x0*scale;oz=190-z0*scale;W=width*scale+200;H=depth*scale+330
    X=lambda x: round(ox+x*scale,3);Y=lambda z: round(oz+z*scale,3)
    total=sum(polygon_area(r['polygon']) for r in p['rooms'])
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">',
         '<defs><pattern id="wood" width="96" height="15" patternUnits="userSpaceOnUse"><path d="M0 0H96M0 15H96M47 0V15" fill="none" stroke="#9c7c54" stroke-opacity=".13" stroke-width=".6"/></pattern><pattern id="tile" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M0 0H30V30H0Z" fill="none" stroke="#a0aaa4" stroke-opacity=".3" stroke-width=".7"/></pattern><filter id="shadow" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="1" dy="2.5" stdDeviation="2" flood-color="#263832" flood-opacity=".2"/></filter><linearGradient id="linen" x2="0" y2="1"><stop stop-color="#faf7ee"/><stop offset="1" stop-color="#ded7c8"/></linearGradient></defs>',
         '<rect width="100%" height="100%" fill="#faf9f5"/>',
         f'<text x="60" y="51" font-family="Arial,sans-serif" font-size="13" letter-spacing="3" fill="#4c6e5d">ROOMPLAN / RESIDENCES</text>',
         f'<text x="60" y="94" font-family="Arial,sans-serif" font-size="29" font-weight="600" fill="#253b32">{esc(p["name"])}</text>',
         f'<text x="60" y="124" font-family="Arial,sans-serif" font-size="14" fill="#738178">{total:.1f} м²  ·  Высота {p["ceilingHeight"]:.2f} м  ·  План с расстановкой мебели</text>',
         f'<path d="M60 146H{W-60:.0f}" stroke="#d9dfd6"/>']
    for r in p['rooms']:
        pts=' '.join(f'{X(v[0])},{Y(v[1])}' for v in r['polygon'])
        out.append(f'<polygon points="{pts}" fill="{r.get("color","#e8dfcf")}"/>')
        out.append(f'<polygon points="{pts}" fill="url(#{"tile" if "ван" in r["name"].lower() else "wood"})"/>')
    byid={c['id']:c for c in CATALOG}
    for o in sorted(p['objects'],key=lambda o: (o['position'][1],o['size'][1])):
        kind=o.get('kind') or byid.get(o.get('catalogId'),{}).get('kind','custom')
        w=o['size'][0]*scale;d=o['size'][2]*scale;x=-w/2;z=-d/2;c=o['color'];rot=-o['rotation']*180/math.pi
        out.append(f'<g transform="translate({X(o["position"][0])} {Y(o["position"][2])}) rotate({rot:.2f})" stroke="#5b675d" stroke-width=".8" filter="url(#shadow)"><title>{esc(o["name"])}</title>')
        def rect(a,b,ww,dd,fill,rx=3,stroke=None):
            out.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{max(.1,ww):.2f}" height="{max(.1,dd):.2f}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
        def ellipse(cx,cy,rx,ry,fill): out.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{fill}"/>')
        if kind=='rug':
            rect(x,z,w,d,c,1,'#b8ae97');rect(x+5,z+5,w-10,d-10,'none',1,'#ece7d9')
            for a in range(int(x+10),int(-x-5),8): out.append(f'<path d="M{a} {z+8}V{-z-8}" stroke="#b5ac95" stroke-opacity=".17"/>')
        elif kind in ['sofa','armchair']:
            rect(x,z,w,d,c,8);rect(x+7,z+7,w-14,d*.22,c,5)
            count=3 if kind=='sofa' else 1
            for i in range(count): rect(x+10+i*(w-20)/count,z+d*.34,(w-22)/count,d*.55,c,5)
            rect(x+3,z+8,8,d-13,c,4);rect(-x-11,z+8,8,d-13,c,4)
        elif kind=='bed':
            rect(x,z,w,d,c,5);rect(x+4,z+7,w-8,d-11,'url(#linen)',4)
            rect(x+10,z+13,w*.39,d*.19,'#fffdf5',5);rect(x+w*.53,z+13,w*.39,d*.19,'#fffdf5',5)
            rect(x+5,z+d*.38,w-10,d*.5,c,3)
            out.append(f'<path d="M{x+10} {z+d*.43}H{-x-10}" stroke="#f5f0e8" stroke-width="3"/>')
        elif kind in ['coffeeTable','diningTable']:
            rect(x,z,w,d,c,min(w,d)*.2)
            ellipse(-w*.22,-d*.12,w*.09,w*.09,'#f6f3e8');ellipse(w*.2,d*.08,w*.1,w*.1,'#7b936f')
        elif kind in ['diningChair','officeChair']:
            rect(x,z,w,d,c,6);rect(x+3,z+2,w-6,d*.18,c,3);rect(x+4,z+d*.3,w-8,d*.6,c,4)
        elif kind=='plant':
            ellipse(0,0,w*.32,d*.32,'#c4b39b')
            for a in range(0,360,45):
                out.append(f'<ellipse cx="0" cy="{-d*.2:.2f}" rx="{w*.17:.2f}" ry="{d*.3:.2f}" transform="rotate({a})" fill="{c}" stroke="#527458"/>')
        elif kind=='bathtub':
            rect(x,z,w,d,'#f8f7ee',min(w,d)*.3);rect(x+7,z+9,w-14,d-18,'#dce7e3',min(w,d)*.3);ellipse(0,z+d*.75,2,2,'#8a9d98')
        elif kind=='toilet':
            rect(x,z,w,d*.25,'#f8f7f1',4);ellipse(0,d*.1,w*.48,d*.37,'#fcfbf7');ellipse(0,d*.1,w*.29,d*.23,'#dfe6e2')
        elif kind=='sink':
            rect(x,z,w,d,c,2);rect(x+w*.18,z+d*.17,w*.64,d*.66,'#e4e9e5',8);ellipse(0,0,2,2,'#7a8985');out.append(f'<path d="M0 {z+2}v10" stroke="#798a87" stroke-width="4"/>')
        elif kind=='stove':
            rect(x,z,w,d,c,2);rect(x+5,z+5,w-10,d-10,'#414c49',2)
            for a in [-.23,.23]:
                for b in [-.23,.23]: ellipse(w*a,d*b,w*.13,w*.13,'#59635e')
        elif kind=='tv': rect(x,z,w,max(d,4),'#253632',1)
        else:
            rect(x,z,w,d,c,2)
            if kind in ['wardrobe','cabinet']:
                out.append(f'<path d="M0 {z}V{-z}" stroke="#918777"/><path d="M-4 -4v8M4 -4v8" stroke="#6b7166" stroke-width="1.5"/>')
        out.append('</g>')
    for w in p['walls']:
        out.append(f'<path d="M{X(w["a"][0])} {Y(w["a"][1])}L{X(w["b"][0])} {Y(w["b"][1])}" stroke="#34483e" stroke-width="{w["thickness"]*scale:.2f}" stroke-linecap="square"/>')
    # Anchored metadata: hide detached openings after geometry changes.
    endpoints=[w[k] for w in p['walls'] for k in ['a','b']]
    for opening in p.get('openings',[]):
        a,b=opening['a'],opening['b'];d=math.dist(a,b)
        if opening['kind']=='door' and all(any(math.dist(v,e)<.015 for e in endpoints) for v in [a,b]):
            dx=b[0]-a[0];dz=b[1]-a[1];tip=[a[0]-dz,a[1]+dx]
            out.append(f'<path d="M{X(a[0])} {Y(a[1])}L{X(tip[0])} {Y(tip[1])} M{X(tip[0])} {Y(tip[1])}A{d*scale} {d*scale} 0 0 0 {X(b[0])} {Y(b[1])}" fill="none" stroke="#7b8f80" stroke-width="1.2"/>')
        elif opening['kind']=='window':
            wall=next((w for w in p['walls'] if w['id']==opening.get('wallId')),None)
            if wall and all(abs(math.dist(wall['a'],v)+math.dist(v,wall['b'])-math.dist(wall['a'],wall['b']))<.01 for v in [a,b]):
                out.append(f'<path d="M{X(a[0])} {Y(a[1])}L{X(b[0])} {Y(b[1])}" stroke="#eaf1ed" stroke-width="{wall["thickness"]*scale-3:.1f}"/><path d="M{X(a[0])} {Y(a[1])}L{X(b[0])} {Y(b[1])}" stroke="#8ca8a0" stroke-width="1.5"/>')
    for r in p['rooms']:
        poly=r['polygon'];cx,cz=label_anchor(r,p['objects'],scale)
        label=r['name'];area=polygon_area(poly)
        out.append(f'<g font-family="Arial,sans-serif" text-anchor="middle"><rect x="{X(cx)-min(110,len(label)*4.1)}" y="{Y(cz)-26}" width="{min(220,len(label)*8.2)}" height="39" rx="5" fill="#faf9f3" fill-opacity=".87"/><text x="{X(cx)}" y="{Y(cz)-10}" font-size="12" font-weight="600" fill="#344d3f">{esc(label)}</text><text x="{X(cx)}" y="{Y(cz)+5}" font-size="10" fill="#738071">{area:.1f} м²</text></g>')
    out.extend([f'<path d="M{X(x0)} {Y(z1)+35}H{X(x1)}M{X(x0)} {Y(z1)+29}v12M{X(x1)} {Y(z1)+29}v12" stroke="#8c9a8b" fill="none"/>',f'<text x="{(X(x0)+X(x1))/2}" y="{Y(z1)+54}" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#5d7263">{width:.2f} м</text>',f'<path d="M60 {H-58}h{scale:.1f}" stroke="#476653" stroke-width="3"/><text x="60" y="{H-68}" font-family="Arial,sans-serif" font-size="11" fill="#607664">1 метр</text>',f'<text x="{W-60}" y="{H-42}" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#7b867b">Концепция интерьера · Размеры требуют проверки на объекте</text>','</svg>'])
    return '\n'.join(out).encode('utf-8')
