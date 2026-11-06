"""Tiny SVG drawing kit shared by the SVI illustrations (no dependencies)."""
import math

# ---------- palette ----------
STEEL, STEEL_L, STEEL_D, EDGE = '#c4cbd1', '#dbe0e4', '#a5afb7', '#55626d'
SIDE, TOP, PLINTH = '#8994a0', '#e1e6e9', '#1b2833'
INSIDE, PLATE = '#2c3a46', '#b7c0c7'
BLACK, DARK = '#1d2329', '#2a3138'
AMBER, RED, GREEN, BLUE, YELLOW = '#ffb000', '#e5484d', '#2fbf71', '#3b82f6', '#f2c94c'
COPPER = [(0, '#9c5226'), (0.45, '#eaa36b'), (1, '#a95c2b')]
SKIN, SKIN_D, HAIR = '#b97b55', '#985f40', '#1c1613'
COVER, COVER_D = '#45739a', '#2f5677'
STRIPE, BOOT = '#e8eef2', '#3b2e25'
HELMET_W, HELMET_Y = '#eef2f4', '#ffc93c'


def r(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


def attrs(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        k = k.rstrip('_').replace('_', '-')
        out.append(f'{k}="{r(v) if isinstance(v, (int, float)) else v}"')
    return ' '.join(out)


def rect(x, y, w, h, fill='none', **kw):
    return f'<rect {attrs(x=x, y=y, width=w, height=h, fill=fill, **kw)}/>'


def circle(cx, cy, rad, fill='none', **kw):
    return f'<circle {attrs(cx=cx, cy=cy, r=rad, fill=fill, **kw)}/>'


def ellipse(cx, cy, rx, ry, fill='none', **kw):
    return f'<ellipse {attrs(cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, **kw)}/>'


def line(x1, y1, x2, y2, stroke, sw=1, **kw):
    return f'<line {attrs(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=sw, **kw)}/>'


def path(d, fill='none', **kw):
    return f'<path {attrs(d=d, fill=fill, **kw)}/>'


def poly(points, fill='none', **kw):
    pts = ' '.join(f'{r(float(x))},{r(float(y))}' for x, y in points)
    return f'<polygon {attrs(points=pts, fill=fill, **kw)}/>'


def polyline(points, stroke, sw=1, **kw):
    pts = ' '.join(f'{r(float(x))},{r(float(y))}' for x, y in points)
    return f'<polyline {attrs(points=pts, fill="none", stroke=stroke, stroke_width=sw, stroke_linecap="round", stroke_linejoin="round", **kw)}/>'


def group(items, **kw):
    return f'<g {attrs(**kw)}>' + ''.join(flat(items)) + '</g>'


def flat(items):
    for it in items:
        if isinstance(it, (list, tuple)):
            yield from flat(it)
        elif it:
            yield it


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


class Svg:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.defs, self.body, self._n, self._blur = [], [], 0, {}

    def uid(self, p='i'):
        self._n += 1
        return f'{p}{self._n}'

    def add(self, *items):
        self.body.extend(flat(items))

    def lgrad(self, stops, x1=0, y1=0, x2=0, y2=1):
        gid = self.uid('lg')
        st = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{s[0]}"' if s else '') + '/>' for o, c, *s in stops)
        self.defs.append(f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return f'url(#{gid})'

    def rgrad(self, stops, cx=.5, cy=.5, rad=.5):
        gid = self.uid('rg')
        st = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{s[0]}"' if s else '') + '/>' for o, c, *s in stops)
        self.defs.append(f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{rad}">{st}</radialGradient>')
        return f'url(#{gid})'

    def blur(self, sd):
        if sd not in self._blur:
            fid = self.uid('bl')
            self.defs.append(f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
            self._blur[sd] = f'url(#{fid})'
        return self._blur[sd]

    def render(self, title):
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
             f'width="{self.w}" height="{self.h}" role="img"><title>{title}</title>')
        if self.defs:
            s += '<defs>' + ''.join(self.defs) + '</defs>'
        s += ('<style>.lg{animation:lp 3s ease-in-out infinite}@keyframes lp{0%,100%{opacity:.3}50%{opacity:.8}}'
              '.fl{animation:fl .7s ease-in-out infinite alternate}@keyframes fl{from{opacity:.78}to{opacity:1}}'
              '.dr{animation:dr 3.6s ease-in-out infinite alternate}@keyframes dr{to{transform:translate(-7px,-3px)}}'
              '@media (prefers-reduced-motion:reduce){.lg,.fl,.dr{animation:none}}</style>')
        return s + ''.join(self.body) + '</svg>'


# ---------- panel parts ----------
def cabinet(s, x, y, w, h, depth=14, plinth=11, shadow=True):
    dx, dy = depth, depth * .55
    out = []
    if shadow:
        out.append(ellipse(x + w / 2 + dx / 2, y + h + plinth + 2, w * .62, 9, '#000', opacity=.5, filter=s.blur(5)))
    side = s.lgrad([(0, '#9aa5ae'), (1, '#77838d')], 0, 0, 1, 0)
    out.append(poly([(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)], side, stroke=EDGE, stroke_width=1))
    out.append(poly([(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w, y)], TOP, stroke=EDGE, stroke_width=1))
    out.append(rect(x, y + h, w, plinth, PLINTH))
    out.append(poly([(x + w, y + h), (x + w + dx, y + h - dy), (x + w + dx, y + h + plinth - dy), (x + w, y + h + plinth)], '#111b24'))
    out.append(rect(x, y, w, h, STEEL, stroke=EDGE, stroke_width=1.2))
    return out


def door(s, x, y, w, h, handle='right', lock=True):
    g = s.lgrad([(0, STEEL_L), (1, STEEL)])
    out = [rect(x, y, w, h, g, stroke=EDGE, stroke_width=1),
           rect(x + 2.4, y + 2.4, w - 4.8, h - 4.8, 'none', stroke='#eef2f4', stroke_width=.7, opacity=.7)]
    if handle:
        hh = min(15, h * .38)
        hx = x + w - 6.5 if handle == 'right' else x + 3.5
        out.append(rect(hx, y + h / 2 - hh / 2, 3, hh, DARK, rx=1.2))
        if lock and h > 40:
            out.append(circle(hx + 1.5, y + h / 2 + hh / 2 + 5, 1.6, DARK))
    return out


def louvers(x, y, w, n=3, gap=4.5, col='#6c7882'):
    return [rect(x, y + i * gap, w, 1.7, col, rx=.8) for i in range(n)]


def lamp(s, x, y, col, rad=3.6, glow=True):
    out = []
    if glow:
        delay = -((int(x) * 7 + int(y) * 13) % 30) / 10
        out.append(circle(x, y, rad * 2.3, col, opacity=.55, filter=s.blur(2.6), class_='lg', style=f'animation-delay:{delay}s'))
    out += [circle(x, y, rad + 1.5, DARK), circle(x, y, rad, col),
            circle(x - rad * .35, y - rad * .35, rad * .35, '#fff', opacity=.55)]
    return out


def button(x, y, col, rad=3.4):
    return [circle(x, y, rad + 1.6, DARK), circle(x, y, rad, col), circle(x - rad * .3, y - rad * .35, rad * .3, '#fff', opacity=.45)]


def meter_digital(s, x, y, w, h, col='#48e08a'):
    out = [rect(x, y, w, h, '#20272d', rx=1.5), rect(x + 3, y + 3, w - 6, h * .55, '#0b1712')]
    sh = h * .55 - 6
    for i, frac in enumerate((.72, .55, .64)):
        ly = y + 6 + i * (sh / 3)
        out.append(rect(x + 6, ly, (w - 12) * frac, max(1.4, sh / 3 - 2.2), col, opacity=.9))
    out.append(rect(x + 3, y + 3, w - 6, h * .55, col, opacity=.18, filter=s.blur(2)))
    for i in range(4):
        out.append(rect(x + 5 + i * (w - 10) / 4, y + h * .72, (w - 10) / 4 - 3, h * .16, '#3a434b', rx=.8))
    return out


def meter_analog(x, y, size):
    cx, cy = x + size / 2, y + size * .62
    rad = size * .38
    out = [rect(x, y, size, size, DARK, rx=1.2), rect(x + 2, y + 2, size - 4, size - 4, '#f2f0ea')]
    for i in range(7):
        a = math.radians(210 + i * 20)
        out.append(line(cx + math.cos(a) * rad * .8, cy + math.sin(a) * rad * .8, cx + math.cos(a) * rad, cy + math.sin(a) * rad, '#333', .7))
    a = math.radians(262)
    out.append(line(cx, cy, cx + math.cos(a) * rad * .95, cy + math.sin(a) * rad * .95, RED, .9))
    return out


def mccb(x, y, w, h, on=True):
    out = [rect(x, y, w, h, BLACK, rx=1.5), rect(x + w * .39, y + h * .2, w * .22, h * .6, '#0d1115', rx=1)]
    ty = y + h * .22 if on else y + h * .48
    out.append(rect(x + w * .4, ty, w * .2, h * .3, '#d6dbdf', rx=1))
    out.append(rect(x + w * .08, y + h * .14, w * .2, h * .1, '#eaeef0', opacity=.8))
    return out


def door_cutout(x, y, w, h):
    return rect(x - 2, y - 2, w + 4, h + 4, '#2b333a', rx=1.5)


def acb(x, y, w, h):
    out = [rect(x, y, w, h, BLACK, rx=2), rect(x + 4, y + 4, w - 8, h * .2, '#3a434b', rx=1),
           rect(x + 8, y + 6, w * .35, h * .08, '#e9edf0', opacity=.8),
           rect(x + 8, y + h * .38, w * .17, h * .14, GREEN, rx=1), rect(x + 8 + w * .21, y + h * .38, w * .17, h * .14, RED, rx=1),
           rect(x + w * .66, y + h * .36, w * .2, h * .08, '#f5f5f5'), rect(x + w * .66, y + h * .48, w * .2, h * .08, YELLOW),
           rect(x + w * .44, y + h * .64, w * .12, h * .3, '#59636b', rx=1.5), rect(x + 8, y + h * .72, w * .26, h * .05, '#59636b'),
           rect(x + w - 8 - w * .2, y + h * .72, w * .2, h * .05, '#59636b')]
    return out


def nameplate(x, y, w, h=6):
    return [rect(x, y, w, h, '#eceff1', stroke='#7a8690', stroke_width=.5), rect(x + 2, y + h / 2 - .5, w * .55, 1, '#56626c')]


def danger_sign(x, y, size=12):
    pts = [(x + size / 2, y), (x + size, y + size * .88), (x, y + size * .88)]
    bolt = [(x + size * .56, y + size * .26), (x + size * .38, y + size * .56), (x + size * .52, y + size * .56), (x + size * .44, y + size * .8),
            (x + size * .64, y + size * .46), (x + size * .5, y + size * .46)]
    return [poly(pts, YELLOW, stroke=BLACK, stroke_width=.9, stroke_linejoin='round'), poly(bolt, BLACK)]


def selector(x, y, rad=4):
    return [circle(x, y, rad + 1.5, '#3b444c'), circle(x, y, rad, BLACK), rect(x - 1, y - rad + .8, 2, rad * 1.6, '#d6dbdf', rx=1, transform=f'rotate(35 {r(float(x))} {r(float(y))})')]


def capacitor(s, x, y, w, h):
    g = s.lgrad([(0, '#7d93a6'), (.4, '#dce5ec'), (1, '#6f8598')], 0, 0, 1, 0)
    return [rect(x, y + w * .18, w, h - w * .18, g), ellipse(x + w / 2, y + h, w / 2, w * .18, '#6f8598'),
            ellipse(x + w / 2, y + w * .18, w / 2, w * .18, '#c9d4dd', stroke='#7d93a6', stroke_width=.6),
            circle(x + w * .3, y + w * .16, 1.6, '#a85b2b'), circle(x + w * .7, y + w * .16, 1.6, '#a85b2b')]


def contactor(x, y, w=14, h=16):
    return [rect(x, y, w, h, '#d9dde0', stroke='#8b959d', stroke_width=.6, rx=1), rect(x + 2, y + 2, w - 4, h * .28, '#4a535b'),
            rect(x + w * .3, y + h * .52, w * .4, h * .22, '#9aa3aa')]


def duct(x, y, w, h, horizontal=True):
    out = [rect(x, y, w, h, '#8f9aa3', stroke='#77828b', stroke_width=.6)]
    if horizontal:
        for i in range(int(w // 5)):
            out.append(rect(x + 2 + i * 5, y + 1.2, 1.6, h - 2.4, '#6f7a83'))
    else:
        for i in range(int(h // 5)):
            out.append(rect(x + 1.2, y + 2 + i * 5, w - 2.4, 1.6, '#6f7a83'))
    return out


def terminals(x, y, n, w=3.2, h=12):
    cols = ['#9aa3aa', '#9aa3aa', '#3b82f6', '#9aa3aa', '#c9d23a']
    return [rect(x + i * (w + .6), y, w, h, cols[i % len(cols)], stroke='#55606a', stroke_width=.3) for i in range(n)]


def mcb_row(x, y, n, w=6, h=16):
    out = []
    for i in range(n):
        bx = x + i * (w + .5)
        out += [rect(bx, y, w, h, '#eef0f1', stroke='#9aa3aa', stroke_width=.4), rect(bx + w * .3, y + h * .3, w * .4, h * .3, BLACK)]
    return out


def plc_rack(x, y, n=6, h=28):
    out = [rect(x, y, 22, h, '#3b444c', rx=1), rect(x + 3, y + 4, 16, 6, '#1a1f24'), circle(x + 6, y + 14, 1.2, GREEN), circle(x + 10, y + 14, 1.2, AMBER)]
    for i in range(n):
        mx = x + 24 + i * 9
        out += [rect(mx, y, 8, h, '#4a535b', rx=.8), rect(mx + 1, y + 3, 6, 3, '#1a1f24')]
        for j in range(4):
            out.append(circle(mx + 2.5 + (j % 2) * 3, y + 9 + (j // 2) * 3, .8, GREEN if (i + j) % 3 else AMBER))
    return out


def busbar(s, x, y, w, h, vertical=False):
    g = s.lgrad(COPPER, 0, 0, 1, 0) if vertical else s.lgrad(COPPER)
    return [rect(x, y, w, h, g, rx=1)]


# ---------- people ----------
def limb(points, col, width):
    d = 'M' + ' L'.join(f'{r(float(px))} {r(float(py))}' for px, py in points)
    return path(d, stroke=col, stroke_width=width, stroke_linecap='round', stroke_linejoin='round')


def boot(ankle, facing, col=BOOT):
    ax, ay = ankle
    x = ax - 5 if facing > 0 else ax - 13
    return rect(x, ay - 3, 18, 9.5, col, rx=3.5)


def person(P, facing=1, helmet=HELMET_W, vest=True, suit=(COVER, COVER_D), headwear='helmet', mask=None):
    """P: head, torso(4 pts: back-shoulder, front-shoulder, front-hip, back-hip),
    sh, sh2, hip, hip2, arm_f, arm_b (elbow, hand), leg_f, leg_b (knee, ankle)."""
    front, back = suit
    hx, hy = P['head']
    hr = P.get('hr', 12)
    out = []
    out.append(limb([P['hip2'], *P['leg_b']], back, 13))
    out.append(boot(P['leg_b'][-1], facing, '#2c221b'))
    out.append(limb([P['sh2'], *P['arm_b']], back, 9.5))
    out.append(circle(*P['arm_b'][-1], 4.6, SKIN_D))
    t = P['torso']
    out.append(poly(t, front, stroke_linejoin='round'))
    if vest:
        v = [lerp(t[0], t[3], .04), lerp(t[1], t[2], .04), lerp(t[2], t[1], .14), lerp(t[3], t[0], .14)]
        out.append(poly(v, AMBER))
        for f in (.48, .7):
            a, b = lerp(v[0], v[3], f), lerp(v[1], v[2], f)
            out.append(line(a[0], a[1], b[0], b[1], STRIPE, 3.2))
        out.append(line(*lerp(v[0], v[1], .5), *lerp(v[3], v[2], .5), '#d99600', .8))
    out.append(limb([P['hip'], *P['leg_f']], front, 13.5))
    out.append(boot(P['leg_f'][-1], facing))
    nx, ny = P.get('neck', (hx - 2 * facing, hy + hr - 1))
    out.append(rect(nx - 4, ny - 2, 8, 9, SKIN_D, rx=2))
    out.append(circle(hx, hy, hr, SKIN))
    out.append(path(f'M{hx - hr * facing} {hy - 2} q{hr * .1 * facing} {-hr * .9} {hr * .9 * facing} {-hr * .95} l0 {hr * .5} q{-hr * .5 * facing} {hr * .1} {-hr * .7 * facing} {hr * 1.1}z', HAIR))
    out.append(circle(hx - hr * .25 * facing, hy + 1, 2.2, SKIN_D))  # ear
    if mask == 'weld':
        out.append(path(f'M{hx + hr * .1 * facing} {hy - hr * 1.1} L{hx + hr * 1.35 * facing} {hy - hr * .7} L{hx + hr * 1.3 * facing} {hy + hr * 1.05} L{hx + hr * .2 * facing} {hy + hr * 1.15}z', '#2b3239', stroke='#14191d', stroke_width=1))
        out.append(rect(min(hx + hr * .55 * facing, hx + hr * 1.15 * facing), hy - hr * .35, hr * .55, hr * .32, '#1e8a63', opacity=.9))
    if mask == 'resp':
        out.append(path(f'M{hx + hr * .35 * facing} {hy + hr * .1} q{hr * .8 * facing} 0 {hr * .75 * facing} {hr * .55} q{-hr * .1 * facing} {hr * .45} {-hr * .6 * facing} {hr * .4}z', '#d6dbdf', stroke='#7b868f', stroke_width=.8))
        out.append(circle(hx + hr * .95 * facing, hy + hr * .6, hr * .28, '#c94f3d'))
        out.append(path(f'M{hx + hr * .4 * facing} {hy - hr * .55} l{hr * .65 * facing} 0 l0 {hr * .4} l{-hr * .7 * facing} 0z', '#9fd2e8', opacity=.85))
    if headwear == 'helmet':
        out.append(path(f'M{hx - hr * 1.05} {hy - 1} a{hr * 1.05} {hr * 1.05} 0 0 1 {hr * 2.1} 0z', helmet, transform=f'translate(0 -2)'))
        bx = hx - hr * 1.1 if facing > 0 else hx - hr * 1.6
        out.append(rect(bx, hy - 4, hr * 2.7, 3.2, helmet, rx=1.5))
        out.append(rect(hx - 1.4, hy - hr - 1.5, 2.8, hr * .9, '#ffffff', opacity=.5, rx=1.2))
    elif headwear == 'hood':
        out.append(path(f'M{hx - hr * 1.15} {hy + hr * .4} a{hr * 1.15} {hr * 1.2} 0 0 1 {hr * 2.3} 0 l{-hr * .25 * facing} {-hr * .25} a{hr * .9} {hr * .95} 0 0 0 {-hr * 1.8} 0z', front))
    out.append(limb([P['sh'], *P['arm_f']], front, 10))
    out.append(circle(*P['arm_f'][-1], 4.9, SKIN))
    return out


def standing(fx, gy, facing=1, arm_f=None, arm_b=None, lean=0, crouch=0):
    """Generic standing pose; feet at x=fx on ground y=gy. Arms as (elbow, hand) offsets from shoulder."""
    f = facing
    top = gy - 186 + crouch
    head = (fx + (4 + lean) * f, top + 12)
    sh = (fx + (5 + lean * .8) * f, top + 38)
    sh2 = (fx + (-7 + lean * .8) * f, top + 39)
    hip = (fx + 5 * f, top + 100 + crouch * .2)
    hip2 = (fx - 6 * f, top + 100 + crouch * .2)
    torso = [(fx + (-13 + lean * .8) * f, top + 33), (fx + (13 + lean * .8) * f, top + 32), (fx + 12 * f, top + 104 + crouch * .2), (fx - 12 * f, top + 104 + crouch * .2)]
    kd = crouch * .5
    leg_f = [(fx + (9 + kd) * f, gy - 44 - crouch * .1), (fx + 8 * f, gy - 4)]
    leg_b = [(fx + (-6 + kd * .6) * f, gy - 44 - crouch * .1), (fx - 10 * f, gy - 4)]

    def arm(spec, s):
        if spec is None:
            return [(s[0] + 2 * f, s[1] + 34), (s[0] + 4 * f, s[1] + 62)]
        (ex, ey), (hx_, hy_) = spec
        return [(s[0] + ex * f, s[1] + ey), (s[0] + hx_ * f, s[1] + hy_)]
    return dict(head=head, torso=torso, sh=sh, sh2=sh2, hip=hip, hip2=hip2,
                leg_f=leg_f, leg_b=leg_b, arm_f=arm(arm_f, sh), arm_b=arm(arm_b, sh2), neck=(head[0] - 2 * f, head[1] + 11))


# ---------- scene background ----------
def scene_bg(s, floor_y, lights=(.25, .7), wall=('#17324b', '#0f2337')):
    W, H = s.w, s.h
    out = [rect(0, 0, W, floor_y, s.lgrad([(0, wall[0]), (1, wall[1])]))]
    for x in range(0, W + 1, 24):
        out.append(line(x, 0, x, floor_y, '#fff', .5, opacity=.04))
    for y in range(0, floor_y, 24):
        out.append(line(0, y, W, y, '#fff', .5, opacity=.04))
    cone = s.lgrad([(0, '#fff6dc', .16), (1, '#fff6dc', 0)])
    for f in lights:
        lx = W * f
        out.append(poly([(lx - 30, 14), (lx + 30, 14), (lx + 120, floor_y + 40), (lx - 120, floor_y + 40)], cone))
        out.append(rect(lx - 34, 9, 68, 5, '#fff3cf', rx=2.5))
        out.append(rect(lx - 34, 9, 68, 5, '#fff3cf', rx=2.5, filter=s.blur(4), opacity=.9))
    out.append(rect(0, floor_y, W, H - floor_y, s.lgrad([(0, '#102233'), (1, '#08131c')])))
    out.append(line(0, floor_y, W, floor_y, '#2c4a62', 1.4))
    out.append(line(0, floor_y + (H - floor_y) * .62, W, floor_y + (H - floor_y) * .62, AMBER, 3, opacity=.3, stroke_dasharray='18 12'))
    return out


def ik(shoulder, hand, l1=34, l2=33, bend=1):
    """Elbow position for an arm reaching from shoulder to hand (2-bone IK)."""
    sx, sy = shoulder
    hx, hy = hand
    dx, dy = hx - sx, hy - sy
    d = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - .5))
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    hgt = math.sqrt(max(0, l1 * l1 - a * a))
    ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
    bx, by = sx + a * ux, sy + a * uy
    return (bx - uy * hgt * bend, by + ux * hgt * bend)


def reach(P, which, hand, bend=1):
    sh = P['sh'] if which == 'f' else P['sh2']
    if math.hypot(hand[0] - sh[0], hand[1] - sh[1]) > 66:
        print(f'  warning: {which} hand {hand} is out of reach from shoulder {tuple(round(v) for v in sh)}')
    P['arm_' + which] = [ik(sh, hand, bend=bend), hand]
    return P


def glow_burst(s, x, y, rad=48, col=AMBER, seed=3):
    import random
    rnd = random.Random(seed)
    out = [circle(x, y, rad, s.rgrad([(0, '#fff', .95), (.18, col, .7), (1, col, 0)]))]
    for _ in range(18):
        a = rnd.uniform(-math.pi, .2)
        l1, l2 = rnd.uniform(6, 12), rnd.uniform(16, 34)
        out.append(line(x + math.cos(a) * l1, y + math.sin(a) * l1, x + math.cos(a) * l2, y + math.sin(a) * l2,
                        rnd.choice(['#fff7d6', AMBER, '#ffd77a']), rnd.uniform(.8, 1.6), stroke_linecap='round'))
    for _ in range(14):
        a = rnd.uniform(0, math.pi)
        d = rnd.uniform(10, 40)
        out.append(circle(x + math.cos(a) * d, y + math.sin(a) * d * .7 + 6, rnd.uniform(.8, 1.6), '#ffd77a'))
    out.append(circle(x, y, 4, '#fff'))
    return [group(out, class_='fl')]
