import argparse


def main(option):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('run_option', choices=['scan', 'detect'])

    args = parser.parse_args()

    main(args.run_option)
