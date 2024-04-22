import json
import xml.etree.ElementTree as ET
import os
import logging
import io


class Converter:
    def __init__(self, src_folder: str, dst_folder: str) -> None:
        self.src_folder = src_folder
        self.dst_folder = dst_folder

    def _read_file(self, filehandler: io.TextIOWrapper) -> dict:

        """ Open file with given filename from source folder
        and read it as a JSON """

        flight_data = json.load(filehandler)
        return flight_data

    def _convert_to_XML(self, flight_data: dict) -> ET.Element:

        """Convert single-level dict to XML element"""

        if len(flight_data) > 1:
            raise TypeError('More than one root element')

        if len(flight_data) == 0:
            raise TypeError('No root element')

        root_element_name = list(flight_data.keys())[0]
        flight_element = ET.Element(root_element_name)
        for (attribute, value) in flight_data[root_element_name].items():
            logging.debug(f'Read attribute {attribute} with value {value}')
            element = ET.SubElement(flight_element, attribute)
            logging.debug(f'Attribute {attribute} added successfully to document tree')
            element.text = str(value)
        return flight_element

    def _write_file(self, filehandler: io.TextIOWrapper, element: ET.Element) -> None:

        """Write XML element with proper name to destination folder"""

        ET.indent(element, space="\t", level=0)
        filehandler.write(ET.tostring(element, encoding="unicode"))

    def _delete_old_file(self, filename: str) -> None:

        """Delete old file when it isn't longer needed"""

        os.unlink(f'{self.src_folder}{filename}')

    def _make_conversion(self, input_fh: io.TextIOWrapper, output_fh: io.TextIOWrapper) -> None:
        data = self._read_file(input_fh)
        element = self._convert_to_XML(data)
        self._write_file(output_fh, element)

    def convert_file(self, filename: str) -> None:

        """Convert single file with given name from source folder
        and write it back to destination folder"""

        src_file_path = f'{self.src_folder}{filename}'

        logging.info(f'Conversion started for file {src_file_path}')
        if filename.split('.')[-1] == 'json':
            output_filename = '.'.join(filename.split('.')[:-1])
        else:
            output_filename = filename
        dest_file_path = f'{self.dst_folder}{output_filename}.xml'

        try:
            input_fh = open(f'{self.src_folder}{filename}', 'r')
        except FileNotFoundError:
            logging.error(f'File with name {filename} not found in {self.src_folder}')
            return
        except PermissionError:
            logging.error(f"Program doesn't have permission to read {filename} in {self.src_folder}")
            return
        with input_fh:
            try:
                output_fh = open(f'{dest_file_path}', 'w')
            except FileNotFoundError:
                logging.error(f'Directory {self.dst_folder} does not exist')
                return
            except PermissionError:
                logging.error(f"Program doesn't have permission to write to {self.dst_folder}")
                return
            except IsADirectoryError:
                logging.error(f"There is already a directory with name {dest_file_path}")
                return

            with output_fh:
                try:
                    self._make_conversion(input_fh, output_fh)
                except json.JSONDecodeError:
                    logging.error(f'File {filename} is in wrong format and cannot be parsed as JSON.')
                    return
                except TypeError as e:
                    logging.error(f'File {filename} not in expected format: {e}')
                    return
                except AttributeError:
                    logging.error(f'File {filename} does not contain nested object with flight data')
                    return
        self._delete_old_file(os.path.basename(src_file_path))
        logging.info(f'Conversion successfully ended - results wrote to the file {dest_file_path}')

    def convert_all(self) -> None:

        """Convert all files from source folder"""

        for filename in os.listdir(self.src_folder):
            self.convert_file(filename)
