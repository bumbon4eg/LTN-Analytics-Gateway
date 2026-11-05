import tkinter as tk


class LabelComponents:
    def _label(
        self,
        parent: tk.Misc,
        text: str,
        *,
        size: int = 10,
        color: str | None = None,
        weight: str = "normal",
        **options: object,
    ) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg=options.pop("bg", self.SURFACE),
            fg=color or self.INK,
            font=(self.FONT, size, weight),
            anchor=options.pop("anchor", "w"),
            **options,
        )
