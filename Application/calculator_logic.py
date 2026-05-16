# -*- coding: utf-8 -*-
"""
calculator_logic.py
Logic backend for the Educational Scientific Calculator.
@author: abdul
"""
# this code was done by abdulaziz
# This file handles all maths operations and expression parsing.
# It has no GUI code — it is imported and used by calculator_gui.py.
import math  # Provides sqrt, sin, cos, tan, asin, acos, atan


class CalculatorLogic:
    """
    Handles all calculation logic for the calculator.
    Keeps maths completely separate from the GUI layer.
    """

    def calculate(self, expression: str) -> str:
        """
        Takes the expression string built by the GUI (e.g. "sin(45)+√(9)")
        and evaluates it, returning the result as a string.
        If the expression is invalid, returns a descriptive error string
        instead of raising an exception, so the GUI can display it safely.
        """
        try:
            # --- Symbol translation ---
            # The GUI uses display-friendly symbols (√, x², sin, etc.).
            # Python's eval() cannot understand these directly, so we replace
            # them with their Python/math-module equivalents before evaluating.
            expr = expression
            expr = expr.replace("π", "math.pi")      # Replace pi symbol with math.pi
            expr = expr.replace("√(", "math.sqrt(")    # square root
            expr = expr.replace("x²", "**2")            # square (power of 2)
            # asin/acos/atan must be replaced BEFORE sin/cos/tan
            # to avoid partial replacements (e.g. "asin" becoming "amath.sin")
            # Replace inverse trig first using unique placeholders to avoid
            # partial matches — e.g. asin( must not get caught by the sin( replace
            expr = expr.replace("asin(", "[[ASIN]](")
            expr = expr.replace("acos(", "[[ACOS]](")
            expr = expr.replace("atan(", "[[ATAN]](")
            expr = expr.replace("sin(",  "math.sin(")   # sine
            expr = expr.replace("cos(",  "math.cos(")   # cosine
            expr = expr.replace("tan(",  "math.tan(")   # tangent
            # Now safely swap placeholders to their final math equivalents
            expr = expr.replace("[[ASIN]](", "math.asin(")  # inverse sine
            expr = expr.replace("[[ACOS]](", "math.acos(")  # inverse cosine
            expr = expr.replace("[[ATAN]](", "math.atan(")  # inverse tangent

            # --- Safe evaluation ---
            # eval() is used here with a restricted namespace:
            # - "__builtins__": {} removes access to all built-in functions
            #   (e.g. open, exec) so users cannot run harmful code.
            # - {"math": math} allows only the math module to be used.
            result = eval(expr, {"__builtins__": {}}, {"math": math})

            # --- Result formatting ---
            # If the result is a float with no decimal part (e.g. 4.0),
            # display it as an integer (4) to keep the output clean.
            if isinstance(result, float):
                if result == int(result):
                    return str(int(result))
                return f"{result:.10g}"  # up to 10 significant figures
            return str(result)

        except ZeroDivisionError:
            # Caught separately to give a clearer message than a generic error
            return "Error: Divide by 0"
        except ValueError as e:
            # Raised by math functions for invalid inputs, e.g. sqrt(-1), asin(2)
            return f"Error: {e}"
        except Exception:
            # Catch-all for malformed expressions (e.g. "5++3", unclosed brackets)
            return "Error: Invalid input"

    def append_token(self, expression: str, value: str) -> str:
        """
        Called each time a button is pressed (except C and =).
        Appends the correct token to the current expression string.

        For function buttons (sin, cos, √, etc.) an opening bracket is added
        automatically so the user does not have to type it manually.
        For all other buttons (numbers, operators) the value is appended as-is.

        Returns the updated expression string.
        """
        # Map each function button label to the token that should be appended.
        # Functions need an opening bracket so the user can type the argument next.
        func_tokens = {
            "√":    "√(",    # e.g. pressing √ gives "√(" ready for the number
            "sin":  "sin(",
            "cos":  "cos(",
            "tan":  "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "x²":   "x²",   # applied directly after a number, no bracket needed
            "π":    "π",     # pi constant -- replaced with math.pi in calculate()
        }
        # If the value is in the map use its token, otherwise append it directly
        token = func_tokens.get(value, value)

        # Auto-insert * when a number or closing bracket is directly before
        # a function or pi to support expressions like 3π or 2sin(
        if token and expression:
            last = expression[-1]
            if (last.isdigit() or last == ")") and token in ("π", "√(", "sin(", "cos(", "tan(", "asin(", "acos(", "atan("):
                return expression + "*" + token

        return expression + token