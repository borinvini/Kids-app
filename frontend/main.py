from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex

# Configurar tamanho inicial (simulando um smartphone)
Window.size = (360, 640)

# Define o estilo da aplicação usando o Kivy Language
Builder.load_string('''
<RoundedImage>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height/2,]
    
<TaskItem>:
    canvas.before:
        Color:
            rgba: 0.95, 0.5, 0.5, 1 if not root.is_complete else 0.5, 0.9, 0.5, 1  # Vermelho se não concluído, verde se concluído
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
    
    orientation: 'horizontal'
    padding: dp(8)
    spacing: dp(8)
    height: dp(55)
    size_hint_y: None
    
    CheckBox:
        id: checkbox
        size_hint_x: None
        width: dp(32)
        on_active: root.mark_complete(self.active)
        active: root.is_complete
    
    BoxLayout:
        orientation: 'vertical'
        padding: [0, dp(5)]
        
        Label:
            id: task_label
            text: root.task_text
            font_size: sp(14)
            text_size: self.width, None
            halign: 'left'
            valign: 'middle'
            color: 0.3, 0.3, 0.3, 1
            
        Label:
            id: description
            text: root.description_text
            font_size: sp(11)
            text_size: self.width, None
            halign: 'left'
            valign: 'top'
            color: 0.5, 0.5, 0.5, 1
            
    Label:
        id: money
        text: root.money_text
        size_hint_x: None
        width: dp(45)
        font_size: sp(13)
        color: 0.1, 0.6, 0.1, 1

<SectionHeader>:
    canvas.before:
        Color:
            rgba: root.section_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5,]
    
    size_hint_y: None
    height: dp(32)
    padding: [dp(12), 0]
    
    Label:
        text: root.title
        font_size: sp(16)
        bold: True
        halign: 'left'
        valign: 'middle'
        text_size: self.width, None
        color: 0.3, 0.3, 0.3, 1
''')

# Classe para imagem arredondada (foto de perfil)
class RoundedImage(Image):
    pass

# Classe para checkbox personalizado
class CheckBox(ButtonBehavior, BoxLayout):
    active = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(CheckBox, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(active=self.update_canvas)
        Clock.schedule_once(self.update_canvas, 0)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.active:
                # Checked
                Color(0.2, 0.7, 0.3, 1)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height/2,])
                Color(1, 1, 1, 1)
                # Draw checkmark
                center_x = self.pos[0] + self.size[0]/2
                center_y = self.pos[1] + self.size[1]/2
            else:
                # Unchecked
                Color(0.9, 0.9, 0.9, 1)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height/2,])
                Color(0.7, 0.7, 0.7, 1)
            
            # Border
            line_width = 1.5
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height/2,])
                
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return super(CheckBox, self).on_touch_down(touch)

# Classe para item de tarefa
class TaskItem(BoxLayout):
    task_text = StringProperty('')
    description_text = StringProperty('')
    money_text = StringProperty('')
    is_complete = BooleanProperty(False)
    
    def __init__(self, task_text, description_text, money, is_complete=False, **kwargs):
        super(TaskItem, self).__init__(**kwargs)
        self.task_text = task_text
        self.description_text = description_text
        self.money_text = f"R$ {money:.2f}".replace('.', ',')
        self.is_complete = is_complete
    
    def mark_complete(self, is_active):
        self.is_complete = is_active
        # Aqui você poderia implementar uma lógica para mover o item entre as seções

# Classe para o cabeçalho de seção
class SectionHeader(BoxLayout):
    title = StringProperty('')
    section_color = ListProperty([0.9, 0.9, 0.9, 1])  # Cor padrão cinza
    
    def __init__(self, title, is_completed=False, **kwargs):
        super(SectionHeader, self).__init__(**kwargs)
        self.title = title
        # Azul para pendentes, verde para concluídas
        self.section_color = [0.4, 0.6, 0.9, 1] if not is_completed else [0.4, 0.8, 0.4, 1]
        
# Classe principal da aplicação
class KidTasksApp(App):
    def build(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header com perfil e nível
        header = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(80),
            padding=[dp(15), dp(10)],
            spacing=dp(10)
        )
        
        # Adiciona gradiente de cores ao header
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)  # Azul bonito
            header_rect = RoundedRectangle(pos=header.pos, size=header.size, radius=[0, 0, 0, 0])
            header.bind(pos=lambda obj, pos: setattr(header_rect, 'pos', pos))
            header.bind(size=lambda obj, size: setattr(header_rect, 'size', size))
        
        # Botão de perfil com foto
        profile_btn = Button(
            background_color=(0,0,0,0),
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )
        
        # Imagem de perfil arredondada
        profile_image = RoundedImage(
            source='atlas://data/images/defaulttheme/filechooser_selected',  # Use uma imagem real aqui
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )
        profile_btn.add_widget(profile_image)
        
        # Informações do usuário (nome e nível)
        user_info = BoxLayout(orientation='vertical', padding=[dp(10), 0])
        
        name_label = Label(
            text='Maria',
            font_size=sp(18),
            halign='left',
            valign='bottom',
            color=(1, 1, 1, 1),
            text_size=(None, None),
            size_hint_y=0.6
        )
        
        level_box = BoxLayout(
            orientation='horizontal', 
            size_hint_y=0.4,
            spacing=dp(5)
        )
        
        level_label = Label(
            text='Nível:',
            font_size=sp(14),
            color=(1, 1, 1, 0.9),
            halign='left',
            valign='top',
            size_hint_x=None,
            width=dp(40)
        )
        
        level_value = Label(
            text='5',
            font_size=sp(14),
            color=(1, 1, 1, 1),
            halign='left',
            valign='top',
            bold=True
        )
        
        level_box.add_widget(level_label)
        level_box.add_widget(level_value)
        
        user_info.add_widget(name_label)
        user_info.add_widget(level_box)
        
        # Adiciona widgets ao header
        header.add_widget(profile_btn)
        header.add_widget(user_info)
        
        # Título da página
        title_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            padding=[dp(20), dp(10)]
        )
        
        title_label = Label(
            text='Minhas Tarefas de Hoje',
            font_size=sp(20),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            valign='middle',
            text_size=(Window.width - dp(40), None)
        )
        
        title_box.add_widget(title_label)
        
        # Container de tarefas com rolagem
        scroll_view = ScrollView()
        
        tasks_container = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None
        )
        
        # Define a altura do container para permitir rolagem
        tasks_container.bind(minimum_height=tasks_container.setter('height'))
        
        # Lista de tarefas demonstrativa
        tasks = [
            {
                'task': 'Arrumar a cama',
                'description': 'Antes de sair para a escola',
                'money': 2.50,
                'completed': False
            },
            {
                'task': 'Guardar os brinquedos',
                'description': 'Manter o quarto organizado',
                'money': 3.00,
                'completed': False
            },
            {
                'task': 'Ajudar com a louça',
                'description': 'Após o almoço',
                'money': 5.00,
                'completed': False
            },
            {
                'task': 'Escovar os dentes',
                'description': 'Antes de dormir',
                'money': 1.50,
                'completed': True
            },
            {
                'task': 'Fazer a lição de casa',
                'description': 'Matemática e português',
                'money': 8.00,
                'completed': False
            },
            {
                'task': 'Alimentar o cachorro',
                'description': 'De manhã e à noite',
                'money': 2.00,
                'completed': True
            },
            {
                'task': 'Separar roupas sujas',
                'description': 'Colocar no cesto',
                'money': 1.00,
                'completed': True
            }
        ]
        
        # Separa as tarefas em pendentes e concluídas
        pending_tasks = [task for task in tasks if not task['completed']]
        completed_tasks = [task for task in tasks if task['completed']]
        
        # Adiciona cabeçalho e tarefas pendentes
        if pending_tasks:
            tasks_container.add_widget(SectionHeader(title='Tarefas Pendentes', is_completed=False))
            for task in pending_tasks:
                task_item = TaskItem(
                    task_text=task['task'],
                    description_text=task['description'],
                    money=task['money'],
                    is_complete=False
                )
                tasks_container.add_widget(task_item)
        
        # Adiciona espaçador entre seções
        spacer = BoxLayout(size_hint_y=None, height=dp(10))
        tasks_container.add_widget(spacer)
        
        # Adiciona cabeçalho e tarefas concluídas
        if completed_tasks:
            tasks_container.add_widget(SectionHeader(title='Tarefas Concluídas', is_completed=True))
            for task in completed_tasks:
                task_item = TaskItem(
                    task_text=task['task'],
                    description_text=task['description'],
                    money=task['money'],
                    is_complete=True
                )
                tasks_container.add_widget(task_item)
        
        # Monta a hierarquia de widgets
        scroll_view.add_widget(tasks_container)
        
        main_layout.add_widget(header)
        main_layout.add_widget(title_box)
        main_layout.add_widget(scroll_view)
        
        return main_layout

if __name__ == '__main__':
    KidTasksApp().run()