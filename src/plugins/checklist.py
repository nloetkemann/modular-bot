import os

from src.exceptions.not_found_exception import NotFoundException
from src.yaml.plugin import Plugin


class Checklist(Plugin):
    # todo more languages
    CHECKLIST_PATH = './temp/checklist/'

    class ChecklistItem:
        def __init__(self, name, status):
            self.name = name
            self.status = status

        def __str__(self):
            value = 'x' if self.status else ' '
            return f'- [{value}] {self.name}\n'

        def to_message(self):
            if self.status:
                return f'\- ~{self.name}~\n'
            return f'\- {self.name}\n'

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)

    def _load_file(self, messenger, chat_id):
        checklists = {}
        with open(self._file_name(messenger, chat_id), 'r') as file:
            content = file.readlines()
        last_checklist = ''
        for line in content:
            if line[0] == '-':
                item = line[5:].strip()
                status = line[3].strip()
                checklists[last_checklist].append(self.ChecklistItem(item, status == 'x'))
            elif line[0] == '#':
                last_checklist = line[2:].strip()
                checklists[last_checklist] = []
        return checklists

    def _create_file(self, messenger, chat_id, checklist_name='', items=[]):
        with open(self._file_name(messenger, chat_id), 'w') as file:
            if checklist_name != '':
                file.write(f'# {checklist_name}\n')
                file.writelines([str(item) for item in items])
            file.close()

    def _save_file(self, messenger, chat_id, checklists):
        with open(self._file_name(messenger, chat_id), 'w') as file:
            for entry in checklists:
                file.write(f'# {entry}\n')
                file.writelines([str(item) for item in checklists[entry]])
        file.close()

    def _file_name(self, messenger, chat_id):
        return self.CHECKLIST_PATH + f'{messenger}_{chat_id}.md'

    def create_checklist(self, args):
        if os.path.isfile(self._file_name(args['messenger'], args['chat_id'])):
            checklists = self._load_file(args['messenger'], args['chat_id'])
            checklists[args['$checklistname']] = []
            self._save_file(args['messenger'], args['chat_id'], checklists)
        else:
            self._create_file(args['messenger'], args['chat_id'])
            checklists = {args['$checklistname']: []}
            self._save_file(args['messenger'], args['chat_id'], checklists)
        return {}

    def add_to_checklist(self, args):
        messenger = args['messenger']
        chat_id = args['chat_id']
        checklist_name = args['$checklistname']
        checklist_item = args['$checklistitem']
        item = self.ChecklistItem(checklist_item, False)
        if os.path.isfile(self._file_name(messenger, chat_id)):
            checklists = self._load_file(messenger, chat_id)
            if checklist_name in checklists:
                checklists[checklist_name].append(item)
            else:
                checklists[checklist_name] = [item]
            self._save_file(messenger, chat_id, checklists)
        else:
            self._create_file(messenger, chat_id, checklist_name, [item])
        return {}

    def status_checklist(self, args):
        self.requiere_param(args, '$checklistname')
        messenger = args['messenger']
        chat_id = args['chat_id']
        checklist_name = args['$checklistname']
        if os.path.isfile(self._file_name(messenger, chat_id)):
            text = ''
            checklists = self._load_file(messenger, chat_id)
            if checklist_name in checklists:
                text += f'**{checklist_name.upper()}**\n'
                text += ''.join([item.to_message() for item in checklists[checklist_name]])
                return {'$checklist': text}
            return {'$checklist': 'Es gibt die Checkliste nicht'}
        else:
            return {'$checklist': 'Keine Checklisten erstellt'}

    def remove_from_checklist(self, args):
        self.requiere_param(args, '$checklistname', '$checklistitem')
        messenger = args['messenger']
        chat_id = args['chat_id']
        checklist_name = args['$checklistname']
        checklist_item = args['$checklistitem']
        if os.path.isfile(self._file_name(messenger, chat_id)):
            checklists = self._load_file(messenger, chat_id)
            items = checklists[checklist_name]
            checklists[checklist_name] = [item for item in items if item.name != checklist_item]
            self._save_file(messenger, chat_id, checklists)
            return {}
        raise NotFoundException('Keine Checkliste vorhanden')

    def check_from_checklist(self, args):
        self.requiere_param(args, '$checklistname', '$checklistitem')
        messenger = args['messenger']
        chat_id = args['chat_id']
        checklist_name = args['$checklistname']
        checklist_item = args['$checklistitem']
        if os.path.isfile(self._file_name(messenger, chat_id)):
            checklists = self._load_file(messenger, chat_id)
            for item in checklists[checklist_name]:
                if item.name == checklist_item:
                    item.status = True
            self._save_file(messenger, chat_id, checklists)
            return {}
        raise NotFoundException('Nichts gefunden')

    def uncheck_from_checklist(self, args):
        self.requiere_param(args, '$checklistname', '$checklistitem')
        messenger = args['messenger']
        chat_id = args['chat_id']
        checklist_name = args['$checklistname']
        checklist_item = args['$checklistitem']
        if os.path.isfile(self._file_name(messenger, chat_id)):
            checklists = self._load_file(messenger, chat_id)
            for item in checklists[checklist_name]:
                if item.name == checklist_item:
                    item.status = False
            self._save_file(messenger, chat_id, checklists)
            return {}
        raise NotFoundException('Nichts gefunden')
