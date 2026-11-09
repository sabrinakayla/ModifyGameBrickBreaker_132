import tkinter as tk
import random

class Ball:
    def __init__(self, canvas, paddle, bricks, color):
        self.canvas = canvas
        self.paddle = paddle
        self.bricks = bricks
        self.color = color
        self.radius = 10
        self.speed_x = 3
        self.speed_y = -3
        self.hit_bottom = False
        
        self.id = canvas.create_oval(10, 10, 10 + self.radius * 2, 10 + self.radius * 2, fill=self.color, outline="#FFB6C1", width=2, tags='ball')
        self.canvas.move(self.id, 230, 300)

    def draw(self):
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        pos = self.canvas.coords(self.id)
        
        if pos[0] <= 0 or pos[2] >= 500:
            self.speed_x = -self.speed_x
        if pos[1] <= 0:
            self.speed_y = -self.speed_y
        if pos[3] >= 400:
            self.hit_bottom = True

        paddle_pos = self.canvas.coords(self.paddle.id)
        if len(paddle_pos) > 0:
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                    overlap = pos[3] - paddle_pos[1]
                    self.canvas.move(self.id, 0, -overlap - 2)
                    
                    center_paddle = (paddle_pos[0] + paddle_pos[2]) / 2
                    center_ball = (pos[0] + pos[2]) / 2
                    offset = (center_ball - center_paddle) / (self.paddle.width / 2)
                    self.speed_x = offset * 5
                    self.speed_y = -abs(self.speed_y)

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.width = 95
        self.height = 14
        self.id = canvas.create_rectangle(0, 0, self.width, self.height, fill=color, outline="#FFFFFF", width=2)
        self.canvas.move(self.id, 202, 340)
        self.direction = 0
        
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress-Left>", self.turn_left)
        self.canvas.bind("<KeyPress-Right>", self.turn_right)
        self.canvas.bind("<KeyRelease-Left>", self.stop)
        self.canvas.bind("<KeyRelease-Right>", self.stop)

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] + self.direction >= 0 and pos[2] + self.direction <= 500:
            self.canvas.move(self.id, self.direction, 0)

    def turn_left(self, event):
        self.direction = -7

    def turn_right(self, event):
        self.direction = 7

    def stop(self, event):
        self.direction = 0

class Brick:
    def __init__(self, canvas, x, y, color, points):
        self.canvas = canvas
        self.points = points
        
        # Area kotak deteksi tabrakan bola
        self.bbox = [x, y, x + 60, y + 24]
        cx = x + 30
        
        # BENTUK BATA: Hati (Love) Sempurna & Menyatu Mulus
        self.part1 = canvas.create_oval(cx - 30, y, cx, y + 16, fill=color, outline=color, width=1)
        self.part2 = canvas.create_oval(cx, y, cx + 30, y + 16, fill=color, outline=color, width=1)
        triangle_pts = [x + 2, y + 8, x + 58, y + 8, cx, y + 24]
        self.part3 = canvas.create_polygon(triangle_pts, fill=color, outline=color, width=1)
        self.outline_line = canvas.create_line(
            x + 15, y + 2, x + 2, y + 8, x + 2, y + 12, cx, y + 24, 
            x + 58, y + 12, x + 58, y + 8, x + 45, y + 2, 
            smooth=False, fill="#FFFFFF", width=1.5
        )

    def delete(self):
        self.canvas.delete(self.part1)
        self.canvas.delete(self.part2)
        self.canvas.delete(self.part3)
        self.canvas.delete(self.outline_line)

class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ModifyGameBrickBreaker_XYZ") # Jangan lupa ganti XYZ dengan 3 digit NIM terakhir Anda
        self.root.configure(bg="#FFC0CB")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=500, height=400, bg="#FFF0F5", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.root.update()
        
        self.score = 0
        self.lives = 3
        self.running = False
        self.fireworks = []
        
        self.score_text = self.canvas.create_text(75, 25, text=f"💖 Score: {self.score}", fill="#DB7093", font=("Arial", 11, "bold"))
        self.lives_text = self.canvas.create_text(425, 25, text=f"🎀 Lives: {self.lives}", fill="#DB7093", font=("Arial", 11, "bold"))
        
        self.btn_start = tk.Button(root, text="💖 Mulai Game 💖", font=("Arial", 11, "bold"), bg="#FFB6C1", fg="#708090", activebackground="#FFC0CB", relief="raised", bd=3, command=self.start_game)
        self.btn_start.pack(pady=10)

    def setup_level(self):
        self.paddle = Paddle(self.canvas, "#FFB6C1")
        self.bricks = []
        
        colors = ["#FFB6C1", "#FFDAB9", "#FFFACD", "#E6E6FA"]
        points_map = [40, 30, 20, 10]
        
        for row in range(4):
            for col in range(6):
                x = 28 + col * 74
                y = 50 + row * 28
                brick = Brick(self.canvas, x, y, colors[row], points_map[row])
                self.bricks.append(brick)
                
        self.ball = Ball(self.canvas, self.paddle, self.bricks, "#FFFFFF")

    def start_game(self):
        if not self.running:
            self.btn_start.pack_forget()
            self.setup_level()
            self.running = True
            self.game_loop()

    def trigger_fireworks(self):
        colors_fw = ["#FFB6C1", "#FFDAB9", "#FFFACD", "#E0FFFF", "#FF69B4", "#BA55D3"]
        for _ in range(45):
            px = random.randint(150, 350)
            py = random.randint(120, 280)
            p_color = random.choice(colors_fw)
            p_id = self.canvas.create_oval(px, py, px + 7, py + 7, fill=p_color, outline="")
            vx = random.uniform(-3.5, 3.5)
            vy = random.uniform(-3.5, 3.5)
            self.fireworks.append((p_id, vx, vy))
        
        self.animate_fireworks()

    def animate_fireworks(self):
        if not self.running:
            for item in self.fireworks:
                p_id, vx, vy = item
                self.canvas.move(p_id, vx, vy)
            self.root.after(30, self.animate_fireworks)

    def game_loop(self):
        if self.running:
            self.paddle.draw()
            self.ball.draw()
            
            ball_pos = self.canvas.coords(self.ball.id)
            for brick in self.bricks[:]:
                brick_pos = brick.bbox
                if ball_pos[2] >= brick_pos[0] and ball_pos[0] <= brick_pos[2]:
                    if ball_pos[3] >= brick_pos[1] and ball_pos[3] <= brick_pos[3]:
                        brick.delete()
                        self.bricks.remove(brick)
                        self.score += brick.points
                        self.canvas.itemconfig(self.score_text, text=f"💖 Score: {self.score}")
                        self.ball.speed_y = -self.ball.speed_y
                            
            if len(self.bricks) == 0:
                self.running = False
                self.canvas.create_text(250, 190, text="✨ YAY! YOU WIN! ✨", fill="#DB7093", font=("Arial", 20, "bold"))
                self.trigger_fireworks()
                return

            if self.ball.hit_bottom:
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"🎀 Lives: {self.lives}")
                self.canvas.delete(self.ball.id)
                self.canvas.delete(self.paddle.id)
                
                if self.lives > 0:
                    self.paddle = Paddle(self.canvas, "#FFB6C1")
                    self.ball = Ball(self.canvas, self.paddle, self.bricks, "#FFFFFF")
                else:
                    self.running = False
                    self.canvas.create_text(250, 200, text="🥺 GAME OVER 🥺", fill="#DB7093", font=("Arial", 22, "bold"))
                    return

            self.root.after(10, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreakerGame(root)
    root.mainloop()