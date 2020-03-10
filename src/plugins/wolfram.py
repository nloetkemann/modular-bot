import wolframalpha
from src.config import config as global_config
from src.yaml.plugin import Plugin


class Wolfram(Plugin):
    token_required = True
    list_of_ignored_infos = ['Length of data', 'Input interpretation', 'Number line']

    list_of_images = ['Plot', 'Pie chart']

    def __init__(self, name, config):
        super().__init__(name, config)
        self.wolfram_client = wolframalpha.Client(global_config.secrets.get_secret('wolfram'))

    def __do_request(self, term):
        return self.wolfram_client.query(term)

    def add_numbers(self, args):
        self.requiere_param(args, '$first', '$second')
        result = self.__do_request('{0}+{1}'.format(args['$first'], args['$second']))
        value = next(result.results).text
        return {'$result': value}

    def calculate_term(self, args):
        self.requiere_param(args, '$term')
        result = self.__do_request(args['$term'])

        all_values = {}

        for pod in result['pod']:
            if pod['@title'] in self.list_of_images:
                if int(pod['@numsubpods']) == 1 and 'img' in pod['subpod']:
                    img = pod['subpod']['img']['@src']
                    all_values[pod['@title']] = img
                elif int(pod['@numsubpods']) > 1:
                    description = ''
                    for subpod in pod['subpod']:
                        if 'img' in pod['subpod']:
                            img = pod['subpod']['img']['@src']
                            img += '\n |-> {0}\n {1}'.format(subpod['@title'], img)
                    all_values[pod['@title']] = description
            elif pod['@title'] not in self.list_of_ignored_infos:
                if int(pod['@numsubpods']) == 1:
                    description = pod['subpod']['plaintext']
                    all_values[pod['@title']] = description
                elif int(pod['@numsubpods']) > 1:
                    description = ''
                    for subpod in pod['subpod']:
                        description += '\n |-> _{0}_\n {1}'.format(subpod['@title'], subpod['plaintext'])
                    all_values[pod['@title']] = description

        return_value = '\n'
        for key in all_values:
            return_value += '*{0}* => {1}\n\n'.format(key, all_values[key])
        return {'$result': return_value}
