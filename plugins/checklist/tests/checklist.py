import os.path

from src.plugin_test import PluginTest


class TestChecklist(PluginTest):
    test_obj_name = 'checklist'
    messenger = 'telegram'
    chat_id = '12345'

    @staticmethod
    def tests():
        return TestChecklist('test_create_checklist'), TestChecklist('test_add_checklist')

    @staticmethod
    def get_test_obj_name():
        return 'checklist'

    @staticmethod
    def _is_created(checklist_name):
        """
        checks if the file was created
        """
        return os.path.isfile(f'./temp/checklist/{checklist_name}')

    @staticmethod
    def _is_created_list(checklist_name, list_name):
        """
        checks if the list in the file was created
        """
        with open(f'./temp/checklist/{checklist_name}', 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if line[0] == '#']
        for line in lines:
            if line[2:].strip() == list_name:
                return True
        return False

    @staticmethod
    def _is_added(checklist_name, list_name, item):
        pass

    @staticmethod
    def clean(checklist_name):
        """
        cleans the temp/checklist/ file that was created by the test
        """
        if TestChecklist._is_created(checklist_name):
            os.remove(f'./temp/checklist/{checklist_name}')

    def test_create_checklist(self):
        """
        This test checks if the file and the list was created.
        """
        args = {'messenger': TestChecklist.messenger, 'chat_id': TestChecklist.chat_id, '$checklistname': 'Test'}
        file_name = args['messenger'] + '_' + args['chat_id'] + '.md'
        plugin = self.get_test_obj(self.get_test_obj_name())
        result = plugin.create_checklist(args)
        self.assertEqual(result, {})
        self.assertEqual(self._is_created(file_name), True)
        self.assertEqual(self._is_created_list(file_name, args['$checklistname']), True)
        TestChecklist.clean(file_name)

    def test_add_checklist(self):
        """
        checks if the function will add something to a list
        """
        args = {'messenger': 'telegram', 'chat_id': '123456', '$checklistname': 'Test', '$checklistitem': 'Item'}
        file_name = args['messenger'] + '_' + args['chat_id'] + '.md'
        plugin = self.get_test_obj(self.get_test_obj_name())
        result = plugin.add_to_checklist(args)
        self.assertEqual(result, {})
        self.assertEqual(self._is_created_list(file_name, args['$checklistname']), True)
