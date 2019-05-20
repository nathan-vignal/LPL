""" Python 3 API for interactive oral data visualization with Bokeh
Coding : utf-8
Docstrings in reStructuredText style
Develop in internship in Laboratoire Parole et Langage (lpl-aix.fr)
22/06/2018 V1.0 by Antonin Gaboriau (antonin.gaboriau@hotmail.fr)
"""

from os import listdir
from numpy import *
from bokeh.io import output_notebook
from re import match
import warnings

warnings.simplefilter('ignore')
output_notebook()


class VisualizationData:
    """ Class to read data and be visualize by Display's methods"""

    def __init__(self, directory, conversations=[], speakers=[], corpus_format="minimalist", **format_details):
        """ VisualizationData Constructor

        Read csv files that matchs with conversation and speaker filters, then store readed data and metadata

        :param directory: Name of directory (with path) where the scv files are
        :type directory: string

        :param conversations: To be read, a data file must have one of the conversation ID from this optionnal list
        unless the list is empty or undefined.
        :type conversations: list of string

        :param speakers: To be read, a data file must have one of the speaker ID from this optionnal list
        unless the list is empty or undefined.
        :type speakers: list of string

        :param corpus_format: Predefined format for data reading, including all format details from next parameter.
                              By default the format is set to a minimalist format.
        :type corpus_format: string 'SW' or 'CID'

        :param \**format_detail: List of named parameters, 8 possible :
        * data_columns: List of data files columns names in the right order. Must include at least 'time' and 'values'
                        type: list of string
        * metadata_columns: List of metadata file columns names in the right order.
                            Must include at least 'corpus', 'data_type', 'id_conv' and 'id_speaker'
                            type: list of string
        * data_delimiter: Data file delimiter between columns
                          type: string
        * metadata_delimiter: Metadata file delimiter between columns
                              type: string
        * data_head_lines: Head lines number in data files
                           type: int
        * metadata_head_lines: Head lines number in metadata file
                               type: int
        * file_name: List of informations (that are also in metadata file) with wich data files name are makes.
                     type: list of string
        * file_name_delimiter: Delimiter between information in data files name
                               type: string
        """

        # Initialize predefined formats
        if corpus_format == "CID":
            format = {'data_columns': ['corpus', 'id_speaker', 'fill', 'time',
                                       'time_stop', 'values', 'fill'],
                      'metadata_columns': ['id_conv', 'id_speaker', 'data_type', 'corpus'],
                      'data_delimiter': ",",
                      'metadata_delimiter': "\t",
                      'data_head_lines': 0,
                      'metadata_head_lines': 1,
                      'file_name': ['id_speaker'],
                      'file_name_delimiter': " "}
        elif corpus_format == "SW":
            format = {'data_columns': ['id_line', 'values', 'time'],
                      'metadata_columns': ['id', 'id_conv', 'id_caller', 'id_speaker', 'id_topic',
                                           'sex', 'age', 'geography', 'level_study', 'corpus', 'data_type'],
                      'data_delimiter': "\t",
                      'metadata_delimiter': "\t",
                      'data_head_lines': 1,
                      'metadata_head_lines': 1,
                      'file_name': ['corpus', 'id_conv', 'data_type', 'id_caller'],
                      'file_name_delimiter': "_"}
        else:  # minimalist  format
            format = {'data_columns': ['time', 'values'],
                      'metadata_columns': ['id_conv', 'id_speaker', 'data_type', 'corpus'],
                      'data_delimiter': "\t",
                      'metadata_delimiter': "\t",
                      'data_head_lines': 0,
                      'metadata_head_lines': 0,
                      'file_name': ['id_speaker'],
                      'file_name_delimiter': ""}
        for info in format:
            if info in format_details:
                format[info] = format_details[info]

        # Read the metadata
        for file_name in listdir(directory):
            if match(".*metadata.*\.csv$", file_name):
                metadata_file = open(directory + "/" + file_name, "r")
                self.metadata = genfromtxt(metadata_file, skip_header=format['metadata_head_lines'],
                                           encoding=None, delimiter=format['metadata_delimiter'],
                                           names=format['metadata_columns'], dtype=None)
                break

        self.data = []
        cpt = 0

        # Read files which match with the filters
        for line in self.metadata:
            if ((len(conversations) == 0 or str(line['id_conv']) in conversations)
                    and (len(speakers) == 0 or str(line['id_speaker']) in speakers)):
                cpt += 1
                to_add = {'data': {}, }
                for info_key in format['metadata_columns']:
                    to_add[info_key] = line[info_key]
                file_name = line[format['file_name'][0]]
                if len(format['file_name']) > 1:
                    for i in range(1, len(format['file_name'])):
                        info = line[format['file_name'][i]]
                        file_name = file_name + format['file_name_delimiter'] + str(info)
                file_name += ".csv"
                to_add['data'] = genfromtxt(open(directory + "/" + file_name), encoding=None,
                                            skip_header=format['data_head_lines'],
                                            delimiter=format['data_delimiter'],
                                            names=format['data_columns'], dtype=None)
                self.data.append(to_add)

        print(str(cpt) + " data files have been read")

speakerData = VisualizationData("./data/metadata/", corpus_format="SW")
print( speakerData)

# test by VIGNAL Nathan from here

