import xml.etree.ElementTree as et


class ALSModder():
    def __init__(self, project_path):
        self.project_path = project_path
        self.output_filename = ''
        self.source_tree = None
        self.target_tree = None
        self.add_to_top = '<?xml version="1.0" encoding="UTF-8"?>\n'

    def load_source_file(self, source_filename):
        filename_pieces = source_filename.split('.')
        self.output_filename = filename_pieces[0] + '_output.' + filename_pieces[1]
        self.source_tree = et.parse(self.project_path + source_filename)

    def load_target_file(self, target_filename):
        self.target_tree = et.parse(self.project_path + target_filename)

    def write(self):
        self.target_tree.write(self.project_path + self.output_filename)
        tree_str = et.tostring(self.target_tree.getroot())
        res = self.add_to_top + tree_str.decode('utf-8')
        print('output file: ' + self.output_filename)
        open(self.output_filename, 'w').write(res)

    def get_group_infos(self, tree):
        groups = []
        name_by_id = {}
        id_by_name = {}
        for el in tree.iter('GroupTrack'):
            group_id = self.get_track_id(el)
            group_name = self.get_track_name(el)
            groups.append({'group_id': group_id, 'group_name': group_name})
            name_by_id[group_id] = group_name
            id_by_name[group_name] = group_id
        return groups, name_by_id, id_by_name

    def transfer_tracks(self):
        # get group infos from target tree
        target_group_infos, target_group_name_by_id, target_group_id_by_name = self.get_group_infos(self.target_tree)

        # get group infos from source tree
        source_group_infos, source_group_name_by_id, source_group_id_by_name = self.get_group_infos(self.source_tree)
        source_group_names = [info['group_name'] for info in source_group_infos]

        # get lists of source tracks by their group names
        source_tracks = self.get_all_tracks(self.source_tree)
        source_tracks_by_group_name = self.get_tracks_by_group_name(source_tracks, source_group_name_by_id)

        # remove target tracks for each target group id w/ corresponding source name
        target_tracks = self.get_all_tracks(self.target_tree)

        # self.print_source_tracks()
        # self.print_target_tracks()

        for target_at in target_tracks.findall('AudioTrack'):
            if self.get_group_name(target_at, target_group_name_by_id) in source_group_names:
                target_tracks.remove(target_at)

        for target_mt in target_tracks.findall('MidiTrack'):
            if self.get_group_name(target_mt, target_group_name_by_id) in source_group_names:
                target_tracks.remove(target_mt)

        seen = {}
        for idx, track in enumerate(target_tracks):
            if track.tag == 'GroupTrack' and self.get_track_name(track) not in seen:
                seen[self.get_track_name(track)] = True
                group_name = self.get_track_name(track)
                if group_name in source_tracks_by_group_name:
                    source_group_tracks = source_tracks_by_group_name[group_name]
                    i = 1
                    for sgt in source_group_tracks:
                        self.set_group_id(sgt, self.get_track_id(track))
                        target_ids = self.get_all_track_ids(target_tracks)
                        sgt_id = self.get_track_id(sgt)
                        while sgt_id in target_ids:
                            sgt_id = str(int(sgt_id) + 1)
                        self.set_track_id(sgt, sgt_id)
                        target_tracks.insert(idx + i, sgt)
                        i += 1

        # self.print_source_tracks()
        # self.print_target_tracks()

        # get midi & audio tracks from source tree
        # route source tracks to target groups
        # add source tracks under corresponding target groups

        # replace target_tracks
        self.target_tree.find('./LiveSet').remove(self.target_tree.find('./LiveSet/Tracks'))
        self.target_tree.find('./LiveSet').insert(0, target_tracks)

        # verify unique ids
        # alter track ids if necessary

        # print output to file
        self.write()

    def get_group_name(self, track, group_name_by_id):
        group_id = self.get_group_id(track)
        if group_id in group_name_by_id:
            return group_name_by_id[group_id]
        else:
            return ''

    def get_tracks_by_group_name(self, tracks, group_name_by_id):
        tracks_by_group_name = {}
        for track in tracks:
            if track.tag == 'ReturnTrack':
                continue
            elif track.tag == 'GroupTrack':
                tracks_by_group_name[self.get_track_name(track)] = []
            else:
                tracks_by_group_name[self.get_group_name(track, group_name_by_id)].append(track)
        return tracks_by_group_name

    def get_all_track_ids(self, tracks):
        return [self.get_track_id(track) for track in tracks]

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
            if track.tag == 'ReturnTrack':
                continue
            print('* * * * * * * * * *')
            print('\t' + track.tag + ' , ' + self.get_track_name(track) + ' , ' + self.get_track_id(track) + ' , ' + self.get_group_id(track))

    def print_source_tracks(self):
        self.print_tracks(self.get_all_tracks(self.source_tree), 'Source')

    def print_target_tracks(self):
        self.print_tracks(self.get_all_tracks(self.target_tree), 'Target')
