import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

from parsers.qs_parser import load_qs_from_csv
from parsers.the_parser import load_the_from_csv
from parsers.arwu_parser import load_arwu_from_csv
from normalizer import normalize_names
from calculator import calculate_aggregate
from exporter import export_to_excel, export_to_csv

from dotenv import load_dotenv
import os

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE")
BG_COLOR = os.getenv("BG_COLOR")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.configure(bg=BG_COLOR)

        self.qs = None
        self.the = None
        self.arwu = None
        self.result = None

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.sources_tab = ttk.Frame(notebook)
        self.aggregate_tab = ttk.Frame(notebook)
        self.result_tab = ttk.Frame(notebook)

        notebook.add(self.sources_tab, text="Источники")
        notebook.add(self.aggregate_tab, text="Агрегация")
        notebook.add(self.result_tab, text="Итоговый рейтинг")

        self.create_sources_tab()
        self.create_aggregate_tab()
        self.create_result_tab()

    def create_sources_tab(self):
        ttk.Button(
            self.sources_tab,
            text="Загрузить QS",
            command=self.load_qs
        ).pack(pady=5)

        ttk.Button(
            self.sources_tab,
            text="Загрузить THE",
            command=self.load_the
        ).pack(pady=5)

        ttk.Button(
            self.sources_tab,
            text="Загрузить ARWU",
            command=self.load_arwu
        ).pack(pady=5)

    def create_aggregate_tab(self):
        self.w_qs = tk.DoubleVar(value=0.33)
        self.w_the = tk.DoubleVar(value=0.33)
        self.w_arwu = tk.DoubleVar(value=0.34)

        ttk.Label(self.aggregate_tab, text="Вес QS").pack()
        ttk.Scale(self.aggregate_tab, from_=0, to=1,
                  variable=self.w_qs, orient="horizontal").pack()

        ttk.Label(self.aggregate_tab, text="Вес THE").pack()
        ttk.Scale(self.aggregate_tab, from_=0, to=1,
                  variable=self.w_the, orient="horizontal").pack()

        ttk.Label(self.aggregate_tab, text="Вес ARWU").pack()
        ttk.Scale(self.aggregate_tab, from_=0, to=1,
                  variable=self.w_arwu, orient="horizontal").pack()

        ttk.Button(
            self.aggregate_tab,
            text="Рассчитать",
            command=self.calculate
        ).pack(pady=10)

    def create_result_tab(self):
        self.tree = ttk.Treeview(
            self.result_tab,
            columns=("Rank", "University", "QS",
                     "THE", "ARWU", "Final Score"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(fill="both", expand=True)

        ttk.Button(
            self.result_tab,
            text="Построить график",
            command=self.plot
        ).pack(pady=5)

        ttk.Button(
            self.result_tab,
            text="Сохранить в Excel",
            command=self.save_excel
        ).pack(pady=5)

        ttk.Button(
            self.result_tab,
            text="Сохранить в CSV",
            command=self.save_csv
        ).pack(pady=5)

    def load_qs(self):
        path = filedialog.askopenfilename()
        if path:
            self.qs = normalize_names(load_qs_from_csv(path))
            messagebox.showinfo("QS", "QS загружен")

    def load_the(self):
        path = filedialog.askopenfilename()
        if path:
            self.the = normalize_names(load_the_from_csv(path))
            messagebox.showinfo("THE", "THE загружен")

    def load_arwu(self):
        path = filedialog.askopenfilename()
        if path:
            self.arwu = normalize_names(load_arwu_from_csv(path))
            messagebox.showinfo("ARWU", "ARWU загружен")

    def calculate(self):
        df = self.qs.merge(self.the, on="University", how="outer")
        df = df.merge(self.arwu, on="University", how="outer")

        self.result = calculate_aggregate(
            df,
            self.w_qs.get(),
            self.w_the.get(),
            self.w_arwu.get()
        )

        if not hasattr(self, "tree"):
            messagebox.showerror("Ошибка", "Таблица не создана")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in self.result.iterrows():
            self.tree.insert("", "end", values=list(row))

    def plot(self):
        if self.result is None:
            return

        top20 = self.result.head(20)
        plt.figure(figsize=(10, 6))
        plt.barh(top20["University"], top20["Final Score"])
        plt.gca().invert_yaxis()
        plt.show()

    def save_excel(self):
        if self.result is None:
            messagebox.showerror(
                "Ошибка",
                "Сначала рассчитайте рейтинг!"
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if path:
            try:
                export_to_excel(self.result, path)
                messagebox.showinfo(
                    "Успех",
                    "Файл успешно сохранён!"
                )
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", str(e))

    def save_csv(self):
        if self.result is None:
            messagebox.showerror(
                "Ошибка",
                "Сначала рассчитайте рейтинг!"
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if path:
            try:
                export_to_csv(self.result, path)
                messagebox.showinfo(
                    "Успех",
                    "Файл успешно сохранён!"
                )
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", str(e))


def run_app():
    root = tk.Tk()
    app = App(root)
    root.mainloop()