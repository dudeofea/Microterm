import st7565
import math

class GraphicDisplay:
    def __init__(self):
        self.display = st7565.ST7565()
        self.display.set_contrast(0x20)
        self.clear()

    def clear(self):
        self.buf = [0] * int(self.display.width * self.display.height / 8)
        self.buf_ind = []
        self.display.clear()

    def refresh(self):
        for ind in self.buf_ind:
            self.display.add_blocks(
                self.buf[ind[0]:ind[1]], ind[2])

    def pixel(self, x, y, value):
        y_cur = int(y / 8)
        buf_ind = y_cur * self.display.width + x
        val = self.buf[buf_ind] | 0x1 << (7 - y % 8)
        self.buf[buf_ind] = val
        self.buf_ind.append((buf_ind, buf_ind+1, (x, y_cur)))

    def circle(self, x, y, radius, value):
        # get center pixel (or pixel edge) at 45deg
        r2 = radius * radius
        center_float = radius / math.sqrt(2)
        center = (
            math.ceil(center_float) + 0.5,
            math.floor(center_float) - 0.5,
            (math.ceil(center_float) + math.floor(center_float)) / 2
        )
        center_err = [abs(2*c*c - r2) for c in center]
        center_err[2] *= 2
        #print("Error: (ceil, floor, mix) ", center_err, radius)
        if center_err[2] <= center_err[0] and center_err[2] <= center_err[1]:
            cur_point = math.floor(center_float), math.ceil(center_float)
        elif center_err[0] < center_err[1]:
            cur_point = math.ceil(center_float), math.ceil(center_float)
        else:
            cur_point = math.floor(center_float), math.floor(center_float)

        # calc 45deg segment
        points = []
        while cur_point[0] > 0:
            #print("Current:  ", cur_point, points)
            pot = [
                (cur_point[0]-1, cur_point[1]),
                (cur_point[0]-1, cur_point[1]+1),
                (cur_point[0], cur_point[1]+1)
            ]
            res = [abs(float(p[0]*p[0] + p[1]*p[1]) - r2) for p in pot]
            res_min = min(res)
            #print("Potential:", pot, res)
            points.append(cur_point)
            cur_point = pot[res.index(res_min)]
        points.append(cur_point)

        # display
        for pnt in points:
            self.pixel(x + pnt[0], y + pnt[1], value)
            self.pixel(x - pnt[0], y + pnt[1], value)
            self.pixel(x + pnt[0], y - pnt[1], value)
            self.pixel(x - pnt[0], y - pnt[1], value)
            self.pixel(x + pnt[1], y + pnt[0], value)
            self.pixel(x - pnt[1], y + pnt[0], value)
            self.pixel(x + pnt[1], y - pnt[0], value)
            self.pixel(x - pnt[1], y - pnt[0], value)
