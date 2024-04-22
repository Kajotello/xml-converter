import json
import xml.etree.ElementTree as ET
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

    def _read_file(self, filename: str) -> dict:

        """ Open file with given filename from source folder and read it as a JSON """

        with open(f'{self.src_folder}{filename}', 'r') as fh:
            content = json.load(fh)
            flight_data = content[self.root_element_name]
            return flight_data

    def _convert_to_XML(self, flight_data: dict) -> ET.Element:
        flight_element = ET.Element(self.root_element_name)
        for (attribute, value) in flight_data.items():
            logging.debug(f'Read attribute {attribute} with value {value}')
            element = ET.SubElement(flight_element, attribute)
            logging.debug(f'Attribute {attribute} added successfully to document tree')
            element.text = str(value)
        return flight_element

    def _write_file(self, filename: str, element: ET.Element) -> None:
        if filename.split('.')[-1] == 'json':
            filename = '.'.join(filename.split('.')[:-1])
        with open(f'{self.dst_folder}{filename}.xml', 'w') as fh:
            fh.write(ET.tostring(element, encoding="unicode"))

    def _delete_old_file(self, filename: str) -> None:
        os.unlink(f'{self.src_folder}{filename}')

    def start_observing(self) -> None:
        event_handler = NewFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.src_folder, recursive=False)
        self.observer.start()

    def stop_observing(self) -> None:
        self.observer.stop()
    
    def convert_file(self, filename: str) -> None:
        logging.info(f'Conversion started for file {self.src_folder}{filename}')
        try:
            data = self._read_file(filename)
        except FileNotFoundError:
            logging.error(f'File with name {filename} not found in {self.src_folder}')
            return
        except PermissionError:
            logging.error(f"Program doesn't have permission to read {filename} in {self.src_folder}")
            return   
        except json.JSONDecodeError:
            logging.error(f'File {filename} is in wrong format and cannot be parsed as JSON.')
            return
        except KeyError:
            logging.error(f'File {filename} do not contain FLIGHT field')
            return
        
        element = self._convert_to_XML(data)
        try:
            self._write_file(filename, element)
        except:
            logging.error(f'Destination folder {self.dst_folder} does not exist')
            return
        
        self._delete_old_file(filename)
        logging.info(f'Conversion successfully ended - results wrote to the file {self.dst_folder}{filename}.xml')
    
    def convert_all(self) -> None:
        for filename in os.listdir(self.src_folder):
            self.convert_file(filename)
    




    