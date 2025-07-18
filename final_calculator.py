from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform
import webbrowser
import math
import random

class MatrixRain(Widget):
    """Матричный дождь на заднем плане"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        self.drops = []
        self.create_drops()
        
    def create_drops(self):
        """Создаем капли матричного дождя"""
        for i in range(25):
            x = random.randint(0, int(Window.width))
            y = random.randint(0, int(Window.height))
            speed = random.uniform(0.5, 2.0)
            length = random.randint(3, 12)
            brightness = random.uniform(0.1, 0.7)
            self.drops.append({
                'x': x, 'y': y, 'speed': speed, 'length': length,
                'brightness': brightness,
                'chars': [random.choice(self.chars) for _ in range(length)]
            })
    
    def update(self, dt):
        """Обновляем позиции капель"""
        for drop in self.drops:
            drop['y'] -= drop['speed']
            if drop['y'] < -100:
                drop['y'] = Window.height + 100
                drop['x'] = random.randint(0, int(Window.width))
                drop['brightness'] = random.uniform(0.1, 0.7)
        self.canvas.clear()
        self.draw()
    
    def draw(self):
        """Отрисовываем матричный дождь"""
        with self.canvas:
            for drop in self.drops:
                for i, char in enumerate(drop['chars']):
                    alpha = (1.0 - (i / len(drop['chars']))) * drop['brightness'] * 0.4
                    Color(0, 1, 0, alpha)
                    Rectangle(
                        pos=(drop['x'], drop['y'] - i * 16),
                        size=(14, 14)
                    )

class CyberpunkButton(Button):
    """Киберпанк кнопка с черным фоном и круглыми углами"""
    
    def __init__(self, text="", color_scheme="cyan", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.color_scheme = color_scheme
        self.background_color = (0, 0, 0, 0)  # Прозрачный фон для кастомной отрисовки
        self.font_size = dp(20)
        self.size_hint = (1, 1)
        
        # Устанавливаем цвет в зависимости от схемы
        if color_scheme == "cyan":
            self.color = (0, 1, 1, 1)
        elif color_scheme == "pink":
            self.color = (1, 0, 1, 1)
        elif color_scheme == "green":
            self.color = (0, 1, 0, 1)
        else:
            self.color = (0, 1, 1, 1)
        
        self.bind(on_press=self.on_button_press)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        """Обновляем отрисовку кнопки"""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.9)  # Черный фон с высокой прозрачностью
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(20),]  # Круглые углы
            )
        
    def on_button_press(self, instance):
        """Анимация нажатия"""
        # Анимация прозрачности
        anim = Animation(opacity=0.6, duration=0.1) + Animation(opacity=1.0, duration=0.2)
        anim.start(self)

class HeaderPanel(BoxLayout):
    """Заголовок приложения с названием и кнопкой телеграм"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(20)
        self.spacing = dp(10)
        
        # Название приложения
        title_label = Label(
            text='CalcuHill',
            color=(0, 1, 1, 1),  # Голубой цвет
            font_size=dp(32),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(title_label)
        
        # Кнопка телеграм
        telegram_btn = CyberpunkButton(
            text='Телеграм разработчика {ТЫК}',
            color_scheme="pink",
            size_hint=(None, None),
            size=(dp(250), dp(40)),
            pos_hint={'center_x': 0.5}
        )
        telegram_btn.bind(on_press=self.open_telegram)
        self.add_widget(telegram_btn)
    
    def open_telegram(self, instance):
        """Открываем телеграм-канал разработчика"""
        webbrowser.open('https://t.me/hillvys')

class CyberpunkDisplay(BoxLayout):
    """Киберпанк дисплей с улучшенным дизайном"""
    
    result_text = StringProperty('0')
    expression_text = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(25)
        self.spacing = dp(15)
        
        # Поле выражения
        self.expression_label = Label(
            text='',
            color=(0.6, 0.6, 0.6, 1),
            font_size=dp(18),
            size_hint_y=None,
            height=dp(35),
            halign='right'
        )
        self.add_widget(self.expression_label)
        
        # Поле результата
        self.result_label = Label(
            text='0',
            color=(0, 1, 1, 1),
            font_size=dp(40),
            size_hint_y=None,
            height=dp(60),
            halign='right',
            bold=True
        )
        self.add_widget(self.result_label)
        
        self.bind(result_text=self.update_result)
        self.bind(expression_text=self.update_expression)
    
    def update_result(self, instance, value):
        """Обновляем результат с анимацией"""
        anim = Animation(opacity=0.7, duration=0.1) + Animation(opacity=1.0, duration=0.1)
        anim.start(self.result_label)
        self.result_label.text = value
    
    def update_expression(self, instance, value):
        """Обновляем выражение"""
        self.expression_label.text = value

class HistoryPanel(BoxLayout):
    """Панель истории вычислений с улучшенным дизайном"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.8
        self.pos_hint = {'right': 1}
        self.background_color = (0.1, 0.1, 0.15, 0.95)
        
        # Заголовок
        title = Label(
            text='История вычислений',
            color=(0, 1, 1, 1),
            font_size=dp(22),
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(title)
        
        # Список истории
        self.history_list = GridLayout(
            cols=1,
            spacing=dp(8),
            size_hint_y=None,
            padding=dp(10)
        )
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.history_list)
        self.add_widget(scroll)
    
    def add_history_item(self, expression, result):
        """Добавляем элемент в историю с анимацией"""
        item = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70))
        
        expr_label = Label(
            text=expression,
            color=(0.8, 0.8, 0.8, 1),
            font_size=dp(16),
            halign='left'
        )
        result_label = Label(
            text=f'= {result}',
            color=(0, 1, 1, 1),
            font_size=dp(18),
            halign='right',
            bold=True
        )
        
        item.add_widget(expr_label)
        item.add_widget(result_label)
        
        # Анимация появления
        item.opacity = 0
        anim = Animation(opacity=1, duration=0.4)
        anim.start(item)
        
        self.history_list.add_widget(item)

class CyberpunkCalculator(BoxLayout):
    """Основной класс киберпанк калькулятора"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.background_color = (0.05, 0.06, 0.09, 1)  # Темный фон
        
        # Матричный дождь
        self.matrix_rain = MatrixRain()
        self.add_widget(self.matrix_rain)
        
        # Основная панель калькулятора
        main_panel = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # Заголовок с названием и телеграм
        header = HeaderPanel()
        main_panel.add_widget(header)
        
        # Дисплей
        self.display = CyberpunkDisplay()
        main_panel.add_widget(self.display)
        
        # Кнопки калькулятора
        self.create_buttons(main_panel)
        
        self.add_widget(main_panel)
        
        # Панель истории
        self.history_panel = HistoryPanel()
        self.add_widget(self.history_panel)
        
        # Переменные калькулятора
        self.current_number = '0'
        self.previous_number = None
        self.operation = None
        self.new_number = True
        self.history = []
        
        # Запускаем анимацию матричного дождя
        Clock.schedule_interval(self.matrix_rain.update, 1.0/30.0)
    
    def create_buttons(self, parent):
        """Создаем кнопки калькулятора с улучшенным дизайном"""
        button_layout = GridLayout(cols=4, spacing=dp(8), padding=dp(15))
        
        # Определяем кнопки с цветовыми схемами
        buttons = [
            ('C', self.clear, "pink"),
            ('±', self.negate, "cyan"),
            ('%', self.percentage, "cyan"),
            ('÷', lambda x: self.set_operation('/'), "green"),
            ('7', lambda x: self.add_number('7'), "cyan"),
            ('8', lambda x: self.add_number('8'), "cyan"),
            ('9', lambda x: self.add_number('9'), "cyan"),
            ('×', lambda x: self.set_operation('*'), "green"),
            ('4', lambda x: self.add_number('4'), "cyan"),
            ('5', lambda x: self.add_number('5'), "cyan"),
            ('6', lambda x: self.add_number('6'), "cyan"),
            ('-', lambda x: self.set_operation('-'), "green"),
            ('1', lambda x: self.add_number('1'), "cyan"),
            ('2', lambda x: self.add_number('2'), "cyan"),
            ('3', lambda x: self.add_number('3'), "cyan"),
            ('+', lambda x: self.set_operation('+'), "green"),
            ('0', lambda x: self.add_number('0'), "cyan"),
            ('.', lambda x: self.add_number('.'), "cyan"),
            ('sin', self.sin, "pink"),
            ('=', self.calculate, "green"),
        ]
        
        for text, callback, color_scheme in buttons:
            btn = CyberpunkButton(text=text, color_scheme=color_scheme)
            btn.bind(on_press=callback)
            button_layout.add_widget(btn)
        
        parent.add_widget(button_layout)
    
    def add_number(self, number):
        """Добавляем цифру"""
        if self.new_number:
            self.current_number = number
            self.new_number = False
        else:
            if number == '.' and '.' not in self.current_number:
                self.current_number += number
            elif number != '.':
                self.current_number += number
        
        self.display.result_text = self.current_number
    
    def clear(self, instance=None):
        """Очищаем калькулятор"""
        self.current_number = '0'
        self.previous_number = None
        self.operation = None
        self.new_number = True
        self.display.result_text = '0'
        self.display.expression_text = ''
    
    def negate(self, instance=None):
        """Меняем знак числа"""
        if self.current_number != '0':
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.display.result_text = self.current_number
    
    def percentage(self, instance=None):
        """Процент от числа"""
        try:
            value = float(self.current_number) / 100
            self.current_number = str(value)
            self.display.result_text = self.current_number
        except ValueError:
            pass
    
    def set_operation(self, op):
        """Устанавливаем операцию"""
        if self.previous_number is not None:
            self.calculate()
        
        self.previous_number = float(self.current_number)
        self.operation = op
        self.new_number = True
        
        # Показываем выражение
        op_symbol = {'+': '+', '-': '-', '*': '×', '/': '÷'}.get(op, op)
        self.display.expression_text = f"{self.previous_number} {op_symbol}"
    
    def calculate(self, instance=None):
        """Выполняем вычисление"""
        if self.previous_number is None or self.operation is None:
            return
        
        try:
            current = float(self.current_number)
            previous = self.previous_number
            op = self.operation
            
            if op == '+':
                result = previous + current
            elif op == '-':
                result = previous - current
            elif op == '*':
                result = previous * current
            elif op == '/':
                if current == 0:
                    self.display.result_text = 'Ошибка'
                    return
                result = previous / current
            
            # Добавляем в историю
            expression = f"{previous} {self.operation} {current}"
            self.history_panel.add_history_item(expression, str(result))
            
            self.current_number = str(result)
            self.display.result_text = self.current_number
            self.display.expression_text = ''
            self.previous_number = None
            self.operation = None
            self.new_number = True
            
        except ValueError:
            self.display.result_text = 'Ошибка'
    
    def sin(self, instance=None):
        """Синус числа"""
        try:
            value = math.sin(math.radians(float(self.current_number)))
            self.current_number = str(value)
            self.display.result_text = self.current_number
        except ValueError:
            pass

class CyberpunkCalculatorApp(App):
    """Главное приложение"""
    
    def build(self):
        """Строим интерфейс"""
        # Устанавливаем разрешение окна 1080x2400
        Window.size = (1080, 2400)
        Window.clearcolor = (0.05, 0.06, 0.09, 1)
        return CyberpunkCalculator()

if __name__ == '__main__':
    CyberpunkCalculatorApp().run() 