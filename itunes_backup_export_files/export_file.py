import os
import shutil
import biplist
import sqlite3

class exporter:
    def __init__(self, manifest_db_path: str):
        '''
        :param manifest_db_path: the path of the file 'Manifest.db'
        '''
        # base_path/Manifest.db
        self.manifest_db_path = os.path.abspath(manifest_db_path)
        # base_path
        self.base_path = os.path.dirname(self.manifest_db_path)
        
        self.file_dict = {}
        self.file_info_dict = {}
        self.file_inner_join = {}

    # get files in base_path/00/* base_path/01/* ... base_path/bc/* ...
    # key: file name without extension; value: abspath of the file
    def get_file_dict(self) -> dict:
        '''
        :return: key->file name without extension; value->abspath of the file;
        '''
        for d in os.listdir(self.base_path):
            d_path = os.path.join(self.base_path, d)
            if os.path.isdir(d_path):
                for f in os.listdir(d_path):
                    self.file_dict[os.path.basename(f)] = os.path.join(d_path, f)
        
        return self.file_dict
    
    # get file_info from 'Files' table in the Manifest.db
    # key: fileID; value: file_info;
    def get_file_info_dict(self) -> dict:
        '''
        :return: key->fileID; value->file_info;
        '''
        if not os.path.exists(self.manifest_db_path):
            return None

        fit = file_info_translator()
        
        with sqlite3.connect(self.manifest_db_path) as conn:
            cursor = conn.cursor()
            files_table_data = cursor.execute(
                '''
                SELECT *
                FROM Files
                '''
            ).fetchall()
            for row_data in files_table_data:
                info = file_info(row_data)
                self.file_info_dict[info.fileID] = fit.to_dict(info)

        return self.file_info_dict

    # merge the file_dict and file_info_dict together by the keys
    # file_info_dict.keys() is the superset of file_dict.keys()
    def get_file_inner_join(self) -> dict:
        for k, v in self.file_dict.items():
            temp = self.file_info_dict[k].copy()
            temp['file_path'] = v
            self.file_inner_join[k] = temp

        return self.file_inner_join

    # a function that helps to export files to the save_path
    # filtered_file_list shall be a subset of file_inner_join.values(), 
    #   because it shall be filtered by yourself, with the domain, or the path, or other things
    def export_files(self, save_path: str, filtered_file_list: list):
        '''
        :param save_path: path to save the files
        :param filtered_file_list: a list of files wanted to be exported
        '''
        save_path = os.path.abspath(save_path)

        for f in filtered_file_list:
            f_path = os.path.join(save_path, f['full_path'])
            if not os.path.exists(os.path.dirname(f_path)):
                os.makedirs(os.path.dirname(f_path))
            shutil.copyfile(f['file_path'], f_path)

        
'''
CREATE TABLE Files (
    fileID TEXT PRIMARY KEY, 
    domain TEXT, 
    relativePath TEXT, 
    flags INTEGER, 
    file BLOB
    )
'''
class file_info:
    def __init__(self, row_data):
        self.fileID = row_data[0]
        self.domain = row_data[1]
        self.relativePath = row_data[2]
        self.flags = row_data[3]
        self.file = row_data[4]


class file_info_translator:
    def to_dict(self, fi):
        return {
            'file_id': fi.fileID,
            'domain': fi.domain,
            'relative_path': fi.relativePath,
            'full_path': self._blob_to_readable_text(fi)['$objects'][2]
        }

    def _blob_to_readable_text(self, fi):
        return biplist.readPlistFromString(fi.file)
