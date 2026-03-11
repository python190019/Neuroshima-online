from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath
import math


class TicTacToeApp(ShowBase):
    """Hex-based tic-tac-toe demo.

    Uses a pointy-top hex layout. The board is a hexagon with diameter=3
    (radius=1). Win condition: 3 in a straight line along any hex axis
    (this includes "side" directions).

    Kod nie pisany przezemnie (AI), ale dziala i to nieźle. Obsluguje zapis na hexagonalnej planszy.
    """

    def __init__(self):
        super().__init__()
        self.disableMouse()

        # Hex board parameters
        # Use radius=2 (diameter=5) as requested
        self.RADIUS = 2

        # we'll compute hex_size so the board occupies ~1/2 of the screen
        self.target_screen_fraction = 0.5
        self.hex_size = self.compute_hex_size_for_screen_fraction(self.RADIUS, self.target_screen_fraction)

        # Logical board: map (q,r) axial -> None/'X'/'O'
        self.board = {}
        for q in range(-self.RADIUS, self.RADIUS + 1):
            for r in range(-self.RADIUS, self.RADIUS + 1):
                s = -q - r
                if abs(s) <= self.RADIUS:
                    self.board[(q, r)] = None

        self.current = 'X'

        # Node to hold grid and marks (attach to aspect2d to draw in 2D)
        self.grid_node = self.aspect2d.attachNewNode('grid')
        self.hex_nodes = {}  # map (q,r) -> NodePath for hex outlines
        self.marks = {}  # map (q,r) -> NodePath for X/O

        self.draw_board()

        self.status = OnscreenText(text=f"Current: {self.current}", pos=(0, 0.9), scale=0.06)

        # Input
        self.accept('mouse1', self.on_click)
        self.accept('r', self.reset_game)

    # (no chess clock in this version)

    # Layout math for pointy-top hexes
    def hex_to_pixel(self, q, r):
        x = self.hex_size * math.sqrt(3) * (q + r / 2.0)
        y = self.hex_size * 1.5 * r
        return x, y

    def pixel_to_hex(self, x, y):
        q = (math.sqrt(3) / 3 * x - 1.0 / 3 * y) / self.hex_size
        r = (2.0 / 3 * y) / self.hex_size
        return self.hex_round(q, r)

    def hex_round(self, qf, rf):
        xf = qf
        zf = rf
        yf = -xf - zf

        xr = round(xf)
        yr = round(yf)
        zr = round(zf)

        x_diff = abs(xr - xf)
        y_diff = abs(yr - yf)
        z_diff = abs(zr - zf)

        if x_diff > y_diff and x_diff > z_diff:
            xr = -yr - zr
        elif y_diff > z_diff:
            yr = -xr - zr
        else:
            zr = -xr - yr

        return int(xr), int(zr)

    def draw_hex(self, cx, cy, size, thickness=2.0, color=None):
        ls = LineSegs()
        ls.setThickness(thickness)
        pts = []
        for i in range(6):
            angle = math.radians(60 * i - 30)  # pointy-top
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            pts.append((x, y))

        ls.moveTo(pts[0][0], 0, pts[0][1])
        for (x, y) in pts[1:]:
            ls.drawTo(x, 0, y)
        ls.drawTo(pts[0][0], 0, pts[0][1])
        node = ls.create()
        np_hex = NodePath(node)
        np_hex.reparentTo(self.grid_node)
        return np_hex

    def compute_hex_size_for_screen_fraction(self, radius, fraction):
        """Compute hex_size so the bounding box of the hex board uses about
        `fraction` of the screen width/height (aspect2d coordinates span -1..1).

        We compute centers with a unit size then scale them to fit into the
        target bounding box (2 * fraction in aspect2d units). A small margin
        is applied.
        """
        # temporary size = 1.0 for layout
        temp_size = 1.0
        xs = []
        ys = []
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q - r
                if abs(s) <= radius:
                    x = temp_size * math.sqrt(3) * (q + r / 2.0)
                    y = temp_size * 1.5 * r
                    xs.append(x)
                    ys.append(y)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x
        height = max_y - min_y

        # target in aspect2d coordinates: full span is 2.0, so fraction -> 2*fraction
        target_dim = 2.0 * fraction

        # avoid division by zero
        if width <= 0 or height <= 0:
            return 0.3

        scale_x = target_dim / width
        scale_y = target_dim / height
        scale = min(scale_x, scale_y)

        # apply a small margin so hex outlines are fully visible
        scale *= 0.92
        return temp_size * scale

    def draw_board(self):
        # Draw each hex and remember its center
        for coord in self.board.keys():
            q, r = coord
            cx, cy = self.hex_to_pixel(q, r)
            # draw hex with full size so adjacent hexes touch (no intentional gap)
            np_hex = self.draw_hex(cx, cy, self.hex_size, thickness=2.5)
            self.hex_nodes[coord] = (np_hex, (cx, cy))

    def on_click(self):
        if not self.mouseWatcherNode.hasMouse():
            return
        m = self.mouseWatcherNode.getMouse()
        mx, my = m.getX(), m.getY()

        coord = self.pixel_to_hex(mx, my)
        if coord not in self.board:
            return
        if self.board[coord] is not None:
            return

        self.board[coord] = self.current
        self.draw_mark(coord, self.current)

        winner = self.check_winner()
        if winner:
            self.status.setText(f"Winner: {winner} — press 'r' to restart")
        elif all(v is not None for v in self.board.values()):
            self.status.setText("Tie — press 'r' to restart")
        else:
            self.current = 'O' if self.current == 'X' else 'X'
            self.status.setText(f"Current: {self.current}")
            # continue play

    def draw_mark(self, coord, mark):
        q, r = coord
        cx, cy = self.hex_nodes[coord][1]

        if mark == 'X':
            ls = LineSegs()
            ls.setThickness(3.0)
            s = self.hex_size * 0.6
            ls.moveTo(cx - s, 0, cy - s)
            ls.drawTo(cx + s, 0, cy + s)
            ls.moveTo(cx - s, 0, cy + s)
            ls.drawTo(cx + s, 0, cy - s)
            node = ls.create()
            np_mark = NodePath(node)
            np_mark.reparentTo(self.grid_node)
            self.marks[coord] = np_mark
        else:
            ls = LineSegs()
            ls.setThickness(3.0)
            segments = 24
            radius = self.hex_size * 0.6
            for i in range(segments + 1):
                a = (i / segments) * (2 * math.pi)
                x = cx + radius * math.cos(a)
                z = cy + radius * math.sin(a)
                if i == 0:
                    ls.moveTo(x, 0, z)
                else:
                    ls.drawTo(x, 0, z)
            node = ls.create()
            np_mark = NodePath(node)
            np_mark.reparentTo(self.grid_node)
            self.marks[coord] = np_mark

    def check_winner(self):
        # directions for axial coords (q,r)
        dirs = [(1, 0), (0, 1), (1, -1)]
        for coord, val in self.board.items():
            if val is None:
                continue
            q, r = coord
            for dq, dr in dirs:
                count = 1
                # forward
                nq, nr = q + dq, r + dr
                while (nq, nr) in self.board and self.board[(nq, nr)] == val:
                    count += 1
                    nq += dq
                    nr += dr
                # backward
                nq, nr = q - dq, r - dr
                while (nq, nr) in self.board and self.board[(nq, nr)] == val:
                    count += 1
                    nq -= dq
                    nr -= dr
                if count >= 3:
                    return val
        return None

    def reset_game(self):
        for k in list(self.marks.keys()):
            self.marks[k].removeNode()
        self.marks = {}
        self.board = {k: None for k in self.board.keys()}
        self.current = 'X'
        self.status.setText(f"Current: {self.current}")

    # (no chess clock in this version)


if __name__ == '__main__':
    app = TicTacToeApp()
    app.run()
