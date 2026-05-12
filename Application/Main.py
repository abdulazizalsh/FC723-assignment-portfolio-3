# -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:10:28 2026

@author: ROG / zizhao dong
"""
#This code is made by my partner zizhao.
import tkinter as tk
from tkinter import messagebox
import math


class EducationalCalculator:

    def __init__(self, root):

        self.root = root
        self.root.title("FC723 Portfolio Project 3: Educational Calculator")
        self.root.geometry("400x600")

        self.expression = ""

        self.result_var = tk.StringVar()

        self.display = tk.Entry(
            root,
            textvariable=self.result_var,
            font=("Arial", 24),
            borderwidth=5,
            relief="flat",
            justify='right',
            bg="#f4f4f4"
        )

        self.display.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="nsew",
            padx=10,
            pady=20
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = EducationalCalculator(root)

    root.mainloop()