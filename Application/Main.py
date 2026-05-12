# -*- coding: utf-8 -*-
"""
calculator_gui.py
GUI for the Educational Scientific Calculator.
@author: ROG / zizhao dong
"""

#This file is responsible only for the visual interface.
#All maths logic is handled by calculator_logic.py, which is imported below.
#Run this file to launch the calculator.

import tkinter as tk
from calculator_logic import CalculatorLogic  # Import the logic backend


class EducationalCalculator:
    """
    Builds and manages the calculator window.
    Holds the display, all buttons, and the history panel.
    """

    def __init__(self, root):
        """
        Sets up the main window and initialises all components.
        Called once when the application starts.
        """
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("470x750")       # Width x Height in pixels
        self.root.configure(bg="black")
        self.root.resizable(False, False)   # Prevent window resizing

        # Stores the current expression as the user builds it (e.g. "3+sin(45)")
        self.expression = ""

        # StringVar links the display Entry widget to a Python variable.
        # Updating result_var automatically updates what is shown on screen.
        self.result_var = tk.StringVar()

        # Create the logic backend — all calculation calls go through this
        self.logic = CalculatorLogic()

        # --- Display Entry widget (read-only, shows expression and result) ---
        self.display = tk.Entry(
            root,
            textvariable=self.result_var,
            font=("Arial", 28),
            bg="#1E1E1E",
            fg="white",
            bd=0,                           # No border
            insertbackground="white",       # Cursor colour (not visible as readonly)
            justify="right",                # Text aligned to the right like a real calc
            state="readonly",               # Blocks keyboard input from the user
            readonlybackground="#1E1E1E"    # Keeps dark bg even in readonly state
        )
        self.display.grid(
            row=0,
            column=0,
            columnspan=5,   # Spans all 5 columns
            padx=15,
            pady=20,
            ipady=20,       # Internal vertical padding to make the display taller
            sticky="nsew"
        )

        # Build the button grid and the history panel below it
        self.create_buttons()
        self.create_history_panel()

    def get_button_colors(self, text):
        """
        Returns the (background, foreground, active background) colour tuple
        for a given button label.
        Numbers and dot use grey; everything else uses amber.
        """
        if text in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}:
            return "#2D2D2D", "white", "#505050"        # grey — numbers & dot
        else:
            return "#4A3000", "#FFB833", "#6A4500"      # amber — all other buttons

    def create_buttons(self):
        """
        Builds the 5x5 grid of calculator buttons.
        Each button calls handle_button_click with its label when pressed.
        """
        # 2D list defining the button layout row by row
        buttons = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "√"],
            ["1", "2", "3", "-", "x²"],
            ["0", ".", "=", "+", "sin"],
            ["cos", "tan", "asin", "acos", "atan"]
        ]

        # Iterate over every button, placing it at the correct grid position
        for row_index, row in enumerate(buttons, start=1):  # start=1 — row 0 is the display
            for column_index, button_text in enumerate(row):
                bg, fg, activebg = self.get_button_colors(button_text)
                button = tk.Button(
                    self.root,
                    text=button_text,
                    font=("Arial", 16, "bold"),
                    width=6,
                    height=2,
                    bg=bg,
                    fg=fg,
                    activebackground=activebg,
                    activeforeground=fg,
                    bd=0,
                    # lambda captures button_text at definition time via default arg
                    command=lambda value=button_text: self.handle_button_click(value)
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def create_history_panel(self):
        """
        Builds the history section below the buttons.
        Includes a 'History' label, a 'Clear' button, and a scrollable listbox
        that shows all previous calculations.
        """
        # --- 'History' section label ---
        history_label = tk.Label(
            self.root,
            text="History",
            font=("Arial", 13, "bold"),
            bg="black",
            fg="#AAAAAA",
            anchor="w"
        )
        history_label.grid(
            row=6,
            column=0,
            columnspan=4,
            padx=15,
            pady=(15, 0),
            sticky="w"
        )

        # --- 'Clear' button — deletes all entries from the history list ---
        clear_btn = tk.Button(
            self.root,
            text="Clear",
            font=("Arial", 11, "bold"),
            bg="#3A0000",
            fg="#FF5555",
            activebackground="#5A0000",
            activeforeground="#FF5555",
            bd=0,
            command=self.clear_history
        )
        clear_btn.grid(
            row=6,
            column=4,
            padx=5,
            pady=(15, 0),
            sticky="nsew"
        )

        # --- Frame to hold the listbox and scrollbar together ---
        frame = tk.Frame(self.root, bg="black")
        frame.grid(
            row=7,
            column=0,
            columnspan=5,
            padx=15,
            pady=(5, 15),
            sticky="nsew"
        )

        # Scrollbar linked to the listbox so long histories can be scrolled
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Listbox displays one history entry per line (newest at the top)
        self.history_box = tk.Listbox(
            frame,
            font=("Arial", 13),
            bg="#1E1E1E",
            fg="#CCCCCC",
            selectbackground="#505050",
            selectforeground="white",
            bd=0,
            height=8,                           # Show 8 lines before scrolling
            yscrollcommand=scrollbar.set        # Connect scrollbar to listbox
        )
        self.history_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_box.yview)

        # Bind double-click so users can reload a past result into the calculator
        self.history_box.bind("<Double-Button-1>", self.load_from_history)

    def add_to_history(self, expression, result):
        """
        Adds a completed calculation to the top of the history listbox.
        Format: "expression  =  result"
        """
        entry = f"{expression}  =  {result}"
        self.history_box.insert(0, entry)  # index 0 inserts at the top (newest first)

    def clear_history(self):
        """Removes all entries from the history listbox."""
        self.history_box.delete(0, tk.END)  # delete from index 0 to the last item

    def load_from_history(self, event):
        """
        Triggered by a double-click on a history entry.
        Extracts the result from the selected entry and loads it into the
        calculator display so the user can continue calculating from it.
        Does nothing if the entry contains an error.
        """
        selection = self.history_box.curselection()  # returns a tuple of selected indices
        if not selection:
            return

        entry = self.history_box.get(selection[0])
        # Entry format is "expression  =  result", so split and take the last part
        result = entry.split("  =  ")[-1].strip()

        # Only load valid results, not error messages
        if not result.startswith("Error"):
            self.expression = result
            self.result_var.set(result)

    def handle_button_click(self, value):
        """
        Central handler called whenever any calculator button is pressed.
        Decides what to do based on which button was clicked.
        """
        if value == "C":
            # Clear button — reset the expression and blank the display
            self.expression = ""
            self.result_var.set("")

        elif value == "=":
            # Equals button — send the expression to the logic backend to evaluate
            if not self.expression:
                return  # Do nothing if there is nothing to evaluate

            result = self.logic.calculate(self.expression)

            # Save to history before overwriting the expression
            self.add_to_history(self.expression, result)

            self.result_var.set(result)

            if not result.startswith("Error"):
                # Allow chaining: use the result as the start of the next expression
                self.expression = result
            else:
                # On error, clear the expression so the user can start fresh
                self.expression = ""

        else:
            # Any other button — append its token to the expression
            # append_token handles adding opening brackets for functions automatically
            self.expression = self.logic.append_token(self.expression, value)
            self.result_var.set(self.expression)


# --- Entry point ---
# Only runs when this file is executed directly, not when imported as a module
if __name__ == "__main__":
    root = tk.Tk()           # Create the main Tkinter window
    app = EducationalCalculator(root)  # Attach the calculator to the window
    root.mainloop()          # Start the event loop (keeps the window open)
