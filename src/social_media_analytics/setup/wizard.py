import logging
import os
import platform
import subprocess
import tkinter as tk
import webbrowser

from tkinter import messagebox
from tkinter import ttk

from social_media_analytics.setup.config_io import ensure_app_directory
from social_media_analytics.setup.config_io import save_config
from social_media_analytics.setup.config_io import save_env

logger = logging.getLogger(__name__)


class SetupWindow:
    def __init__(self):
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

        text = ttk.Label(
            frame,
            text=label,
            width=20,
        )

        text.pack(
            side="left",
        )

        if link_url:
            link = tk.Label(
                frame,
                text="Link",
                fg="blue",
                cursor="hand2",
            )

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

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Social Media Analytics Configuration",
        )

        title.pack(
            pady=15,
        )

        self.create_entry(
            self.root,
            "Instagram Account",
            default_value="sanykorea",
        )

        self.create_entry(
            self.root,
            "YouTube Handle",
            default_value="@SANYKorea_1989",
        )

        self.create_entry(
            self.root,
            "APIFY API Token",
            secret=True,
            link_url="https://console.apify.com/account/integrations",
        )

        self.create_entry(
            self.root,
            "YouTube API Key",
            secret=True,
            link_url="https://console.cloud.google.com/apis/credentials",
        )

        self.create_entry(
            self.root,
            "SMTP User",
        )

        self.create_entry(
            self.root,
            "SMTP Password",
            secret=True,
            link_url="https://myaccount.google.com/apppasswords",
        )

        self.create_entry(
            self.root,
            "Mail Recipients",
        )

        self.create_entry(
            self.root,
            "SMTP Server",
            default_value="smtp.gmail.com",
        )

        self.create_entry(
            self.root,
            "SMTP Port",
            default_value="587",
        )

        self.create_entry(
            self.root,
            "Log Level",
            default_value="INFO",
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

            env_values = {
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
            }

            save_env(
                env_values,
            )

            config = {
                "logging": {
                    "level": self.get_value(
                        "Log Level",
                    ),
                    "file": "logs/social_media_analytics.log",
                },
                "instagram": {
                    "accounts": [
                        self.get_value(
                            "Instagram Account",
                        ),
                    ],
                },
                "youtube": {
                    "handles": [
                        self.get_value(
                            "YouTube Handle",
                        ),
                    ],
                },
                "output": {
                    "data_path": "data",
                },
                "mail": {
                    "smtp_server": self.get_value(
                        "SMTP Server",
                    ),
                    "smtp_port": int(
                        self.get_value(
                            "SMTP Port",
                        ),
                    ),
                    "subject": "Social Media Analytics Report",
                },
            }

            save_config(
                config,
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
