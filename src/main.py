import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random

Window.clearcolor = (0, 0, 0, 1)

KANJIS = list("雨風火水木金土日月山川田人口目耳手足音楽愛夢空海光影闇声波")

class KanjiDrop:
    def __init__(self, layout):
        self.x = random.uniform(0.01, 0.97)
        self.y = random.uniform(0.8, 1.5)
        self.speed = random.uniform(0.003, 0.009)
        self.char = random.choice(KANJIS)
        self.opacity = random.uniform(0.15, 0.7)
        self.size = random.choice([18, 22, 26])
        self.label = Label(
            text=self.char,
            font_size=self.size,
            color=(0, 1, 0.4, self.opacity),
            pos_hint={"x": self.x, "top": self.y},
            size_hint=(0.05, 0.05),
        )
        layout.add_widget(self.label)

    def update(self):
        self.y -= self.speed
        self.label.pos_hint = {"x": self.x, "top": self.y}
        if random.random() < 0.05:
            self.char = random.choice(KANJIS)
            self.label.text = self.char
        return self.y < -0.05

class QuupScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.drops = []
        for _ in range(40):
            self.drops.append(KanjiDrop(self))

        self.title = Label(
            text="quup",
            font_size=52,
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 0.15),
        )
        self.add_widget(self.title)

        Clock.schedule_interval(self.update, 1/30)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update(self, dt):
        dead = [d for d in self.drops if d.update()]
        for d in dead:
            self.remove_widget(d.label)
            self.drops.remove(d)
            self.drops.append(KanjiDrop(self))

class QuupApp(App):
    def build(self):
        return QuupScreen()

if __name__ == "__main__":
    QuupApp().run()
