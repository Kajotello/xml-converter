import argparse
import logging
from src.converter_class import Converter

def parse_arguments():
    parser = argparse.ArgumentParser(
                    prog='JSON2XML converter',
                    description='Convert JSON fueling files to XML',
                    )

    parser.add_argument('input_folder')
    parser.add_argument('output_folder')
    parser.add_argument('-l', '--logfile')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    logger = logging.getLogger('__name__')
    logging.basicConfig(filename=args.logfile, encoding='utf-8', level=logging.INFO)

    converter = Converter(args.input_folder, args.output_folder)

    converter.convert_all()

    converter.start_observing()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            converter.stop_observing()