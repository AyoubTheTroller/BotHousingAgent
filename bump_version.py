import configparser
import argparse

CHANGELOG_FILE = "CHANGELOG.md"

def bump_version(config_file, part, increment=1, description=None):
    """Bumps the specified version part in the config file.

    Args:
        config_file (str): Path to the setup.cfg file.
        part (str): The version part to bump ("major", "minor", or "patch").
        increment (int, optional): The amount to increment the version part by. Defaults to 1.
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        version_str = config["metadata"]["version"]
        major, minor, patch = map(int, version_str.split("."))

        if part == "major":
            major += increment
            minor = 0
            patch = 0
            header = "#"
        elif part == "minor":
            minor += increment
            patch = 0
            header = "##"
        elif part == "patch":
            patch += increment
            header = "###"
        else:
            raise ValueError(f"Invalid version part: {part}")

        new_version = f"{major}.{minor}.{patch}"
        config["metadata"]["version"] = new_version

        with open(config_file, "w", encoding="utf-8") as configfile:
            config.write(configfile)

        print(f"Version bumped to {new_version}")
    except KeyError:
        print(f"Error: 'version' not found in metadata section of {config_file}")
    except ValueError:
        print(f"Error: Invalid version format in {config_file}")

    # Update changelog
    if description:
        with open(CHANGELOG_FILE, "a", encoding="utf-8") as changelog:
            changelog.write(f"{header} {new_version}\n")
            changelog.write(f"- {description}\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bump the version and update changelog."
    )
    parser.add_argument(
        "part", choices=["major", "minor", "patch"], help="The version part to bump"
    )
    parser.add_argument(
        "-i", "--increment", type=int, default=1, help="Increment amount (default: 1)"
    )
    parser.add_argument(
        "-d", "--description", help="Description of the changes for the changelog"
    )
    parser.add_argument(
        "-f",
        "--file",
        default="setup.cfg",
        help="Path to the setup.cfg file (default: setup.cfg)",
    )
    args = parser.parse_args()

    bump_version(args.file, args.part, args.increment, args.description)
