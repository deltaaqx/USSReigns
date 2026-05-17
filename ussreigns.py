# ussreigns.py

import json
import random
import tkinter as tk

WINDOW_WIDTH = 520
WINDOW_HEIGHT = 720
BG_COLOR = "#1a1a1a"
CARD_BG = "#2a2a2a"
ACCENT_RED = "#cc0000"
ACCENT_GOLD = "#ffd700"
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#aaaaaa"
BAR_BG = "#333333"
BAR_ECONOMY = "#4caf50"
BAR_ELITES = "#9c27b0"
BAR_PEOPLE = "#2196f3"
BAR_WORLD = "#ff9800"
BAR_ARMY = "#f44336"
BTN_A_COLOR = "#2e7d32"
BTN_B_COLOR = "#1565c0"
BTN_HOVER_A = "#388e3c"
BTN_HOVER_B = "#1976d2"

STAT_NAMES = {
    "economy": "Экономика",
    "elites": "Элиты",
    "people": "Народ",
    "world_order": "Мир",
    "army": "Армия"
}

STAT_COLORS = {
    "economy": BAR_ECONOMY,
    "elites": BAR_ELITES,
    "people": BAR_PEOPLE,
    "world_order": BAR_WORLD,
    "army": BAR_ARMY
}

ENDINGS = {
    "economy_0": "Экономический коллапс! Казна пуста, республики требуют независимости. Страна распадается под грузом долгов и обязательств.",
    "economy_100": "Чрезмерное богатство СССР пугает капиталистические страны. Они объединяются и начинают полномасштабную войну против социалистического лагеря.",
    "elites_0": "Верхи больше не могут управлять. Элиты свергают вас в результате заговора. Партийный переворот положил конец вашему правлению.",
    "elites_100": "Элиты рукоплещут каждому вашему слову, превратившись в послушных подхалимов. Народ видит этот фарс и выходит на улицы. Революция сметает прогнившую верхушку.",
    "people_0": "Народное восстание! Чаша терпения переполнена. Толпы штурмуют Кремль, ваша власть пала под натиском народного гнева.",
    "people_100": "Народ настолько поверил в свои силы, что решает: 'А зачем нам вообще лидер? Мы и сами справимся!' Анархия и хаос охватывают страну.",
    "world_order_0": "ЯДЕРНАЯ ВОЙНА! Дипломатия провалилась. Ракеты взлетают с обеих сторон. Мир погружается в ядерную зиму. Конец цивилизации.",
    "world_order_100": "Вы достигли невозможного — полная разрядка и прочный мир без единого выстрела. Секретная победа! Холодная война окончена миром, а не крахом.",
    "army_0": "Армия развалена. Генералы арестовывают вас за развал обороны страны. Военный переворот.",
    "army_100": "Милитаризация поглотила всё. Военные требуют нанести превентивный удар по США, пока не поздно. Ядерная война неизбежна.",
    "historical_victory": "Вы дошли до конца 1991 года! СССР под вашим руководством прожил всю Холодную войну. История свершилась — Советский Союз прекратил существование, но вы были у руля до самого конца."
}

class GameState:
    def __init__(self):
        self.stats = {
            "economy": 50,
            "elites": 50,
            "people": 50,
            "world_order": 50,
            "army": 50
        }
        self.flags = {"leader_stalin": True}
        self.current_year = 1946
        self.current_leader = "Иосиф Сталин"
        self.event_count = 0
        self.years_passed = 0
        self.game_over = False
        self.ending_text = ""
        self.historical_events = []
        self.neutral_events = []
        self.historical_index = 0
        self.historical_in_year = []
        self.neutral_count = 0
        self.neutral_pool = []
        self.current_event = None

    def load_events(self):
        try:
            with open("historical_events.json", "r", encoding="utf-8") as f:
                self.historical_events = json.load(f)
        except FileNotFoundError:
            self.historical_events = []
        try:
            with open("neutral_events.json", "r", encoding="utf-8") as f:
                self.neutral_events = json.load(f)
        except FileNotFoundError:
            self.neutral_events = []

    def reset(self):
        self.__init__()
        self.load_events()

    def update_leader_name(self):
        if self.flags.get("leader_gorbachev"):
            self.current_leader = "Михаил Горбачёв"
        elif self.flags.get("leader_chernenko"):
            self.current_leader = "Константин Черненко"
        elif self.flags.get("leader_andropov"):
            self.current_leader = "Юрий Андропов"
        elif self.flags.get("leader_brezhnev"):
            self.current_leader = "Леонид Брежнев"
        elif self.flags.get("leader_khrushchev"):
            self.current_leader = "Никита Хрущёв"
        elif self.flags.get("leader_beria"):
            self.current_leader = "Лаврентий Берия"
        elif self.flags.get("leader_stalin_dead"):
            self.current_leader = "Иосиф Сталин (скончался)"
        else:
            self.current_leader = "Иосиф Сталин"

    def get_next_event(self):
        self.update_leader_name()
        if self.game_over:
            return None

        self.historical_in_year = [
            e for e in self.historical_events
            if e["year"] == self.current_year
        ]
        self.historical_in_year.sort(key=lambda e: e["id"])

        if self.historical_index < len(self.historical_in_year):
            event = self.historical_in_year[self.historical_index]
            self.historical_index += 1
            self.current_event = event
            return event

        if not self.neutral_pool:
            self.neutral_count = random.randint(1, 2)
            self.neutral_pool = self.neutral_events[:]
            random.shuffle(self.neutral_pool)

        if self.neutral_count > 0 and self.neutral_pool:
            self.neutral_count -= 1
            event = self.neutral_pool.pop()
            self.current_event = event
            return event

        self.advance_year()
        return self.get_next_event()

    def advance_year(self):
        self.current_year += 1
        self.years_passed += 1
        self.historical_index = 0
        self.neutral_count = 0
        self.neutral_pool = []
        if self.current_year > 1991:
            self.game_over = True
            self.ending_text = ENDINGS["historical_victory"]

    def apply_effects(self, effects):
        for stat, value in effects.items():
            if stat in self.stats:
                self.stats[stat] += value
                if self.stats[stat] < 0:
                    self.stats[stat] = 0
                if self.stats[stat] > 100:
                    self.stats[stat] = 100

    def set_flags(self, flags_dict):
        for flag, value in flags_dict.items():
            if value:
                self.flags[flag] = True
            elif flag in self.flags:
                del self.flags[flag]

    def check_ending(self):
        for stat, value in self.stats.items():
            if value == 0:
                self.game_over = True
                self.ending_text = ENDINGS[f"{stat}_0"]
                return
            if value == 100:
                self.game_over = True
                self.ending_text = ENDINGS[f"{stat}_100"]
                return
        if self.flags.get("game_over_historical"):
            self.game_over = True
            self.ending_text = ENDINGS["historical_victory"]

    def process_choice(self, choice_key):
        if not self.current_event:
            return
        option = self.current_event.get(choice_key)
        if not option:
            return
        flags_require = option.get("flags_require", {})
        for flag, required in flags_require.items():
            if required and not self.flags.get(flag):
                return
        effects = option.get("effects", {})
        self.apply_effects(effects)
        flags_set = option.get("flags_set", {})
        self.set_flags(flags_set)
        self.event_count += 1
        self.check_ending()

class USSReignsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USSReigns")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.game = GameState()
        self.game.load_events()
        self.show_hints = False
        self.last_effects = None

        self.create_widgets()
        self.show_next_event()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.top_frame.pack(fill=tk.X, padx=20, pady=(15, 5))

        self.year_label = tk.Label(
            self.top_frame, text="1946", font=("Arial", 14, "bold"),
            fg=ACCENT_GOLD, bg=BG_COLOR
        )
        self.year_label.pack(side=tk.LEFT)

        self.leader_label = tk.Label(
            self.top_frame, text="Иосиф Сталин", font=("Arial", 11),
            fg=TEXT_GRAY, bg=BG_COLOR
        )
        self.leader_label.pack(side=tk.RIGHT)

        self.bars_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.bars_frame.pack(fill=tk.X, padx=20, pady=5)

        self.bar_widgets = {}
        for stat, name in STAT_NAMES.items():
            row = tk.Frame(self.bars_frame, bg=BG_COLOR)
            row.pack(fill=tk.X, pady=2)
            label = tk.Label(
                row, text=name, font=("Arial", 10),
                fg=TEXT_WHITE, bg=BG_COLOR, width=12, anchor="w"
            )
            label.pack(side=tk.LEFT)
            canvas = tk.Canvas(row, height=16, bg=BAR_BG, highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            value_label = tk.Label(
                row, text="50", font=("Arial", 10),
                fg=TEXT_WHITE, bg=BG_COLOR, width=4, anchor="e"
            )
            value_label.pack(side=tk.RIGHT)
            self.bar_widgets[stat] = {
                "canvas": canvas,
                "label": value_label,
                "bar": None
            }

        separator = tk.Frame(self.root, height=2, bg=ACCENT_RED)
        separator.pack(fill=tk.X, padx=20, pady=10)

        self.card_frame = tk.Frame(
            self.root, bg=CARD_BG,
            highlightbackground=ACCENT_GOLD, highlightthickness=1
        )
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self.event_type_label = tk.Label(
            self.card_frame, text="", font=("Arial", 9, "italic"),
            fg=ACCENT_GOLD, bg=CARD_BG
        )
        self.event_type_label.pack(pady=(10, 5))

        self.event_title_label = tk.Label(
            self.card_frame, text="", font=("Arial", 13, "bold"),
            fg=TEXT_WHITE, bg=CARD_BG, wraplength=440
        )
        self.event_title_label.pack(pady=(0, 5))

        self.event_desc_label = tk.Label(
            self.card_frame, text="", font=("Arial", 10),
            fg=TEXT_GRAY, bg=CARD_BG, wraplength=440, justify=tk.LEFT
        )
        self.event_desc_label.pack(pady=(0, 10), padx=20)

        self.buttons_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        self.btn_a = tk.Button(
            self.buttons_frame, text="", font=("Arial", 11, "bold"),
            bg=BTN_A_COLOR, fg=TEXT_WHITE,
            activebackground=BTN_HOVER_A, activeforeground=TEXT_WHITE,
            relief=tk.FLAT, wraplength=220, height=4,
            command=lambda: self.on_choice("option_a")
        )
        self.btn_a.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_b = tk.Button(
            self.buttons_frame, text="", font=("Arial", 11, "bold"),
            bg=BTN_B_COLOR, fg=TEXT_WHITE,
            activebackground=BTN_HOVER_B, activeforeground=TEXT_WHITE,
            relief=tk.FLAT, wraplength=220, height=4,
            command=lambda: self.on_choice("option_b")
        )
        self.btn_b.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        self.bottom_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.bottom_frame.pack(fill=tk.X, padx=20, pady=(5, 15))

        self.hint_toggle_btn = tk.Button(
            self.bottom_frame, text="Подсказки: OFF", font=("Arial", 9),
            bg="#444444", fg=TEXT_WHITE, relief=tk.FLAT,
            command=self.toggle_hints
        )
        self.hint_toggle_btn.pack(side=tk.LEFT)

        self.stats_label = tk.Label(
            self.bottom_frame, text="Событий: 0", font=("Arial", 9),
            fg=TEXT_GRAY, bg=BG_COLOR
        )
        self.stats_label.pack(side=tk.RIGHT)

    def update_bars(self):
        for stat, value in self.game.stats.items():
            widgets = self.bar_widgets[stat]
            canvas = widgets["canvas"]
            label = widgets["label"]
            canvas.delete("all")
            width = canvas.winfo_width()
            if width < 2:
                width = 200
            fill_width = int(width * value / 100)
            color = STAT_COLORS[stat]
            canvas.create_rectangle(0, 0, fill_width, 16, fill=color, outline="")
            canvas.create_text(
                width // 2, 8, text=str(value),
                fill="white", font=("Arial", 9, "bold")
            )
            label.config(text="")

    def update_info(self):
        self.year_label.config(text=str(self.game.current_year))
        self.leader_label.config(text=self.game.current_leader)
        self.stats_label.config(
            text=f"Событий: {self.game.event_count}"
        )
        self.update_bars()

    def toggle_hints(self):
        self.show_hints = not self.show_hints
        if self.show_hints:
            self.hint_toggle_btn.config(text="Подсказки: ON", bg="#666666")
        else:
            self.hint_toggle_btn.config(text="Подсказки: OFF", bg="#444444")
        if self.game.current_event:
            self.display_event(self.game.current_event)

    def format_effects(self, effects):
        parts = []
        for stat, value in effects.items():
            if value == 0:
                continue
            sign = "+" if value > 0 else ""
            name = STAT_NAMES.get(stat, stat)
            parts.append(f"{name} {sign}{value}")
        return " | ".join(parts) if parts else "Нет эффектов"

    def display_event(self, event):
        self.game.current_event = event
        event_type = event.get("type", "neutral")
        if event_type == "historical":
            self.event_type_label.config(text="[ИСТОРИЧЕСКОЕ] СОБЫТИЕ")
        else:
            self.event_type_label.config(text="СОБЫТИЕ")

        self.event_title_label.config(text=event.get("title", ""))
        self.event_desc_label.config(text=event.get("description", ""))

        option_a = event.get("option_a", {})
        option_b = event.get("option_b", {})

        text_a = option_a.get("text", "Вариант A")
        text_b = option_b.get("text", "Вариант B")

        req_a = option_a.get("flags_require", {})
        req_b = option_b.get("flags_require", {})
        a_locked = False
        b_locked = False
        for flag, required in req_a.items():
            if required and not self.game.flags.get(flag):
                a_locked = True
                break
        for flag, required in req_b.items():
            if required and not self.game.flags.get(flag):
                b_locked = True
                break

        if a_locked:
            self.btn_a.config(
                text=f"[Недоступно]\n{text_a}",
                bg="#4a1515", fg="#cccccc",
                activebackground="#4a1515", activeforeground="#cccccc",
                state=tk.DISABLED
            )
        else:
            self.btn_a.config(
                state=tk.NORMAL,
                bg=BTN_A_COLOR, fg=TEXT_WHITE,
                activebackground=BTN_HOVER_A, activeforeground=TEXT_WHITE
            )
            if self.show_hints:
                eff_a = self.format_effects(option_a.get("effects", {}))
                self.btn_a.config(text=f"{text_a}\n[{eff_a}]")
            else:
                self.btn_a.config(text=text_a)

        if b_locked:
            self.btn_b.config(
                text=f"[Недоступно]\n{text_b}",
                bg="#4a1515", fg="#cccccc",
                activebackground="#4a1515", activeforeground="#cccccc",
                state=tk.DISABLED
            )
        else:
            self.btn_b.config(
                state=tk.NORMAL,
                bg=BTN_B_COLOR, fg=TEXT_WHITE,
                activebackground=BTN_HOVER_B, activeforeground=TEXT_WHITE
            )
            if self.show_hints:
                eff_b = self.format_effects(option_b.get("effects", {}))
                self.btn_b.config(text=f"{text_b}\n[{eff_b}]")
            else:
                self.btn_b.config(text=text_b)

    def show_ending(self):
        self.event_type_label.config(text="")
        self.event_title_label.config(text="КОНЕЦ ИГРЫ", fg=TEXT_WHITE)
        self.event_desc_label.config(text=self.game.ending_text)
        self.btn_a.config(text="Начать заново", state=tk.NORMAL)
        self.btn_a.configure(command=self.restart_game)
        self.btn_b.config(text="Выйти", state=tk.NORMAL)
        self.btn_b.configure(command=self.root.quit)
        self.stats_label.config(
            text=f"Годы: {self.game.years_passed} | Событий: {self.game.event_count}"
        )
        self.update_bars()

    def show_next_event(self):
        if self.game.game_over:
            self.show_ending()
            return
        event = self.game.get_next_event()
        if event is None:
            self.game.game_over = True
            self.game.ending_text = "Нет доступных событий."
            self.show_ending()
            return
        self.display_event(event)
        self.update_info()

    def on_choice(self, choice_key):
        if self.game.game_over:
            return
        event = self.game.current_event
        if not event:
            return
        option = event.get(choice_key, {})
        flags_require = option.get("flags_require", {})
        for flag, required in flags_require.items():
            if required and not self.game.flags.get(flag):
                return

        self.game.process_choice(choice_key)
        self.update_info()
        self.root.after(300, self.after_choice)

    def after_choice(self):
        if self.game.game_over:
            self.show_ending()
        else:
            self.show_next_event()

    def restart_game(self):
        self.game.reset()
        self.last_effects = None
        self.btn_a.configure(command=lambda: self.on_choice("option_a"))
        self.btn_b.configure(command=lambda: self.on_choice("option_b"))
        self.update_info()
        self.show_next_event()

if __name__ == "__main__":
    root = tk.Tk()
    app = USSReignsApp(root)
    root.mainloop()