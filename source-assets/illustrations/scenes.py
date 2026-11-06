"""Workshop and technician scenes (480x320, own dark background)."""
import math
import random
from svgkit import *

FLOOR = 236
GY = 298  # where people stand


def press_brake():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.3, .78)))
    body, face, edge = '#2f4d68', '#3e6386', '#1f354a'
    s.add(ellipse(286, 276, 170, 8, '#000', opacity=.5, filter=s.blur(5)))
    # columns, beams
    s.add(rect(150, 34, 38, 240, body, stroke=edge), rect(384, 34, 38, 240, body, stroke=edge))
    s.add(rect(150, 34, 272, 42, face, stroke=edge), rect(150, 40, 272, 5, AMBER, opacity=.85))
    s.add(rect(178, 76, 216, 48, s.lgrad([(0, '#4d78a0'), (1, '#3b6184')]), stroke=edge))
    s.add([rect(178, 118 - i * 4, 216, 1, '#6d93b5', opacity=.4) for i in range(2)])
    s.add(rect(186, 124, 200, 8, '#26323c'))
    s.add(poly([(188, 132), (384, 132), (384, 139), (381, 146), (191, 146), (188, 139)], '#a3aeb6', stroke='#6c7882', stroke_width=.8))
    s.add(rect(186, 168, 200, 12, '#a3aeb6', stroke='#6c7882', stroke_width=.8), rect(178, 180, 216, 8, '#26323c'))
    s.add(rect(178, 188, 216, 86, face, stroke=edge))
    s.add([poly([(178 + i * 24, 188), (190 + i * 24, 188), (178 + i * 24 + 6, 194), (172 + i * 24 - 6 + 6, 194)], BLACK) for i in range(0)])
    s.add(rect(178, 188, 216, 6, s.lgrad([(0, AMBER), (1, AMBER)]), opacity=.9))
    s.add([poly([(182 + i * 18, 188), (190 + i * 18, 188), (184 + i * 18, 194), (176 + i * 18, 194)], BLACK) for i in range(12)])
    s.add(rect(196, 206, 70, 40, '#355a7c', stroke=edge, rx=2), rect(306, 206, 70, 40, '#355a7c', stroke=edge, rx=2))
    # light curtains
    for lx in (192, 376):
        s.add(rect(lx - 3, 78, 6, 110, '#d8dde1', rx=2), [circle(lx, 86 + i * 12, 1.3, RED) for i in range(9)])
    # sheet in the tools
    s.add(poly([(194, 150), (378, 150), (402, 176), (170, 176)], s.lgrad([(0, '#e5eaee'), (1, '#9aa5ad')]), stroke='#6f7a83', stroke_width=.8))
    s.add(line(190, 156, 382, 156, '#ffffff', .8, opacity=.6))
    # control pendant
    s.add(polyline([(420, 50), (452, 50), (452, 92)], '#55626d', 4))
    s.add(rect(430, 92, 42, 58, '#d9dde0', stroke='#7b868f', rx=3), rect(435, 97, 32, 22, '#0e2233'))
    s.add([rect(438, 101 + i * 5, 22 - i * 5, 2, '#5ab4ff', opacity=.8) for i in range(3)])
    s.add(button(441, 132, GREEN, 3), button(461, 132, RED, 3))
    # foot pedal and sheet stack
    s.add(rect(300, 280, 34, 14, YELLOW, rx=2), rect(304, 283, 26, 6, BLACK, rx=1))
    s.add(rect(418, 284, 56, 8, '#7a5a3c'), [rect(420 + i * 18, 292, 8, 6, '#5e4530') for i in range(3)])
    s.add([rect(420, 278 - i * 3, 52, 2.6, '#c3cbd1' if i % 2 else '#a7b1b9') for i in range(7)])
    # operator feeding the sheet
    P = standing(108, GY, 1, lean=4)
    reach(P, 'f', (172, 172))
    reach(P, 'b', (160, 182))
    s.add(person(P, helmet=HELMET_Y))
    return s.render('Illustration: sheet metal being bent on a press brake')


def welding():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.5,)))
    # welding curtain
    s.add(rect(14, 34, 110, FLOOR - 34, '#c0392b', opacity=.32), line(10, 34, 128, 34, '#55626d', 3))
    s.add([line(22 + i * 12, 36, 22 + i * 12, FLOOR, '#8e2b20', 1.2, opacity=.6) for i in range(9)])
    # gas cylinder + welding machine
    s.add(rect(430, 132, 26, 156, s.lgrad([(0, '#5e2424'), (.4, '#9b3a36'), (1, '#4d1d1d')], 0, 0, 1, 0), rx=12))
    s.add(rect(437, 118, 12, 16, '#9aa5ad', rx=2), circle(443, 116, 5, '#59636b'))
    s.add(rect(376, 236, 62, 54, '#d9dde0', stroke='#7b868f', rx=3), rect(382, 242, 30, 18, '#0e2233'), rect(386, 247, 18, 6, '#48e08a', opacity=.85))
    s.add(circle(424, 252, 6, BLACK), circle(398, 274, 4, '#26313a'), circle(414, 274, 4, '#26313a'))
    # table
    s.add(ellipse(300, 292, 140, 7, '#000', opacity=.5, filter=s.blur(5)))
    s.add(rect(182, 230, 8, 62, '#3b4650'), rect(410, 230, 8, 62, '#3b4650'), rect(186, 270, 228, 5, '#3b4650'))
    s.add(rect(170, 222, 260, 10, '#5d6b76', stroke='#3b4650'), rect(170, 222, 260, 2.5, '#8a98a3'))
    # enclosure frame of square tube (back, connectors, front)
    def tube(a, b, col):
        return [line(*a, *b, '#2b333a', 9, stroke_linecap='square'), line(*a, *b, col, 6.5, stroke_linecap='square')]
    F = [(214, 94), (334, 94), (334, 220), (214, 220)]
    B = [(p[0] + 46, p[1] - 26) for p in F]
    back = '#6f7c87'
    for i in range(4):
        s.add(tube(B[i], B[(i + 1) % 4], back))
    for i in range(4):
        s.add(tube(F[i], B[i], '#86939d'))
    for i in range(4):
        s.add(tube(F[i], F[(i + 1) % 4], '#aab5bd'))
    s.add(circle(220, 196, 150, s.rgrad([(0, AMBER, .28), (1, AMBER, 0)])))
    # welder
    P = standing(150, GY, 1, lean=8, crouch=12)
    reach(P, 'f', (198, 206))
    reach(P, 'b', (186, 214))
    s.add(path('M196 210 C188 262 300 300 382 268', stroke='#20262c', stroke_width=3.5))
    s.add(person(P, vest=False, headwear=None, mask='weld', suit=('#4d6b84', '#34506a')))
    s.add(line(196, 208, 212, 218, '#2b333a', 5, stroke_linecap='round'), line(208, 216, 214, 220, '#c9a227', 3, stroke_linecap='round'))
    s.add(glow_burst(s, 215, 220, 52))
    return s.render('Illustration: welding a steel enclosure frame')


def powder_coating():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.3,)))
    # booth
    s.add(rect(36, 30, 268, FLOOR - 30, '#c9d0d5'), rect(46, 40, 248, FLOOR - 40, '#4c6479'))
    s.add(poly([(46, 40), (294, 40), (262, 66), (78, 66)], '#5c768c'), poly([(46, 40), (78, 66), (78, 214), (46, FLOOR)], '#415a6f'),
          poly([(294, 40), (262, 66), (262, 214), (294, FLOOR)], '#567087'), poly([(46, FLOOR), (294, FLOOR), (262, 214), (78, 214)], '#6a8398'))
    s.add(rect(78, 66, 184, 148, '#3f566a'))
    for row in range(2):
        for i in range(3):
            fx, fy = 90 + i * 58, 76 + row * 68
            s.add(rect(fx, fy, 46, 58, '#8fa3b3', rx=3), [line(fx + 4 + k * 4.2, fy + 4, fx + 4 + k * 4.2, fy + 54, '#6f8496', 1) for k in range(10)])
    # conveyor and part
    s.add(rect(0, 18, 480, 7, '#2b333a'), [rect(x, 24, 12, 6, '#59636b') for x in (40, 132, 196, 300, 400)])
    s.add(line(140, 30, 140, 70, '#59636b', 1.6), line(196, 30, 196, 70, '#59636b', 1.6))
    s.add(rect(118, 70, 104, 132, '#7c8791'), rect(118, 70, 104, 132, s.lgrad([(0, '#9aa5ad', .0), (.5, '#c5ccd2', .5), (1, '#9aa5ad', 0)], 0, 0, 1, 1)))
    s.add(rect(118, 70, 60, 132, '#d7dde2'), rect(118, 70, 60, 132, s.lgrad([(0, '#ffffff', .35), (1, '#ffffff', 0)])))
    s.add(rect(126, 120, 4, 26, '#9aa5ad', rx=1.5))
    # powder cloud
    rnd = random.Random(7)
    cloud = []
    for _ in range(60):
        t = rnd.random()
        cx = 248 - t * 92 + rnd.uniform(-6, 6)
        cy = 142 + rnd.uniform(-1, 1) * (8 + t * 46)
        cloud.append(circle(cx, cy, rnd.uniform(3, 6 + t * 10), '#e8eef2', opacity=round(rnd.uniform(.06, .2), 2)))
    s.add(group(cloud, filter=s.blur(2.5), class_='dr'))
    # powder unit + hose
    s.add(rect(394, 206, 70, 82, '#d9dde0', stroke='#7b868f', rx=3), rect(404, 166, 46, 42, '#b8c1c8', stroke='#7b868f', rx=4), ellipse(427, 166, 23, 5, '#e3e8eb', stroke='#7b868f'))
    s.add(rect(402, 216, 30, 20, '#0e2233'), rect(406, 222, 20, 5, '#5ab4ff', opacity=.8), circle(446, 226, 5, BLACK), circle(410, 292, 5, '#26313a'), circle(450, 292, 5, '#26313a'))
    # operator spraying (facing left)
    P = standing(332, GY, -1, lean=3)
    reach(P, 'f', (262, 142), bend=-1)
    reach(P, 'b', (280, 156), bend=-1)
    s.add(path('M270 154 C296 230 360 250 400 236', stroke='#20262c', stroke_width=3))
    s.add(person(P, facing=-1, vest=False, headwear='hood', mask='resp', suit=('#dfe5ea', '#b6c1c9')))
    s.add(poly([(266, 136), (238, 138), (232, 141), (238, 144), (266, 146)], '#3b444c'), rect(262, 140, 7, 18, '#3b444c', rx=2), circle(232, 141, 2.2, '#9aa5ad'))
    s.add(circle(*P['arm_f'][-1], 4.9, SKIN))
    return s.render('Illustration: powder coating an enclosure door')


def wiring():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.62,)))
    x, y, w, h = 234, 30, 176, 238
    s.add(cabinet(s, x, y, w, h, depth=14, plinth=11))
    s.add(rect(x + 2, y + 2, w - 4, h - 4, INSIDE), rect(x + 8, y + 8, w - 16, h - 16, PLATE))
    px = x + 14
    for i, c in enumerate((RED, YELLOW, BLUE)):
        by = y + 16 + i * 12
        s.add(busbar(s, px + 4, by, w - 36, 7), rect(px + 4, by, 10, 7, c, rx=1))
    s.add(rect(px, y + 12, 6, 42, BLACK, rx=1), rect(x + w - 26, y + 12, 6, 42, BLACK, rx=1))
    for i in range(4):
        mx = px + 6 + i * 37
        s.add(busbar(s, mx + 12, y + 16 + (i % 3) * 12, 5, 64 - (i % 3) * 12, vertical=True))
        s.add(mccb(mx, y + 80, 30, 40))
    s.add(duct(px, y + 128, w - 28, 8))
    s.add(mcb_row(px + 4, y + 142, 13, 8, 18))
    s.add([contactor(px + 4 + i * 24, y + 168, 18, 20) for i in range(6)])
    s.add(duct(px, y + 194, w - 28, 8))
    s.add(terminals(px + 4, y + 206, 32, 3.6, 13))
    rnd = random.Random(4)
    for i in range(10):
        wx = px + 8 + i * 13
        s.add(polyline([(wx, y + 219), (wx + rnd.uniform(-3, 3), y + 228), (px + 60 + i * 3, h + y - 10)], rnd.choice([RED, BLUE, BLACK, YELLOW]), 1.5))
    s.add(poly([(x + w, y), (x + w + 44, y + 14), (x + w + 44, y + h - 12), (x + w, y + h)], s.lgrad([(0, '#aeb7be'), (1, '#8d98a1')], 0, 0, 1, 0), stroke=EDGE))
    # cable drum and toolbox
    s.add(ellipse(76, 294, 44, 6, '#000', opacity=.5, filter=s.blur(4)))
    s.add(circle(76, 262, 32, '#7a5a3c'), circle(76, 262, 25, '#b33a35'), [circle(76, 262, rr, 'none', stroke='#8c2925', stroke_width=1) for rr in (14, 18, 22)])
    s.add(circle(76, 262, 9, '#5e4530'), circle(76, 262, 4, '#2a1f17'))
    s.add(rect(118, 276, 40, 18, '#b33a35', rx=2), rect(130, 270, 16, 6, 'none', stroke='#2b333a', stroke_width=2.5, rx=2))
    # technician routing a wire
    P = standing(206, GY, 1, lean=2)
    hand_f, hand_b = (px + 14, y + 140), (236, 182)
    reach(P, 'f', hand_f)
    reach(P, 'b', hand_b)
    s.add(path(f'M96 250 C150 230 170 200 {hand_b[0]} {hand_b[1]} S{hand_f[0] - 10} {hand_f[1] + 6} {hand_f[0] + 6} {hand_f[1] - 2}', stroke=RED, stroke_width=2))
    s.add(person(P, helmet=HELMET_W))
    return s.render('Illustration: technician wiring and fitting busbars in a panel')


def testing():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.28, .74)))
    # panel under test
    x, y, w, h = 296, 40, 150, 226
    s.add(cabinet(s, x, y, w, h, depth=13, plinth=11))
    s.add(door(s, x, y, 75, 104), door(s, x + 75, y, 75, 104))
    s.add(meter_digital(s, x + 12, y + 14, 44, 30), meter_digital(s, x + 87, y + 14, 44, 30, AMBER))
    s.add([lamp(s, x + 16 + i * 14, y + 62, c, 3.4) for i, c in enumerate((GREEN, GREEN, GREEN))], [lamp(s, x + 91 + i * 14, y + 62, c, 3.4) for i, c in enumerate((GREEN, AMBER, GREEN))])
    s.add(nameplate(x + 14, y + 82, 46), nameplate(x + 89, y + 82, 46))
    oy = y + 104
    s.add(rect(x + 2, oy, w - 4, 78, INSIDE), rect(x + 6, oy + 4, w - 12, 70, PLATE))
    s.add(mcb_row(x + 12, oy + 10, 14, 8, 18), duct(x + 10, oy + 32, w - 20, 7), terminals(x + 12, oy + 46, 28, 3.6, 14))
    s.add(door(s, x, oy + 78, w, h - 182), louvers(x + 20, y + h - 26, w - 40, 3))
    # test bench + instrument
    s.add(ellipse(110, 292, 96, 6, '#000', opacity=.5, filter=s.blur(4)))
    s.add(rect(22, 214, 178, 9, '#5d6b76', stroke='#3b4650'), rect(30, 223, 7, 68, '#3b4650'), rect(186, 223, 7, 68, '#3b4650'))
    s.add(rect(36, 150, 96, 64, '#d9dde0', stroke='#7b868f', rx=4), rect(44, 158, 54, 36, '#0b1712'))
    s.add(path('M48 186 l8 -10 l8 6 l8 -16 l8 12 l8 -8', stroke='#48e08a', stroke_width=1.6))
    s.add(circle(114, 166, 7, BLACK), circle(114, 166, 2, '#9aa5ad'), circle(114, 188, 5, BLACK), [circle(50 + i * 12, 204, 2.6, (RED, BLACK, YELLOW)[i]) for i in range(3)])
    s.add(rect(140, 196, 40, 18, '#eef0f1', stroke='#9aa3aa', rx=2, transform='rotate(-6 160 205)'), [rect(146, 200 + i * 4, 26, 1.2, '#7b868f', transform='rotate(-6 160 205)') for i in range(3)])
    s.add(path('M62 204 C80 280 240 300 300 262', stroke=RED, stroke_width=2.2), path('M50 204 C70 290 240 306 310 266', stroke=BLACK, stroke_width=2.2))
    # technician with meter
    P = standing(250, GY, 1, lean=4)
    probe_hand = (x + 4, oy + 52)
    reach(P, 'f', probe_hand)
    reach(P, 'b', (282, 172))
    s.add(person(P, helmet=HELMET_W))
    s.add(rect(274, 160, 18, 28, YELLOW, rx=3, transform='rotate(-12 283 174)'), rect(277, 164, 12, 8, '#0b1712', transform='rotate(-12 283 174)'), circle(283, 180, 4, BLACK, transform='rotate(-12 283 174)'))
    s.add(path(f'M286 186 C300 200 {probe_hand[0] - 10} {probe_hand[1] + 10} {probe_hand[0]} {probe_hand[1]}', stroke=RED, stroke_width=1.3))
    s.add(line(probe_hand[0] - 2, probe_hand[1], probe_hand[0] + 16, probe_hand[1] - 4, RED, 3, stroke_linecap='round'), line(probe_hand[0] + 16, probe_hand[1] - 4, probe_hand[0] + 24, probe_hand[1] - 6, '#c9ced2', 1.4))
    s.add(circle(*probe_hand, 4.9, SKIN))
    return s.render('Illustration: technician testing a finished panel')


def commissioning():
    s = Svg(480, 320)
    s.add(scene_bg(s, FLOOR, lights=(.55,), wall=('#15303f', '#0f2433')))
    # cable tray and pipes
    s.add(rect(0, 30, 480, 6, '#55626d'), [rect(i * 30, 26, 2, 10, '#55626d') for i in range(17)], [line(0, 28 - k * 2, 480, 28 - k * 2, '#20262c', 2) for k in range(3)])
    s.add(rect(0, 52, 300, 16, s.lgrad([(0, '#6f9a86'), (.5, '#4f7a68'), (1, '#36594a')])), [rect(fx, 48, 8, 24, '#3f6656', rx=1) for fx in (80, 196)])
    s.add(rect(0, 82, 264, 11, s.lgrad([(0, '#7d9cb8'), (1, '#4b6a87')])), rect(150, 93, 11, 132, s.lgrad([(0, '#7d9cb8'), (1, '#4b6a87')], 0, 0, 1, 0)))
    s.add(circle(156, 116, 11, 'none', stroke=RED, stroke_width=2.5), line(145, 116, 167, 116, RED, 2), line(156, 105, 156, 127, RED, 2))
    # motor-pump set
    s.add(ellipse(104, 284, 80, 6, '#000', opacity=.5, filter=s.blur(4)))
    s.add(rect(24, 268, 162, 10, '#2b333a'))
    s.add(rect(34, 226, 76, 42, s.lgrad([(0, '#5d8fbf'), (.5, '#3e6f9f'), (1, '#2b5279')]), rx=6), [line(44 + i * 7, 228, 44 + i * 7, 266, '#2b5279', 1.4) for i in range(9)])
    s.add(rect(28, 230, 12, 34, '#2b5279', rx=5), rect(110, 236, 16, 24, AMBER, rx=2))
    s.add(circle(152, 244, 24, s.rgrad([(0, '#aab4bb'), (1, '#6f7a83')])), circle(152, 244, 8, '#59636b'), rect(146, 222, 12, 8, '#6f7a83'))
    s.add(rect(147, 200, 10, 24, '#6f7a83'))
    # installed panel
    x, y, w, h = 300, 54, 150, 214
    s.add(cabinet(s, x, y, w, h, depth=13, plinth=10))
    th = h / 4
    for i in range(4):
        for k in range(2):
            s.add(door(s, x + k * 75, y + i * th, 75, th))
            s.add(meter_analog(x + k * 75 + 8, y + i * th + 10, 16), lamp(s, x + k * 75 + 40, y + i * th + th / 2, GREEN, 3), lamp(s, x + k * 75 + 54, y + i * th + th / 2, AMBER if (i, k) == (2, 1) else '#55606a', 3, glow=(i, k) == (2, 1)))
    s.add(rect(x + 10, y + h - 30, 12, 8, '#20272d', rx=1))
    # engineer with laptop
    P = standing(236, GY, 1, lean=1)
    reach(P, 'f', (270, 186))
    reach(P, 'b', (256, 190))
    s.add(person(P, helmet=HELMET_W))
    s.add(poly([(250, 186), (296, 186), (300, 192), (246, 192)], '#9aa5ad'), poly([(254, 186), (292, 186), (298, 156), (262, 156)], '#2b333a'))
    s.add(poly([(257, 183), (290, 183), (295, 159), (264, 159)], '#0e2233'), poly([(262, 178), (282, 178), (286, 163), (268, 163)], '#48e08a', opacity=.25))
    s.add([line(266 + i * 2, 176 - i * 4, 282 + i * 2, 176 - i * 4, '#48e08a', 1.4) for i in range(3)])
    s.add(circle(270, 188, 4.9, SKIN), circle(256, 190, 4.6, SKIN_D))
    s.add(path(f'M298 190 C320 214 300 240 {x + 16} {y + h - 22}', stroke='#5ab4ff', stroke_width=1.8))
    return s.render('Illustration: engineer commissioning a panel on site')


def tech_at_panel():
    s = Svg(480, 400)
    floor = 332
    s.add(scene_bg(s, floor, lights=(.55,)))
    x, y, w, h = 186, 28, 250, 300
    s.add(cabinet(s, x, y, w, h, depth=16, plinth=12))
    s.add(rect(x + 2, y + 2, w - 4, h - 4, INSIDE), rect(x + 8, y + 8, w - 16, h - 16, '#a9b3ba'))
    for i in range(3):
        s.add(busbar(s, x + 24 + i * 18, y + 14, 10, h - 28, vertical=True))
    for sy in (y + 30, y + 150, y + 268):
        s.add(rect(x + 16, sy, 62, 10, BLACK, rx=2))
    for row in range(3):
        ry = y + 26 + row * 92
        for i in range(3):
            s.add(busbar(s, x + 29 + i * 18, ry + 14 + i * 9, 92 - i * 18, 6))
        s.add(mccb(x + 120, ry, 44, 62), mccb(x + 178, ry, 44, 62, on=row != 1))
        s.add(circle(x + 29, ry + 17, 2, '#5b3a22'), circle(x + 47, ry + 26, 2, '#5b3a22'), circle(x + 65, ry + 35, 2, '#5b3a22'))
        s.add(duct(x + 116, ry + 70, 110, 7))
    s.add(poly([(x + w, y), (x + w + 34, y + 16), (x + w + 34, y + h - 14), (x + w, y + h)], s.lgrad([(0, '#aeb7be'), (1, '#8d98a1')], 0, 0, 1, 0), stroke=EDGE))
    # technician tightening a busbar joint
    P = standing(160, 392, 1, lean=6)
    joint = (x + 47, y + 26 + 184 + 26)
    hand = (joint[0] - 22, joint[1] + 12)
    reach(P, 'f', hand)
    reach(P, 'b', (190, 300))
    s.add(person(P, helmet=HELMET_W))
    s.add(line(hand[0] - 8, hand[1] + 6, joint[0], joint[1], '#7b868f', 4.5, stroke_linecap='round'), circle(*joint, 4.2, '#59636b'), line(hand[0] - 14, hand[1] + 10, hand[0] - 2, hand[1] + 2, '#c94f3d', 6, stroke_linecap='round'))
    s.add(circle(*hand, 4.9, SKIN))
    s.add(rect(178, 286, 24, 32, '#20272d', rx=3, transform='rotate(-14 190 302)'), rect(181, 290, 18, 22, '#0e2233', transform='rotate(-14 190 302)'), rect(184, 294, 12, 2, '#48e08a', transform='rotate(-14 190 302)'))
    s.add(circle(190, 300, 4.6, SKIN_D))
    return s.render('Illustration: technician tightening busbar connections inside a panel')


SCENES = {
    'work-sheet-metal.svg': press_brake, 'work-welding.svg': welding, 'work-powder-coating.svg': powder_coating,
    'work-wiring.svg': wiring, 'work-testing.svg': testing, 'work-commissioning.svg': commissioning,
    'technician-panel.svg': tech_at_panel,
}
