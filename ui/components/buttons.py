import tkinter as tk
from collections.abc import Callable


class ButtonComponents:
    def _button(
        self,
        parent: tk.Misc,
        text: str,
        command: Callable[[], None],
        primary: bool = False,
        **options: object,
    ) -> tk.Button:
        background = self.INK if primary else self.SURFACE
        foreground = "#ffffff" if primary else self.INK
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=self.GREEN if primary else "#e9eee7",
            activeforeground="#ffffff" if primary else self.INK,
            disabledforeground="#89938d",
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
            font=(self.FONT, 10, "bold"),
            cursor="hand2",
            **options,
        )
