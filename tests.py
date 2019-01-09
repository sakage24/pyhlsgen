from unittest import TestCase
from unittest import main
from operation.files import Crop


class RunTests(TestCase):
    def test_show_crop_messages(self):
        crop = Crop()
        crop.on_message(
            source='path/to/dir',
            ss=10,
            framerate=0.03,
            output_file_name='outputnames',
            platform='linux',
        )

if __name__ == '__main__':
    main()
