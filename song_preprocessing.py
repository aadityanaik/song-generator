import numpy as np
from pydub import AudioSegment


class Song:

    def __init__(self, **kwargs):
        filename = kwargs.get('filename')
        fileFormat = kwargs.get('format')
        array = kwargs.get('npArray')
        reference = kwargs.get('referenceSound')

        if filename is not None and fileFormat is not None and array is None and reference is None:
            sound = AudioSegment.from_file(filename, format=fileFormat)
            if sound.channels > 1:
                sound = sound.set_channels(1)
            self.data = sound.get_array_of_samples()
            self.frame_rate = sound.frame_rate
            self.channels = sound.channels
            self.sample_width = sound.sample_width

        else:
            if filename is None and fileFormat is None and reference is not None:
                self.frame_rate = reference.frame_rate
                self.channels = reference.channels
                self.sample_width = reference.sample_width

                if array is None:
                    self.data = reference.get_array_of_samples()

                else:
                    if self.sample_width == 1:
                        datatype = np.int8

                    else:
                        if self.sample_width == 2:
                            datatype = np.int16

                    self.data = array.astype(datatype)

            else:
                print('Insufficient values')

    def save(self, filename, format='wav'):
        sound = AudioSegment(
            data=self.data.tobytes(),
            frame_rate=self.frame_rate,
            channels=self.channels,
            sample_width=self.sample_width
        )

        sound.export(filename, format)

    def segment(self, t1, t2):
        sound = AudioSegment(
            data=self.data.tobytes(),
            frame_rate=self.frame_rate,
            channels=self.channels,
            sample_width=self.sample_width
        )

        segmented_sound = sound[t1:t2]

        return Song(referenceSound=segmented_sound)



