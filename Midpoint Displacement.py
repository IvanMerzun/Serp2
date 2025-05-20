import matplotlib.pyplot as plt
import random

class InfiniteMidpointDisplacement:
    def __init__(self, roughness=0.5, depth=8, segment_length=1.0):
        self.roughness = roughness
        self.depth = depth
        self.segment_length = segment_length
        self.points = []
        self.generated_ranges = set()
        self.y_last = 0.0

    def midpoint_displacement(self, x_start, x_end, y_start, y_end, disp):
        def subdivide(p1, p2, d, level):
            if level == 0:
                return [p1, p2]
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2 + random.uniform(-d, d)
            midpoint = (mid_x, mid_y)
            left = subdivide(p1, midpoint, d * self.roughness, level - 1)
            right = subdivide(midpoint, p2, d * self.roughness, level - 1)
            return left[:-1] + right

        return subdivide((x_start, y_start), (x_end, y_end), disp, self.depth)

    def ensure_range(self, x_start, x_end):
        x = int(x_start)
        while x < int(x_end):
            if x not in self.generated_ranges:
                y2 = self.y_last + random.uniform(-0.5, 0.5)
                segment = self.midpoint_displacement(
                    x, x + self.segment_length,
                    self.y_last, y2,
                    disp=1.0
                )
                self.points.extend(segment[:-1])
                self.y_last = y2
                self.generated_ranges.add(x)
            x += int(self.segment_length)

    def get_points_in_view(self, view_start, view_end):
        self.ensure_range(view_start - 2, view_end + 2)
        return [pt for pt in self.points if view_start <= pt[0] <= view_end]

# Инициализация генератора
terrain = InfiniteMidpointDisplacement()

# Окно просмотра
view_x = 0.0
view_width = 10.0
view_y1 = -5
view_y2 = 5

# Создание графика
fig, ax = plt.subplots(figsize=(12, 4))
line, = ax.plot([], [], lw=2)
ax.set_ylim(view_y1, view_y2)

def update_plot():
    visible = terrain.get_points_in_view(view_x, view_x + view_width)
    x_vals, y_vals = zip(*visible) #разбивает список на два отдельных для х и у
    line.set_data(x_vals, y_vals)
    ax.set_xlim(view_x, view_x + view_width)
    ax.set_ylim(view_y1, view_y2)
    fig.canvas.draw_idle()

def on_key(event):
    global view_x, view_y1, view_y2
    if event.key == 'right':
        view_x += 1.0
    elif event.key == 'left':
        view_x -= 1.0
    elif event.key == 'up':
        view_y1 += 1
        view_y2 += 1
    elif event.key == 'down':
        view_y1 += -1
        view_y2 += -1
    update_plot()

fig.canvas.mpl_connect('key_press_event', on_key)

update_plot()
plt.title("Midpoint Displacement ")
plt.grid(True)
plt.show()