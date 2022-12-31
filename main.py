"""
Main Module of the interpreter/compiler.

This orchestrates the entire project.
"""
import argparse


def main() -> None:
    """
    Parse the arguments and accordingly start up the interpretation or compilation process.

    :return:
    """
    args = argparse.ArgumentParser("--compile")
    args.add_argument("--interpret")
    args.add_argument("FILE", type=argparse.FileType("r"))
    arguments = args.parse_args()
    print(arguments)


if __name__ == "__main__":
    main()
