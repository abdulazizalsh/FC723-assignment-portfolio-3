# -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:17:45 2026

@author: abdul
"""
# this code was done by me (abdulaziz)

import tkinter as tk


class EducationalCalculator:

    def __init__(self, root):

        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("470x500")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        self.result_var = tk.StringVar()

        self.display = tk.Entry(
            root,
            textvariable=self.result_var,
            font=("Arial", 28),
            bg="#1E1E1E",
            fg="white",
            bd=0,
            insertbackground="white",
            justify="right"
        )

        self.display.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=15,
            pady=20,
            ipady=20,
            sticky="nsew"
        )

        self.create_buttons()

    def create_buttons(self):

        buttons = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "√"],
            ["1", "2", "3", "-", "x²"],
            ["0", ".", "=", "+", "sin"],
            ["cos", "tan", "asin", "acos", "atan"]
        ]

        for row_index, row in enumerate(buttons, start=1):

            for column_index, button_text in enumerate(row):

                button = tk.Button(
                    self.root,
                    text=button_text,
                    font=("Arial", 16, "bold"),
                    width=6,
                    height=2,
                    bg="#2D2D2D",
                    fg="white",
                    activebackground="#505050",
                    activeforeground="white",
                    bd=0
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )


if __name__ == "__main__":

    root = tk.Tk()

    app = EducationalCalculator(root)

    root.mainloop()