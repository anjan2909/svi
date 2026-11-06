"""Close-up illustrations of the components that go inside SVI panels (240x180, transparent)."""
from svgkit import *

W, H = 240, 180


def base(title_shadow_w=150):
    s = Svg(W, H)
    s.add(ellipse(W / 2, 160, title_shadow_w / 2, 7, '#000', opacity=.45, filter=s.blur(5)))
    return s


def din_rail(s, x, y, w):
    return [rect(x, y, w, 12, s.lgrad([(0, '#d7dde1'), (.5, '#9aa5ad'), (1, '#c4cbd1')])),
            [rect(x + 6 + i * 16, y + 4, 9, 4, '#6f7a83', rx=2) for i in range(int((w - 8) // 16))]]


def air_breaker():
    s = base(170)
    x, y, w, h = 52, 26, 136, 126
    s.add(rect(x - 12, y + 8, 12, h - 8, '#8f9aa3', stroke=EDGE), rect(x + w, y + 8, 12, h - 8, '#8f9aa3', stroke=EDGE))
    s.add([rect(x - 9, y + 20 + i * 30, 6, 14, '#5b6670', rx=1) for i in range(4)], [rect(x + w + 3, y + 20 + i * 30, 6, 14, '#5b6670', rx=1) for i in range(4)])
    s.add(rect(x - 3, y - 3, w + 6, h + 6, '#6d7881', rx=4))
    s.add(acb(x, y, w, h))
    s.add(rect(x + 4, y + 4, w - 8, h * .2, '#4b555e', rx=1), rect(x + 8, y + 7, w * .45, h * .07, '#e9edf0'), rect(x + w - 40, y + 7, 30, h * .07, AMBER, opacity=.9))
    s.add(rect(x + w * .44, y + h * .64, w * .12, h * .3, '#8b959d', rx=2), circle(x + w / 2, y + h * .9, 4, '#20272d'))
    s.add(rect(x, y, w, h, 'none', stroke='#8b959d', stroke_width=1.2, rx=2))
    return s.render('Air circuit breaker illustration')


def moulded_breaker():
    s = base(110)
    x, y, w, h = 78, 14, 84, 140
    g = s.lgrad([(0, '#2b333a'), (.5, '#1d2329'), (1, '#14181c')], 0, 0, 1, 0)
    s.add(rect(x, y, w, h, g, rx=4))
    for ty in (y + 4, y + h - 22):
        s.add(rect(x + 6, ty, w - 12, 18, '#2f383f', rx=2), [rect(x + 12 + i * 22, ty + 4, 14, 10, '#0b0e11', rx=1.5) for i in range(3)])
        s.add([circle(x + 19 + i * 22, ty + 9, 2.2, '#9aa5ad') for i in range(3)])
    s.add(rect(x + 30, y + 46, 24, 50, '#0d1115', rx=3), rect(x + 32, y + 48, 20, 22, '#d6dbdf', rx=2))
    s.add(rect(x + 8, y + 30, 22, 9, '#eceff1', opacity=.85), rect(x + 58, y + 30, 18, 9, RED, opacity=.9))
    s.add(circle(x + 67, y + 108, 7, '#3a434b'), line(x + 67, y + 108, x + 71, y + 103, '#eceff1', 1.4))
    s.add(rect(x + 8, y + 102, 30, 3, '#59636b'), rect(x + 8, y + 108, 22, 3, '#59636b'))
    return s.render('Moulded case circuit breaker illustration')


def miniature_breakers():
    s = base(170)
    s.add(din_rail(s, 30, 88, 180))
    for i in range(4):
        x = 38 + i * 26
        s.add(rect(x, 44, 24, 98, '#eef0f1', stroke='#9aa3aa', stroke_width=.8, rx=2), rect(x + 3, 50, 18, 10, '#d4d9dc'))
        s.add(rect(x + 8, 78, 8, 22, '#1d2329', rx=1.5), rect(x + 4, 114, 16, 6, '#c9ced2'), rect(x + 6, 126, 12, 3, GREEN if i < 3 else RED))
    x = 148
    s.add(rect(x, 44, 50, 98, '#eef0f1', stroke='#9aa3aa', stroke_width=.8, rx=2), rect(x + 4, 50, 42, 10, '#d4d9dc'))
    s.add(rect(x + 10, 78, 10, 22, '#1d2329', rx=1.5), rect(x + 30, 78, 10, 22, '#1d2329', rx=1.5), circle(x + 25, 116, 5, YELLOW, stroke='#9a7d1e'))
    s.add(rect(x + 8, 128, 34, 4, '#3b82f6', opacity=.8))
    return s.render('Miniature circuit breakers and RCCB on a DIN rail illustration')


def contactor_relay():
    s = base(130)
    x, y, w = 82, 14, 76
    s.add(rect(x, y, w, 88, '#e3e6e8', stroke='#8b959d', rx=3), rect(x, y, w, 16, '#cfd4d7', rx=3))
    s.add([circle(x + 14 + i * 24, y + 8, 4, '#9aa3aa', stroke='#6f7a83') for i in range(3)])
    s.add(rect(x + 14, y + 28, 48, 34, '#3a434b', rx=2), rect(x + 30, y + 34, 16, 22, '#d4d9dc', rx=1.5))
    s.add(rect(x + 8, y + 70, 30, 8, '#eceff1', stroke='#9aa3aa', stroke_width=.5))
    s.add(rect(x - 2, y + 92, w + 4, 52, '#d7dbde', stroke='#8b959d', rx=3))
    s.add(circle(x + 18, y + 116, 9, '#c94f3d'), circle(x + 18, y + 116, 6, '#e8edf0'), line(x + 18, y + 116, x + 22, y + 111, '#333', 1.4))
    s.add(circle(x + 46, y + 108, 6, '#2f6fd6'), rect(x + 58, y + 104, 12, 8, '#1d2329', rx=1.5))
    s.add([circle(x + 14 + i * 24, y + 138, 3.5, '#9aa3aa', stroke='#6f7a83') for i in range(3)])
    return s.render('Contactor with overload relay illustration')


def protection_relay():
    s = base(140)
    x, y, w, h = 64, 16, 112, 138
    s.add(rect(x, y, w, h, '#3b444c', rx=4), rect(x + 4, y + 4, w - 8, h - 8, '#2a3138', rx=3))
    s.add(rect(x + 14, y + 16, 62, 34, '#0b1712', rx=2))
    s.add([rect(x + 19, y + 22 + i * 9, 40 - i * 10, 4, '#48e08a', opacity=.9) for i in range(3)])
    s.add(rect(x + 14, y + 16, 62, 34, '#48e08a', opacity=.15, filter=s.blur(2)))
    for i, c in enumerate((GREEN, RED, AMBER, RED, '#55606a')):
        s.add(lamp(s, x + 92, y + 22 + i * 13, c, 2.6, glow=c != '#55606a'))
    cx, cy = x + 44, y + 92
    s.add(rect(cx - 7, cy - 22, 14, 12, '#4a535b', rx=2), rect(cx - 7, cy + 10, 14, 12, '#4a535b', rx=2),
          rect(cx - 25, cy - 6, 14, 12, '#4a535b', rx=2), rect(cx + 11, cy - 6, 14, 12, '#4a535b', rx=2), rect(cx - 7, cy - 6, 14, 12, AMBER, rx=2))
    s.add(rect(x + 82, y + 86, 18, 12, '#4a535b', rx=2), rect(x + 82, y + 104, 18, 12, '#4a535b', rx=2))
    s.add(rect(x + 14, y + 122, 50, 4, '#59636b'))
    return s.render('Numerical protection relay illustration')


def plc_hmi():
    s = base(180)
    s.add(rect(28, 22, 104, 76, '#20272d', rx=4), rect(34, 28, 92, 60, '#0e2233'))
    s.add(rect(34, 28, 92, 10, AMBER, opacity=.9))
    for i, hgt in enumerate((20, 30, 16, 36, 26)):
        s.add(rect(40 + i * 17, 84 - hgt, 10, hgt, '#48e08a' if i != 3 else AMBER, opacity=.85))
    s.add(rect(34, 28, 92, 60, '#5ab4ff', opacity=.12, filter=s.blur(2)))
    s.add(din_rail(s, 40, 128, 176))
    s.add(plc_rack(64, 104, n=8, h=44))
    s.add(rect(150, 40, 58, 22, '#2b333a', rx=3), button(164, 51, GREEN, 4), button(180, 51, RED, 4), selector(196, 51, 4))
    s.add(rect(42, 106, 18, 34, '#c9ced2', stroke='#8b959d', stroke_width=.6, rx=1.5), [rect(45, 111 + i * 4, 12, 1.4, '#8b959d') for i in range(5)], circle(51, 133, 1.6, GREEN))
    return s.render('PLC and HMI touchscreen illustration')


def meters():
    s = base(170)
    x, y = 30, 36
    s.add(rect(x, y, 96, 96, '#3b444c', rx=3), rect(x + 4, y + 4, 88, 88, '#20272d', rx=2), rect(x + 10, y + 10, 76, 52, '#0b1712'))
    for row in range(3):
        ry = y + 15 + row * 15
        s.add(rect(x + 14, ry + 3, 10, 5, '#2e6b4a'))
        s.add([rect(x + 32 + k * 12, ry, 9, 11, '#48e08a', opacity=.92, rx=1) for k in range(4)])
    s.add(rect(x + 10, y + 10, 76, 52, '#48e08a', opacity=.14, filter=s.blur(2), class_='lg'))
    s.add([rect(x + 12 + k * 19, y + 72, 15, 10, '#4a535b', rx=2) for k in range(4)])
    s.add(meter_analog(144, 48, 72))
    return s.render('Multifunction meter and analog ammeter illustration')


def busbars():
    s = base(190)
    for i, (c, yy) in enumerate(((RED, 46), (YELLOW, 76), (BLUE, 106))):
        s.add(busbar(s, 22, yy, 196, 14))
        s.add(rect(22, yy, 18, 14, c, rx=1.5), rect(200, yy, 18, 14, c, rx=1.5))
        s.add([circle(110 + k * 14, yy + 7, 2.6, '#6b3d1e') for k in range(2)])
    s.add(rect(22, 136, 196, 9, '#2a3138', rx=1.5))
    for ix in (60, 168):
        s.add(rect(ix, 38, 16, 112, '#7d2b22', rx=3), rect(ix + 2, 40, 4, 108, '#a8443a', opacity=.6))
    s.add(rect(102, 70, 30, 26, s.lgrad(COPPER, 0, 0, 1, 0), rx=1.5, opacity=.9))
    return s.render('Copper busbars on insulator supports illustration')


COMPONENTS = {
    'part-acb.svg': air_breaker, 'part-mccb.svg': moulded_breaker, 'part-mcb.svg': miniature_breakers,
    'part-contactor.svg': contactor_relay, 'part-relay.svg': protection_relay, 'part-plc.svg': plc_hmi,
    'part-meter.svg': meters, 'part-busbar.svg': busbars,
}
