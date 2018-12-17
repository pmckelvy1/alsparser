import xml.etree.ElementTree as et


class ALSModder():
    def __init__(self):
        self.output_filename = ''
        self.source_tree = None
        self.target_tree = None
        self.add_to_top = '<?xml version="1.0" encoding="UTF-8"?>\n'

    def load_source_file(self, source_filename):
        filename_pieces = source_filename.split('.')
        self.output_filename = filename_pieces[0] + '_output.' + filename_pieces[1]
        self.source_tree = et.parse(source_filename)

    def load_target_file(self, target_filename):
        self.target_tree = et.parse(target_filename)

    def write(self):
        # self.target_tree.write(self.output_filename)
        tree_str = et.tostring(self.target_tree)
        res = self.add_to_top + tree_str
        open(self.output_filename, 'w').write(res)

    def get_group_infos(self, tree):
        groups = []
        for el in tree.iter('GroupTrack'):
            groups.append({'group_id': self.get_track_id(el), 'group_name': self.get_track_name(el)})
        return groups

    def transfer_tracks(self):
        # get group infos from target tree
        target_group_infos = self.get_group_infos(self.target_tree)
        # get group infos from source tree
        source_group_infos = self.get_group_infos(self.source_tree)
        source_group_ids = [info['group_id'] for info in source_group_infos]
        # remove target tracks for each target group id w/ corresponding source name
        target_tracks = self.get_all_tracks(self.target_tree)

        self.print_target_tracks()

        for target_at in target_tracks.iter('AudioTrack'):
            if self.get_group_id(target_at) in source_group_ids:
                target_tracks.remove(target_at)

        for target_at in target_tracks.iter('MidiTrack'):
            if self.get_group_id(target_at) in source_group_ids:
                target_tracks.remove(target_at)

        self.target_tree.find('./LiveSet').remove(self.target_tree.find('./LiveSet/Tracks'))
        self.target_tree.find('./LiveSet').insert(0, target_tracks)

        self.print_target_tracks()

        # get midi & audio tracks from source tree

        # route source tracks to target groups

        # add source tracks under corresponding target groups

        # verify unique ids
        # alter track ids if necessary

        # print output to file


    @staticmethod
    def get_track_id(track):
        return track.get('Id')

    @staticmethod
    def set_track_id(track, new_id):
        track.set('Id', new_id)
        return track

    @staticmethod
    def is_group_track(track):
        return track.tag == 'GroupTrack'

    @staticmethod
    def get_group_id(track):
        return track.find('TrackGroupId').get('Value')

    @staticmethod
    def set_group_id(track, new_group_id):
        track.find('TrackGroupId').set('Value', new_group_id)
        return track

    @staticmethod
    def get_track_name(track):
        return track.find('./Name/EffectiveName').get('Value')

    @staticmethod
    def get_all_tracks(tree):
        all_tracks = tree.find('./LiveSet/Tracks')
        return all_tracks

    def print_tracks(self, tracks, type_name):
        print('\n\n')
        print('> > > > > > > > > > > > >\n')
        print('> > > %s Tracks > > >\n' % type_name)
        print('> > > > > > > > > > > > >\n')
        for track in tracks:
            print('* * * * * * * * * *')
            print('\t' + track.tag + ' , ' + self.get_track_name(track) + ' , ' + self.get_track_id(track) + ' , ' + self.get_group_id(track))

    def print_source_tracks(self):
        self.print_tracks(self.get_all_tracks(self.source_tree), 'Source')

    def print_target_tracks(self):
        self.print_tracks(self.get_all_tracks(self.target_tree), 'Target')
