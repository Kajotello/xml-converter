import json
import xml.etree.ElementTree as ET
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import io

class NewFileHandler(FileSystemEventHandler):
        def __init__(self, converter):
            self.converter = converter

        def handler(self, event):
            filename = os.path.basename(event.src_path)
            self.converter.convert_file(filename)

        def on_created(self, event):
            self.handler(event)
            

class Converter:
    def __init__(self, src_folder: str, dst_folder: str, root_element_name: str='FLIGHT') -> None:
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.root_element_name = root_element_name

    def _read_file(self, filehandler: io.TextIOWrapper) -> dict:

        """ Open file with given filename from source folder and read it as a JSON """

        content = json.load(filehandler)
        flight_data = content[self.root_element_name]
        return flight_data

    def _convert_to_XML(self, flight_data: dict) -> ET.Element:

        """Convert single-level dict to XML element"""

        flight_element = ET.Element(self.root_element_name)
        for (attribute, value) in flight_data.items():
            logging.debug(f'Read attribute {attribute} with value {value}')
            element = ET.SubElement(flight_element, attribute)
            logging.debug(f'Attribute {attribute} added successfully to document tree')
            element.text = str(value)
        return flight_element

    def _write_file(self, filehandler: io.TextIOWrapper, element: ET.Element) -> None:

        """Write XML element with proper name to destination folder"""

        filehandler.write(ET.tostring(element, encoding="unicode"))

    def _delete_old_file(self, filename: str) -> None:

        """Delete old file when it isn't longer needed"""

        os.unlink(f'{self.src_folder}{filename}')

    def _make_conversion(self, input_fh: io.TextIOWrapper, output_fh: io.TextIOWrapper) -> None:
        try:
            data = self._read_file(input_fh)  
        except json.JSONDecodeError:
            logging.error(f'File {input_fh.name} is in wrong format and cannot be parsed as JSON.')
            return
        except KeyError:
            logging.error(f'File {input_fh.name} do not contain {self.root_element_name} field')
            return
        
        element = self._convert_to_XML(data)
        self._write_file(output_fh, element)
        self._delete_old_file(os.path.basename(input_fh.name))

    def start_observing(self) -> None:

        """Start observing changes in source folder to handle conversion for new files"""

        event_handler = NewFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.src_folder, recursive=False)
        self.observer.start()

    def stop_observing(self) -> None:

        """Terminate observing for changes in source folder"""

        self.observer.stop()
    
    def convert_file(self, filename: str) -> None:

        """Convert single file with given name from source folder and write it back to destination folder"""

        logging.info(f'Conversion started for file {self.src_folder}{filename}')
        if filename.split('.')[-1] == 'json':
            output_filename = '.'.join(filename.split('.')[:-1])
        else:
            output_filename = filename
        output_filename += '.xml'
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
                output_fh = open(f'{self.dst_folder}{output_filename}', 'w')
            except FileNotFoundError:
                logging.error(f'Directory {self.dst_folder} does not exist')
                return
            except PermissionError:
                logging.error(f"Program doesn't have permission to write to {self.dst_folder}")
                return 
            with output_fh:
                self._make_conversion(input_fh, output_fh)
        logging.info(f'Conversion successfully ended - results wrote to the file {self.dst_folder}{filename}.xml')
    
    def convert_all(self) -> None:

        """Convert all files from source folder"""

        for filename in os.listdir(self.src_folder):
            self.convert_file(filename)
    




    