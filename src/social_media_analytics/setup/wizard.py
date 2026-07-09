import logging
import os
import platform
import subprocess
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter import ttk

from social_media_analytics.setup.config_io import ensure_app_directory
from social_media_analytics.setup.config_io import load_env
from social_media_analytics.setup.config_io import load_or_create_config
from social_media_analytics.setup.config_io import save_config
from social_media_analytics.setup.config_io import save_env

from social_media_analytics.constants import LOG_LEVELS

logger = logging.getLogger(__name__)


class SetupWindow:
    def __init__(self):
        self.config = load_or_create_config()
        self.env = load_env()

        self.root = tk.Tk()
        self.root.title(
            "Social Media Analytics Setup",
        )
        self.root.geometry(
            "640x480",
        )
        self.root.resizable(
            False,
            False,
        )

        self.entries = {}

        self.create_widgets()
        self.adjust_window_height()

    def adjust_window_height(self):
        self.root.update_idletasks()

        width = 640
        height = self.root.winfo_reqheight()

        self.root.geometry(
            f"{width}x{height}",
        )

    def open_url(
        self,
        url,
    ):
        try:
            system = platform.system()

            if system == "Windows":
                os.startfile(
                    url,
                )
                return

            if "microsoft" in platform.release().lower():
                subprocess.run(
                    [
                        "cmd.exe",
                        "/c",
                        "start",
                        "",
                        url,
                    ],
                    check=True,
                )
                return

            webbrowser.open(
                url,
            )

            logger.info(
                f"Browser opened: {url}",
            )

        except Exception:
            logger.exception(
                f"Failed to open url: {url}",
            )

    def create_entry(
        self,
        parent,
        label,
        secret=False,
        default_value="",
        link_url=None,
    ):
        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        label_widget = ttk.Label(
            frame,
            text=label,
            width=20,
        )

        label_widget.pack(
            side="left",
        )

        link = tk.Label(
            frame,
            text="Link" if link_url else "",
            fg="blue" if link_url else "black",
            cursor="hand2" if link_url else "arrow",
            width=6,
        )

        if link_url:
            link.bind(
                "<Button-1>",
                lambda event: self.open_url(
                    link_url,
                ),
            )

        link.pack(
            side="left",
            padx=5,
        )

        entry = ttk.Entry(
            frame,
            show="*" if secret else "",
        )

        entry.insert(
            0,
            default_value,
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.entries[label] = entry

    def create_combobox(
        self,
        parent,
        label,
        values,
        default_value="",
    ):
        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        label_widget = ttk.Label(
            frame,
            text=label,
            width=20,
        )

        label_widget.pack(
            side="left",
        )

        link = tk.Label(
            frame,
            text="",
            width=6,
        )

        link.pack(
            side="left",
            padx=5,
        )

        combobox = ttk.Combobox(
            frame,
            values=values,
            state="readonly",
        )

        combobox.set(
            default_value,
        )

        combobox.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.entries[label] = combobox

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Social Media Analytics Configuration",
        )

        title.pack(
            pady=15,
        )

        links = self.config.get(
            "setup",
            {},
        ).get(
            "links",
            {},
        )

        self.create_entry(
            self.root,
            "Instagram Account",
            default_value=self.config["instagram"]["accounts"][0],
        )

        self.create_entry(
            self.root,
            "YouTube Handle",
            default_value=self.config["youtube"]["handles"][0],
        )

        self.create_entry(
            self.root,
            "APIFY API Token",
            secret=True,
            default_value=self.env.get(
                "APIFY_API_TOKEN",
                "",
            ),
            link_url=links.get("apify"),
        )

        self.create_entry(
            self.root,
            "YouTube API Key",
            secret=True,
            default_value=self.env.get(
                "YOUTUBE_API_KEY",
                "",
            ),
            link_url=links.get("youtube_api"),
        )

        self.create_entry(
            self.root,
            "SMTP User",
            default_value=self.env.get(
                "SMTP_USER",
                "",
            ),
        )

        self.create_entry(
            self.root,
            "SMTP Password",
            secret=True,
            default_value=self.env.get(
                "SMTP_PASSWORD",
                "",
            ),
            link_url=links.get("smtp_password"),
        )

        self.create_entry(
            self.root,
            "Mail Recipients",
            default_value=self.env.get(
                "MAIL_RECIPIENTS",
                "",
            ),
        )

        self.create_entry(
            self.root,
            "SMTP Server",
            default_value=self.config["mail"]["smtp_server"],
        )

        self.create_entry(
            self.root,
            "SMTP Port",
            default_value=self.config["mail"]["smtp_port"],
        )

        # self.create_entry(
        #     self.root,
        #     "Log Level",
        #     default_value=self.config["logging"]["level"],
        # )
        self.create_combobox(
            self.root,
            "Log Level",
            LOG_LEVELS,
            self.config["logging"]["level"],
        )

        button = ttk.Button(
            self.root,
            text="Save",
            command=self.save,
        )

        button.pack(
            pady=15,
        )

    def get_value(
        self,
        key,
    ):
        return self.entries[key].get().strip()

    def save(self):
        try:
            ensure_app_directory()

            save_env(
                {
                    "APIFY_API_TOKEN": self.get_value(
                        "APIFY API Token",
                    ),
                    "YOUTUBE_API_KEY": self.get_value(
                        "YouTube API Key",
                    ),
                    "SMTP_USER": self.get_value(
                        "SMTP User",
                    ),
                    "SMTP_PASSWORD": self.get_value(
                        "SMTP Password",
                    ),
                    "MAIL_RECIPIENTS": self.get_value(
                        "Mail Recipients",
                    ),
                },
            )

            self.config["logging"]["level"] = self.get_value(
                "Log Level",
            )

            self.config["instagram"]["accounts"] = [
                self.get_value(
                    "Instagram Account",
                ),
            ]

            self.config["youtube"]["handles"] = [
                self.get_value(
                    "YouTube Handle",
                ),
            ]

            self.config["mail"]["smtp_server"] = self.get_value(
                "SMTP Server",
            )

            self.config["mail"]["smtp_port"] = int(
                self.get_value(
                    "SMTP Port",
                ),
            )

            save_config(
                self.config,
            )

            logger.info(
                "Setup completed",
            )

            messagebox.showinfo(
                "Completed",
                "Configuration saved.",
            )

            self.root.destroy()

        except Exception:
            logger.exception(
                "Setup failed",
            )

            messagebox.showerror(
                "Error",
                "Configuration failed.",
            )

    def run(self):
        self.root.mainloop()


def run_setup():
    logger.info(
        "Setup started",
    )

    window = SetupWindow()
    window.run()

    logger.info(
        "Setup finished",
    )
