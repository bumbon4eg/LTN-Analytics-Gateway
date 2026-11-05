import tkinter as tk
from tkinter import ttk


class SettingsView:
    def show_settings(self) -> None:
        self._clear_window()
        self.root.configure(bg=self.BACKGROUND)

        shell = tk.Frame(self.root, bg=self.BACKGROUND)
        shell.pack(fill="both", expand=True, padx=38, pady=24)
        header = tk.Frame(shell, bg=self.BACKGROUND)
        header.pack(fill="x", pady=(0, 18))
        titles = tk.Frame(header, bg=self.BACKGROUND)
        titles.pack(side="left")
        self._label(titles, "Настройки", size=22, weight="bold", bg=self.BACKGROUND).pack(
            anchor="w"
        )
        self._label(
            titles,
            "Источник данных и параметры PostgreSQL",
            size=10,
            color=self.MUTED,
            bg=self.BACKGROUND,
        ).pack(anchor="w", pady=(4, 0))
        self._button(header, "Отмена", self.show_dashboard).pack(side="right", anchor="n")

        form = tk.Frame(
            shell,
            bg=self.SURFACE,
            highlightthickness=1,
            highlightbackground=self.LINE,
        )
        form.pack(fill="both", expand=True)
        body = tk.Frame(form, bg=self.SURFACE)
        body.pack(fill="both", expand=True, padx=26, pady=20)

        self._label(body, "ИСТОЧНИК JSONL", size=9, color=self.MUTED, weight="bold").pack(
            anchor="w", pady=(0, 7)
        )
        source_row = tk.Frame(body, bg=self.SURFACE)
        source_row.pack(fill="x", pady=(0, 18))
        source_entry = self._text_entry(
            source_row,
            self.source_var,
            font=(self.FONT, 10),
        )
        source_entry.pack(side="left", fill="x", expand=True, ipady=9)
        self._button(source_row, "Обзор…", self._browse_source).pack(side="left", padx=(9, 0))

        self._label(body, "POSTGRESQL", size=9, color=self.MUTED, weight="bold").pack(
            anchor="w", pady=(0, 10)
        )
        grid = tk.Frame(body, bg=self.SURFACE)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=3)
        grid.columnconfigure(1, weight=1)
        self._entry(grid, "СЕРВЕР", self.host_var).grid(
            row=0, column=0, sticky="ew", padx=(0, 12), pady=(0, 12)
        )
        self._entry(grid, "ПОРТ", self.port_var).grid(
            row=0, column=1, sticky="ew", pady=(0, 12)
        )
        self._entry(grid, "ИМЯ БАЗЫ", self.database_var).grid(
            row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 12)
        )
        self._entry(grid, "ПОЛЬЗОВАТЕЛЬ", self.user_var).grid(
            row=1, column=1, sticky="ew", pady=(0, 12)
        )
        self._entry(
            grid,
            "ПАРОЛЬ",
            self.password_var,
            show="●",
            reveal_toggle=True,
        ).grid(row=2, column=0, columnspan=2, sticky="ew")
        ttk.Checkbutton(
            body,
            text="Использовать SSL/TLS с проверкой сертификата сервера",
            variable=self.ssl_var,
        ).pack(anchor="w", pady=(14, 0))

        footer = tk.Frame(shell, bg=self.BACKGROUND)
        footer.pack(fill="x", pady=(14, 0))
        self.settings_status = self._label(
            footer,
            "",
            size=9,
            color=self.MUTED,
            bg=self.BACKGROUND,
            wraplength=520,
        )
        self.settings_status.pack(side="left", fill="x", expand=True)
        save_button = self._button(
            footer,
            "Сохранить настройки",
            self._save_settings_form,
            primary=True,
        )
        save_button.pack(side="right")
        check_button = self._button(
            footer,
            "Проверить подключение",
            self._test_settings_connection,
        )
        check_button.pack(side="right", padx=(0, 8))
        self.busy_buttons.extend((save_button, check_button))
