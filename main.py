from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# Настройка цвета фона окна (светло-серый, чтобы холст выделялся)
Window.clearcolor = get_color_from_hex('#F0F0F0')

class CanvasWidget(Widget):
    """Область для рисования"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brush_color = (0, 0, 0, 1)  # Черный по умолчанию
        self.brush_size = 2
        
        # Рисуем белый фон для холста
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        # Проверяем, что нажатие произошло в пределах холста, а не на панели
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.brush_color)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.brush_size)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

class NeonPaintApp(App):
    def build(self):
        # Корневой контейнер
        root = BoxLayout(orientation='vertical')

        # --- Панель инструментов ---
        # Цвет Sky Blue: #87CEEB
        toolbar = BoxLayout(size_hint_y=0.15, padding=10, spacing=10)
        with toolbar.canvas.before:
            Color(*get_color_from_hex('#87CEEB'))
            self.rect_bar = Rectangle(size=toolbar.size, pos=toolbar.pos)
        toolbar.bind(size=self._update_toolbar, pos=self._update_toolbar)

        # Заголовок
        title = Label(
            text="[b]Neon Paint [/b]", 
            markup=True, 
            font_size='20sp', 
            color=(1, 1, 1, 1),
            size_hint_x=0.3
        )
        toolbar.add_widget(title)

        # Контейнер для кнопок выбора цвета
        colors_layout = BoxLayout(spacing=5)
        colors = {
            'red': '#FF5252', 'green': '#4CAF50', 
            'blue': '#2196F3', 'yellow': '#FFEB3B', 
            'dark': '#000000'
        }

        for emoji, hex_val in colors.items():
            btn = Button(text=emoji, background_normal='', background_color=get_color_from_hex(hex_val))
            btn.bind(on_release=lambda instance, c=hex_val: self.set_color(c))
            colors_layout.add_widget(btn)
        
        toolbar.add_widget(colors_layout)

        # Кнопка Ластика 
        eraser_btn = Button(
            text="Eraser", 
            size_hint_x=0.2,
            background_color=get_color_from_hex('#E0E0E0')
        )
        eraser_btn.bind(on_release=self.set_eraser)
        toolbar.add_widget(eraser_btn)

        # Кнопка Очистки
        clear_btn = Button(
            text="Clear", 
            size_hint_x=0.15,
            background_color=get_color_from_hex('#FFCDD2')
        )
        clear_btn.bind(on_release=self.clear_canvas)
        toolbar.add_widget(clear_btn)

        # --- Холст ---
        self.painter = CanvasWidget()

        root.add_widget(toolbar)
        root.add_widget(self.painter)
        return root

    def _update_toolbar(self, instance, value):
        self.rect_bar.pos = instance.pos
        self.rect_bar.size = instance.size

    def set_color(self, hex_val):
        self.painter.brush_color = get_color_from_hex(hex_val)
        self.painter.brush_size = 2

    def set_eraser(self, instance):
        # Белый цвет кисти и увеличенный размер для удобства стирания
        self.painter.brush_color = (1, 1, 1, 1)
        self.painter.brush_size = 15

    def clear_canvas(self, instance):
        self.painter.canvas.clear()
        # После очистки нужно вернуть белый фон
        with self.painter.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(size=self.painter.size, pos=self.painter.pos)

if __name__ == '__main__':
    NeonPaintApp().run()