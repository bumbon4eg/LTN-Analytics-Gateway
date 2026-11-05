import tkinter as tk


class InputComponents:
    def _entry(
        self,
        parent: tk.Misc,
        caption: str,
        variable: tk.StringVar,
        *,
        show: str | None = None,
        reveal_toggle: bool = False,
    ) -> tk.Frame:
        frame = tk.Frame(parent, bg=self.SURFACE)
        self._label(frame, caption, size=9, color=self.MUTED, weight="bold").pack(
            anchor="w", pady=(0, 7)
        )
        field_row = tk.Frame(frame, bg=self.SURFACE) if reveal_toggle else frame
        if reveal_toggle:
            field_row.pack(fill="x")

        entry = self._text_entry(field_row, variable, show=show)
        if reveal_toggle:
            entry.pack(side="left", fill="x", expand=True, ipady=10)
            reveal_button: tk.Button

            def toggle_password() -> None:
                if entry.cget("show"):
                    entry.configure(show="")
                    reveal_button.configure(text="Скрыть")
                else:
                    entry.configure(show=show or "●")
                    reveal_button.configure(text="Показать")

            reveal_button = self._button(field_row, "Показать", toggle_password)
            reveal_button.configure(padx=12, pady=8)
            reveal_button.pack(side="right", padx=(8, 0))
        else:
            entry.pack(fill="x", ipady=10)

        return frame

    def _text_entry(
        self,
        parent: tk.Misc,
        variable: tk.StringVar,
        *,
        show: str | None = None,
        **options: object,
    ) -> tk.Entry:
        entry_options = {
            "textvariable": variable,
            "show": show or "",
            "relief": "flat",
            "bg": "#f6f7f6",
            "fg": self.INK,
            "insertbackground": self.INK,
            "font": (self.FONT, 11),
            "highlightthickness": 1,
            "highlightbackground": self.LINE,
            "highlightcolor": self.GREEN,
        }
        entry_options.update(options)
        entry = tk.Entry(parent, **entry_options)
        self._bind_entry_clipboard(entry)
        return entry

    def _bind_entry_clipboard(self, entry: tk.Entry) -> None:
        entry.bind("<Control-KeyPress>", self._entry_control_shortcut)
        entry.bind("<Shift-Insert>", lambda event: self._entry_shortcut(event, "paste"))
        entry.bind("<Control-Insert>", lambda event: self._entry_shortcut(event, "copy"))
        entry.bind("<<Paste>>", lambda event: self._entry_shortcut(event, "paste"))
        entry.bind("<<Copy>>", lambda event: self._entry_shortcut(event, "copy"))
        entry.bind("<<Cut>>", lambda event: self._entry_shortcut(event, "cut"))

        context_menu = tk.Menu(entry, tearoff=False)
        context_menu.add_command(
            label="Вырезать",
            command=lambda: self._entry_clipboard_action(entry, "cut"),
        )
        context_menu.add_command(
            label="Копировать",
            command=lambda: self._entry_clipboard_action(entry, "copy"),
        )
        context_menu.add_command(
            label="Вставить",
            command=lambda: self._entry_clipboard_action(entry, "paste"),
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Выделить всё",
            command=lambda: entry.select_range(0, "end"),
        )

        def show_context_menu(event: tk.Event) -> str:
            entry.focus_set()
            context_menu.tk_popup(event.x_root, event.y_root)
            context_menu.grab_release()
            return "break"

        entry.bind("<Button-3>", show_context_menu)

    @staticmethod
    def _entry_shortcut(event: tk.Event, action: str) -> str:
        widget = event.widget
        if action == "select-all":
            widget.select_range(0, "end")
            widget.icursor("end")
        else:
            InputComponents._entry_clipboard_action(widget, action)
        return "break"

    @staticmethod
    def _entry_control_shortcut(event: tk.Event) -> str | None:
        keysym = event.keysym.lower()
        action_by_keysym = {
            "c": "copy",
            "cyrillic_es": "copy",
            "с": "copy",
            "v": "paste",
            "cyrillic_em": "paste",
            "м": "paste",
            "x": "cut",
            "ч": "cut",
            "a": "select-all",
            "ф": "select-all",
        }
        action_by_keycode = {
            65: "select-all",
            67: "copy",
            86: "paste",
            88: "cut",
        }
        action = action_by_keysym.get(keysym) or action_by_keycode.get(event.keycode)
        if action is None:
            return None
        return InputComponents._entry_shortcut(event, action)

    @staticmethod
    def _entry_clipboard_action(entry: tk.Entry, action: str) -> None:
        try:
            selection_start = entry.index("sel.first")
            selection_end = entry.index("sel.last")
        except tk.TclError:
            selection_start = selection_end = entry.index("insert")

        if action in {"copy", "cut"}:
            if not entry.selection_present():
                return
            selected_text = entry.get()[selection_start:selection_end]
            entry.clipboard_clear()
            entry.clipboard_append(selected_text)
            if action == "cut":
                entry.delete(selection_start, selection_end)
                entry.icursor(selection_start)
            return

        if action == "paste":
            try:
                pasted_text = entry.clipboard_get()
            except tk.TclError:
                return
            entry.delete(selection_start, selection_end)
            entry.insert(selection_start, pasted_text)
            entry.icursor(selection_start + len(pasted_text))
