# itunes_backup_export_files
a package helps to export files from itunes-backup

* Test environment: 
  * win10-19041 & Python-3.8.3
 
* How to use:
  * use iTunes to backup ios devices data
  * open the backup folder and copy **the path of** *Manifest.db* 
  * in the demo.py:
    * set: manifest_db_path = your_Manifest_db_path
    * set: save_path = wherever_you_want_to_save_export_files
    * modify the filter function
    * run demo.py
    * done
