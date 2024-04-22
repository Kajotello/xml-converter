import argparse
import logging
from src.converter_class import Converter
from src.observer_class import DirectoryObserver
import os


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                    prog='JSON2XML converter',
                    description='Convert JSON info fueling files to XML',
                    )
    parser.add_argument('input_folder', help='folder with input files in JSON format')
    parser.add_argument('output_folder', help='folder in which files after conversion will be saved')
    parser.add_argument('--logfile', help='file in which logs will be saved', default='logs.txt')
    parser.add_argument('--loglevel', choices=['ERROR', 'INFO', 'DEBUG'], help='level of logging information')
    parser.add_argument('-o', '--once', action='store_true', help='run program only once an do not enter infinite loop')
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
    logging.getLogger('watchdog.observers.inotify_buffer').setLevel(logging.ERROR)

    converter = Converter(args.input_folder, args.output_folder)
    converter.convert_all()  # on start convert all files that are already in directory

    if not args.once:
        observer = DirectoryObserver(converter.src_folder)
        observer.start_observing(
            lambda x: converter.convert_file(os.path.basename(x.src_path))
        )  # start observing for new files

        while True:
            try:
                pass
            except KeyboardInterrupt:
                converter.stop_observing()


if __name__ == '__main__':
    main()
