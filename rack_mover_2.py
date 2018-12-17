from als_modder import ALSModder

def run():
    als_modder = ALSModder()
    als_modder.load_source_file('./projects/xml_parser_test/test_rack.xml')
    als_modder.load_target_file('./projects/xml_parser_test/test.xml')
    als_modder.transfer_tracks()

if __name__ == '__main__':
    run()