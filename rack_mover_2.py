from als_modder import ALSModder

def run():
    als_modder = ALSModder('../../PS 2018 Followthru/booth Project/', '../../MASTER TEMPLATE 2.0 Project/')
    als_modder.load_source_file('booth.xml')
    als_modder.load_target_file('MASTER_TEMPLATE_25_TARGET.xml')
    als_modder.transfer_tracks()

if __name__ == '__main__':
    run()