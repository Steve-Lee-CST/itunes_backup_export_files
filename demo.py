from itunes_backup_export_files import exporter

def filter(file_inner_join: dict) -> list:
    domain_name = 'com.apple.AppStore'
    file_list = []
    for item in file_inner_join.values():
        # domain filter
        if 'com.tencent.xin' in item['domain']:
            file_list.append(item)
    return file_list

if __name__ == "__main__":
    manifest_db_path = 'your_backup_path/Manifest.db'      # such as: 00003231-041c38926803092E/Manifest.db
    save_path = 'temp/wechat'

    ep = exporter(manifest_db_path)

    # step 1
    fd = ep.get_file_dict()
    print(f'count of file_dict: {len(fd)}')

    # step 2
    fid = ep.get_file_info_dict()
    print(f'count of file_info_dict: {len(fid)}')

    # step 3
    fij = ep.get_file_inner_join()
    print(f'count of file_inner_join: {len(fij)}')

    # step 4
    # filter the files
    file_list = filter(fij)
    
    # step 5
    # export files
    ep.export_files(save_path, file_list)
    print('Done') 
    
    pass
