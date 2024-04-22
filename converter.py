import argparse
import logging
from src.converter_class import Converter
from src.observer_class import DirectoryObserver
import os


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                    prog='JSON2XML converter',
                    description='Convert JSON fueling files to XML',
                    )
    parser.add_argument('input_folder')
    parser.add_argument('output_folder')
    parser.add_argument('--logfile')
    parser.add_argument('--loglevel', choices=['ERROR', 'INFO', 'DEBUG'])
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    match args.loglevel:
        case 'ERROR':
            level = logging.ERROR
        case 'INFO':
            level = logging.INFO
        case 'DEBUG':
            level = logging.DEBUG
        case _:
            level = logging.INFO

    logging.basicConfig(filename=args.logfile,
                        encoding='utf-8',
                        level=level)

    converter = Converter(args.input_folder, args.output_folder)
    converter.convert_all()

    observer = DirectoryObserver(converter.src_folder)
    observer.start_observing(
        lambda x: converter.convert_file(os.path.basename(x.src_path))
    )

    while True:
        try:
            pass
        except KeyboardInterrupt:
            converter.stop_observing()


if __name__ == '__main__':
    main()
