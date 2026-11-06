"""Front-elevation illustrations of the six SVI panel types (transparent background)."""
import math
from svgkit import *


def pcc():
    s = Svg(560, 300)
    x, y, w, h = 50, 46, 430, 206
    s.add(cabinet(s, x, y, w, h, depth=16, plinth=12))
    cols = [(50, 120), (170, 108), (278, 108), (386, 94)]
    for cx, cw in cols:  # busbar chamber
        s.add(door(s, cx, y, cw, 30, handle=None), louvers(cx + 14, y + 9, cw - 28, 3))
    # incomer
    ix, iw, iy = 50, 120, y + 30
    s.add(door(s, ix, iy, iw, h - 30))
    s.add(meter_digital(s, ix + 12, iy + 12, 44, 30))
    for i, c in enumerate((RED, AMBER, BLUE)):
        s.add(lamp(s, ix + 70 + i * 13, iy + 20, c))
    s.add(selector(ix + 83, iy + 38))
    s.add(door_cutout(ix + 16, iy + 56, 86, 66), acb(ix + 16, iy + 56, 86, 66))
    s.add(nameplate(ix + 30, iy + 132, 58), danger_sign(ix + 50, iy + 144, 14), louvers(ix + 14, iy + 162, iw - 28, 3))
    # outgoing feeders
    for cx, cw in cols[1:3]:
        mh = (h - 30) / 4
        for i in range(4):
            my = iy + i * mh
            s.add(door(s, cx, my, cw, mh))
            s.add(nameplate(cx + 10, my + 6, 34, 5))
            s.add(door_cutout(cx + 14, my + 15, 34, 22), mccb(cx + 14, my + 15, 34, 22, on=(i != 2)))
            s.add(lamp(s, cx + 64, my + 26, GREEN if i != 2 else RED, 3.2))
    # cable alley
    ax, aw = cols[3]
    s.add(door(s, ax, iy, aw, h - 30), louvers(ax + 14, iy + 12, aw - 28, 4), louvers(ax + 14, iy + 140, aw - 28, 4))
    s.add(danger_sign(ax + aw / 2 - 8, iy + 74, 16), nameplate(ax + 18, iy + 100, aw - 36))
    return s.render('PCC panel illustration')


def mcc():
    s = Svg(360, 240)
    x, y, w, h = 40, 34, 264, 178
    s.add(cabinet(s, x, y, w, h, depth=13, plinth=10))
    sw = w / 3
    for k in range(3):
        sx = x + k * sw
        s.add(door(s, sx, y, sw, 24, handle=None), louvers(sx + 14, y + 7, sw - 28, 3, 4))
        tiers = [(0, 2), (2, 1), (3, 1), (4, 1)] if k == 0 else [(i, 1) for i in range(5)]
        th = (h - 24) / 5
        for t0, span in tiers:
            ty, tht = y + 24 + t0 * th, th * span
            s.add(door(s, sx, ty, sw, tht))
            if span == 2:
                s.add(meter_digital(s, sx + 8, ty + 8, 30, 22), door_cutout(sx + 46, ty + 10, 24, 34), mccb(sx + 46, ty + 10, 24, 34))
                for i, c in enumerate((RED, AMBER, BLUE)):
                    s.add(lamp(s, sx + 13 + i * 10, ty + 44, c, 2.8))
            else:
                run = not (k == 1 and t0 == 3)
                s.add(meter_analog(sx + 7, ty + 7, 15))
                s.add(button(sx + 32, ty + tht / 2, GREEN, 3), button(sx + 44, ty + tht / 2, RED, 3))
                s.add(lamp(s, sx + 58, ty + tht / 2, GREEN if run else AMBER, 2.9))
    return s.render('MCC panel illustration')


def plc():
    s = Svg(360, 240)
    x, y, w, h = 72, 22, 150, 194
    s.add(cabinet(s, x, y, w, h, depth=12, plinth=10))
    # interior (right half)
    ix, iw = x + 75, 75
    s.add(rect(ix, y + 1, iw - 1, h - 2, INSIDE), rect(ix + 3, y + 4, iw - 7, h - 8, PLATE))
    px = ix + 5
    s.add(duct(px, y + 7, iw - 11, 7))
    s.add(plc_rack(px + 2, y + 18, n=4, h=26))
    s.add(duct(px, y + 48, iw - 11, 6))
    s.add(mcb_row(px + 2, y + 58, 6, 6, 15), rect(px + 44, y + 57, 18, 17, '#c9ced2', stroke='#8b959d', stroke_width=.5))
    s.add([rect(px + 46, y + 60 + i * 3, 14, 1.2, '#8b959d') for i in range(4)])
    s.add(duct(px, y + 78, iw - 11, 6))
    s.add([contactor(px + 2 + i * 15.5, y + 89) for i in range(4)])
    s.add(duct(px, y + 110, iw - 11, 6))
    s.add(terminals(px + 2, y + 121, 15))
    wires = [RED, BLUE, BLACK, YELLOW, BLUE, RED, '#9aa3aa']
    for i, c in enumerate(wires):
        wx = px + 4 + i * 8.5
        s.add(polyline([(wx, y + 133), (wx, y + 150 + (i % 3) * 4), (px + 30 + i * 2, y + 172), (px + 30 + i * 2, y + h - 6)], c, 1.4))
    s.add(duct(px, y + 140, 6, h - 146, horizontal=False))
    # open door (inner side)
    s.add(poly([(x + w, y), (x + w + 46, y + 14), (x + w + 46, y + h - 12), (x + w, y + h)], s.lgrad([(0, '#aeb7be'), (1, '#8d98a1')], 0, 0, 1, 0), stroke=EDGE, stroke_width=1))
    s.add(poly([(x + w + 5, y + 8), (x + w + 41, y + 19), (x + w + 41, y + h - 17), (x + w + 5, y + h - 8)], 'none', stroke='#3a434b', stroke_width=1.6, opacity=.6))
    s.add(poly([(x + w + 12, y + 110), (x + w + 34, y + 116), (x + w + 34, y + 160), (x + w + 12, y + 160)], '#7b868f', opacity=.8))
    # closed left door with HMI
    lx, lw = x, 75
    s.add(door(s, lx, y, lw, h, handle='right'))
    s.add(rect(lx + 9, y + 16, 56, 44, '#20272d', rx=2.5), rect(lx + 13, y + 20, 48, 34, '#0e2233'))
    s.add(rect(lx + 13, y + 20, 48, 6, AMBER, opacity=.9))
    for i, hgt in enumerate((14, 20, 10, 24, 17)):
        s.add(rect(lx + 17 + i * 8.5, y + 52 - hgt, 5, hgt, '#48e08a' if i != 3 else AMBER, opacity=.85))
    s.add(rect(lx + 13, y + 20, 48, 34, '#5ab4ff', opacity=.12, filter=s.blur(2)))
    s.add(rect(lx + 22, y + 74, 30, 30, YELLOW, rx=2), circle(lx + 37, y + 89, 10.5, '#a92f33'), circle(lx + 37, y + 89, 8.5, RED), circle(lx + 34, y + 86, 3, '#fff', opacity=.35))
    for i, c in enumerate((GREEN, AMBER, RED)):
        s.add(lamp(s, lx + 18 + i * 19, y + 122, c, 3.4))
    s.add(button(lx + 18, y + 140, GREEN), button(lx + 37, y + 140, RED), selector(lx + 56, y + 140))
    s.add(nameplate(lx + 14, y + 156, 46), louvers(lx + 14, y + 172, 46, 3))
    return s.render('PLC automation panel illustration')


def amf():
    s = Svg(360, 240)
    x, y, w, h = 44, 34, 256, 176
    s.add(cabinet(s, x, y, w, h, depth=13, plinth=10))
    sw = w / 2
    for k in range(2):
        sx = x + k * sw
        s.add(door(s, sx, y, sw, h, handle='right' if k else 'left'))
    # section A: genset controller
    ax = x
    s.add(rect(ax + 14, y + 12, 58, 40, '#20272d', rx=2), rect(ax + 18, y + 16, 34, 22, '#0b1712'))
    s.add(path(f'M{ax + 20} {y + 31} q4 -9 8 0 t8 0 t8 0 t8 0', stroke='#48e08a', stroke_width=1.3))
    s.add([button(ax + 60, y + 20 + i * 9, c, 2.4) for i, c in enumerate((GREEN, RED, '#9aa3aa'))])
    s.add([rect(ax + 18 + i * 9, y + 42, 7, 5, '#3a434b', rx=1) for i in range(4)])
    # section B: synchroscope + meter
    bx = x + sw
    s.add(rect(bx + 16, y + 12, 40, 40, DARK, rx=2), circle(bx + 36, y + 32, 16, '#f2f0ea'))
    for i in range(12):
        a = math.radians(i * 30)
        s.add(line(bx + 36 + math.cos(a) * 12, y + 32 + math.sin(a) * 12, bx + 36 + math.cos(a) * 15, y + 32 + math.sin(a) * 15, '#333', .8))
    s.add(line(bx + 36, y + 32, bx + 43, y + 20, RED, 1.4), circle(bx + 36, y + 32, 1.6, '#333'))
    s.add(meter_digital(s, bx + 66, y + 12, 44, 28, AMBER))
    s.add(lamp(s, bx + 74, y + 48, GREEN, 3), lamp(s, bx + 88, y + 48, AMBER, 3), lamp(s, bx + 102, y + 48, RED, 3))
    # mimic single-line diagram across both doors
    def ml(x1, y1, x2, y2):
        return line(x1, y1, x2, y2, AMBER, 2.4, stroke_linecap='round')
    gx1, gx2, gy, busy = ax + 50, bx + 64, y + 82, y + 134
    s.add(circle(gx1, gy, 10, 'none', stroke=AMBER, stroke_width=2.2))
    s.add(path(f'M{gx1 - 6} {gy} q3 -6 6 0 t6 0', stroke=AMBER, stroke_width=1.6))
    s.add(circle(gx2 - 4, gy, 8, 'none', stroke=AMBER, stroke_width=2), circle(gx2 + 5, gy, 8, 'none', stroke=AMBER, stroke_width=2))
    for gxx, col in ((gx1, GREEN), (gx2, RED)):
        top = gy + 10 if gxx == gx1 else gy + 8
        s.add(ml(gxx, top, gxx, y + 106), rect(gxx - 6, y + 106, 12, 12, col, stroke=DARK, stroke_width=1), ml(gxx, y + 118, gxx, busy))
    s.add(ml(ax + 16, busy, bx + sw - 16, busy))
    for i in range(3):
        s.add(ml(ax + 40 + i * 70, busy, ax + 40 + i * 70, busy + 14), poly([(ax + 36 + i * 70, busy + 14), (ax + 44 + i * 70, busy + 14), (ax + 40 + i * 70, busy + 20)], AMBER))
    s.add(louvers(ax + 16, y + h - 22, sw - 32, 3), louvers(bx + 16, y + h - 22, sw - 32, 3))
    s.add(nameplate(ax + 30, y + 58, 50), danger_sign(bx + sw - 30, y + h - 46, 14))
    return s.render('AMF and synchronizing panel illustration')


def apfc():
    s = Svg(360, 240)
    x, y, w, h = 94, 22, 172, 192
    s.add(cabinet(s, x, y, w, h, depth=13, plinth=10))
    th = 76
    s.add(door(s, x, y, w, th))
    s.add(rect(x + 12, y + 12, 44, 44, '#20272d', rx=2), rect(x + 16, y + 16, 36, 16, '#1a0f05'))
    s.add([rect(x + 19 + i * 8.2, y + 19, 6, 10, AMBER, opacity=.95, rx=.8) for i in range(4)])
    s.add(rect(x + 16, y + 16, 36, 16, AMBER, opacity=.2, filter=s.blur(2)))
    s.add([circle(x + 19 + i * 5, y + 40, 1.4, GREEN if i < 5 else '#3a434b') for i in range(7)])
    s.add([rect(x + 18 + i * 9, y + 46, 7, 5, '#3a434b', rx=1) for i in range(4)])
    s.add(meter_digital(s, x + 66, y + 12, 44, 30))
    s.add(circle(x + 140, y + 32, 18, '#3a434b'), circle(x + 140, y + 32, 15.5, '#262d33'))
    s.add([circle(x + 140, y + 32, rr, 'none', stroke='#59636b', stroke_width=1) for rr in (5, 9, 13)])
    s.add(line(x + 125, y + 32, x + 155, y + 32, '#59636b', 1), line(x + 140, y + 17, x + 140, y + 47, '#59636b', 1))
    s.add([lamp(s, x + 18 + i * 13.5, y + 64, GREEN if i < 5 else '#55606a', 2.6, glow=i < 5) for i in range(8)])
    # open capacitor compartment
    cy = y + th + 2
    ch = h - th - 4
    s.add(rect(x + 2, cy, w - 4, ch, INSIDE), rect(x + 6, cy + 4, w - 12, ch - 8, '#3b4a57'))
    s.add([contactor(x + 12 + i * 26, cy + 8, 16, 15) for i in range(6)])
    for row in range(2):
        for i in range(6):
            s.add(capacitor(s, x + 12 + i * 26, cy + 30 + row * 40, 17, 34))
    for i in range(6):
        s.add(polyline([(x + 17 + i * 26, cy + 23), (x + 17 + i * 26, cy + 31)], BLACK, 1.4), polyline([(x + 23 + i * 26, cy + 23), (x + 23 + i * 26, cy + 31)], RED, 1.2))
    return s.render('APFC capacitor panel illustration')


def busduct():
    s = Svg(360, 240)
    # bus duct run
    g = s.lgrad([(0, '#aab4bb'), (.5, '#d4dade'), (1, '#7e8a93')])
    s.add(ellipse(110, 214, 100, 7, '#000', opacity=.45, filter=s.blur(5)))
    s.add(rect(8, 46, 178, 24, g, stroke=EDGE, stroke_width=1))
    s.add(path('M186 46 h14 a12 12 0 0 1 12 12 v150 h-24 v-138 h-2z', g, stroke=EDGE, stroke_width=1))
    s.add(rect(186, 46, 2, 24, '#7e8a93'))
    for jx in (58, 128):
        s.add(rect(jx, 42, 16, 32, '#8f9aa3', stroke=EDGE, stroke_width=1, rx=1.5), [circle(jx + 8, 46 + i * 8, 1.4, '#5b6670') for i in range(4)])
    s.add(rect(184, 128, 32, 14, '#8f9aa3', stroke=EDGE, stroke_width=1, rx=1.5), rect(180, 206, 40, 6, '#5b6670'))
    # tap-off box
    s.add(rect(84, 70, 40, 54, STEEL, stroke=EDGE, stroke_width=1), rect(87, 73, 34, 48, 'none', stroke='#eef2f4', stroke_width=.6))
    s.add(door_cutout(94, 82, 20, 26), mccb(94, 82, 20, 26), lamp(s, 104, 116, GREEN, 2.4))
    s.add(path('M104 124 C104 160 96 180 96 214', stroke=BLACK, stroke_width=5, stroke_linecap='round'))
    # feeder pillar
    fx, fy, fw, fh = 232, 82, 100, 116
    s.add(ellipse(fx + fw / 2 + 6, fy + fh + 18, fw * .65, 8, '#000', opacity=.5, filter=s.blur(5)))
    s.add(rect(fx - 8, fy + fh + 4, fw + 16, 12, '#5b6670'), rect(fx - 8, fy + fh + 4, fw + 16, 3, '#76828c'))
    s.add(cabinet(s, fx, fy, fw, fh, depth=12, plinth=4, shadow=False))
    s.add(poly([(fx - 8, fy), (fx + fw + 8, fy), (fx + fw + 20, fy - 8), (fx + fw - 2, fy - 18), (fx + 2, fy - 18)], '#8f9aa3', stroke=EDGE, stroke_width=1))
    s.add(poly([(fx - 8, fy), (fx + 2, fy - 18), (fx + fw - 2, fy - 18), (fx + fw + 8, fy)], s.lgrad([(0, '#b6bfc6'), (1, '#909ba4')]), stroke=EDGE, stroke_width=1))
    s.add(door(s, fx, fy, fw / 2, fh, handle='right'), door(s, fx + fw / 2, fy, fw / 2, fh, handle='left'))
    s.add(danger_sign(fx + 17, fy + 16, 16), nameplate(fx + 60, fy + 20, 30))
    s.add(louvers(fx + 8, fy + fh - 26, fw / 2 - 16, 3), louvers(fx + fw / 2 + 8, fy + fh - 26, fw / 2 - 16, 3))
    s.add(lamp(s, fx + 70, fy + 44, GREEN, 3), lamp(s, fx + 82, fy + 44, GREEN, 3))
    return s.render('Bus duct and feeder pillar illustration')


PANELS = {'panel-pcc.svg': pcc, 'panel-mcc.svg': mcc, 'panel-plc.svg': plc, 'panel-amf.svg': amf, 'panel-apfc.svg': apfc, 'panel-busduct.svg': busduct}
