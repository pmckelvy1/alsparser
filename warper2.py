from als_modder import ALSModder

def run():
    # als_modder = ALSModder('./projects/drumrack_mod/', '../../MASTER TEMPLATE 2.0 Project/')
    # als_modder.load_source_file('drumrack_tester.xml')

    als_modder = ALSModder('../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/', '../../MASTER TEMPLATE 2.0 Project/')
    als_modder.load_source_file('scale_chord_a.xml')

    als_modder.mod_chord_rack()

if __name__ == '__main__':
    run()