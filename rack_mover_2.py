from als_modder import ALSModder

def run():
    als_modder = ALSModder('../../PS 2018 Followthru/booth Project/', '../../MASTER TEMPLATE 2.0 Project/')
    als_modder.load_source_file('booth.xml')
    als_modder.load_target_file('MASTER_TEMPLATE_25_TARGET.xml')
    als_modder.transfer_session()

    # als_modder = ALSModder('./projects/xml_parser_test/', './projects/xml_parser_test/')
    # als_modder.load_source_file('test_rack.xml')
    # als_modder.load_target_file('test.xml')
    # als_modder.transfer_session()

if __name__ == '__main__':
    run()