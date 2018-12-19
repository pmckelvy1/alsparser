from als_modder import ALSModder

def run():
    als_modder = ALSModder('./projects/xml_parser_test/')
    als_modder.load_source_file('test_rack.xml')
    als_modder.load_target_file('test.xml')
    als_modder.transfer_tracks()

if __name__ == '__main__':
    run()