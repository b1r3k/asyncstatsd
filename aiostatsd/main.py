import argparse


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="your name")
    args = parser.parse_args()
    print("Hello, {}!".format(args.name))


if __name__ == "__main__":
    cli()
