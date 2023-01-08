from dynaconf import Dynaconf

SETTINGS = Dynaconf(
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,
    env_switcher="ENV_DYNACONF",
)
