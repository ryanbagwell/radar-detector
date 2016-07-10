import unittest
from ..lib.settings import Settings


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.settings = Settings()

    def test_defaults_are_present(self):

        self.assertTrue(getattr(self.settings, 'pumpStatus', None))
        self.assertTrue(getattr(self.settings, 'autoThreshold', None))

    def test_change_should_be_present(self):

        def toggle_setting():

            if self.settings.pumpStatus == 'on':
                return 'off'
            elif self.settings.pumpStatus == 'off':
                return 'on'

        data = {'pumpStatus': toggle_setting()}

        self.settings.update_object(self.settings.objectId, data)

        self.settings.refresh()

        self.assertTrue('pumpStatus' in self.settings.changed)

        """ Set it back to the original setting """
        data = {'pumpStatus': toggle_setting()}
        self.settings.update_object(self.settings.objectId, data)

if __name__ == '__main__':
    unittest.main()
