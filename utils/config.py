from dataclasses import dataclass
from pathlib import Path

import yaml
from psychopy import data
from .phases import Phase1, Phase2, Phase3, Phase4


@dataclass
class Screen:
    id: int
    distance: float
    frames: int = None


@dataclass
class General:
    isDebugMode: bool
    welcomeText: str
    instructionText: str
    isWelcomeScreenEnabled: bool
    isPhaseOneEnabled: bool
    isPhaseTwoEnabled: bool
    isPhaseThreeEnabled: bool
    isPhaseFourEnabled: bool



@dataclass
class Config:
    """Class for keeping track of an item in inventory.

    Example:
    current_config = Conditions(trials=100)
    current_config.trials
    100
    """

    screen: Screen
    general: General
    debug: bool = None
    fullscreen: bool = False
    time_start: str = data.getDateStr(format="%Y-%m-%d--%H-%M-%S")  # ISO 8601 format
    dir_output: str = "../data/participants/"
    participant_id: str = None  # set in import_conditions
    dir_participant: str = None
    filepath_participant: str = None
    phase1: Phase1 = None
    phase2: Phase2 = None
    phase3: Phase3 = None
    phase4: Phase4 = None


def import_config(
    debug: bool,
    file_name: str = r"C:\Users\Haniah\block_tapping_template\experiment\config.yaml",
) -> Config:
    """Import config from yml file and store it as a dataclass."""

    with open(file_name, encoding="utf-8") as file:
        yml = yaml.safe_load(file.read())

        yml["general"] = General(**yml["general"])
        yml["screen"] = Screen(**yml["screen"])
        yml["phase1"] = Phase1(**yml["phase1"])
        yml["phase2"] = Phase2(**yml["phase2"])
        yml["phase3"] = Phase3(**yml["phase3"])
        yml["phase4"] = Phase4(**yml["phase4"])
        config = Config(**yml)

        config.debug = debug

        # Change directory for output to debug mode: Can be added to gitignore
        if config.debug:
            config.dir_output += ".debug/"

        config.participant_id = (
            f"{config.time_start}"
        )
        config.dir_participant = str(
            config.dir_output + config.participant_id + "/"
        )
        config.filepath_participant = (
            config.dir_participant + config.participant_id
        )

        Path(config.dir_participant).mkdir(
            parents=True,
            exist_ok=True,
        )  # Initialize folder: Make sure the folder exists

        # make sure there is not argument form config which is None
        for key, value in config.__dict__.items():
            if value is None:
                raise ValueError(
                    f"Config argument '{key}' is None."
                    "Set it in the config.yml file or check config.py file."
                )

    return config


if __name__ == "__main__":
    import doctest

    doctest.testmod()