import wolframalpha
from src.yaml.plugin import Plugin


class Wolfram(Plugin):
    token_required = True
    list_of_ignored_infos = ['Length of data', 'Input interpretation', 'Number line']
    list_of_solutions = ['Solutions', 'Result']

    list_of_images = ['Plot', 'Pie chart']

    def __init__(self, name, config):
        super().__init__(name, config)
        self.wolfram_client = wolframalpha.Client(self.token)

    def __do_request(self, term):
        return self.wolfram_client.query(term)

    def add_numbers(self, args):
        self.requiere_param(args, '$first', '$second')
        result = self.__do_request('{0}+{1}'.format(args['$first'], args['$second']))
        value = next(result.results).text
        return {'$result': value}

    def solution_exists(self, args):
        for subpod in args['pod']:
            if subpod['@title'] in self.list_of_solutions:
                return subpod

    def calculate_term(self, args):
        self.requiere_param(args, '$term')
        result = self.__do_request(args['$term'])

        all_values = {}

        pod_result = self.solution_exists(result)
        if pod_result is not None:
            if int(pod_result['@numsubpods']) == 1:
                all_values[pod_result['@title']] = pod_result['subpod']['plaintext']
            elif int(pod_result['@numsubpods']) > 1:
                result_text = ''
                for subpod in pod_result['subpod']:
                    result_text += '\n \-> {0}'.format(subpod['plaintext'])
                all_values[pod_result['@title']] = result_text
        else:
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
