# modular-bot
this will be a modular bot where you can load your plugins by writing a single class your function and a yaml file as config for your plugin

the plugin will be loaded automaticaly and the command should be executed from the plugin


## Install
First install all the requirements
`pip install -r requirements.txt`


## Activate the plugins

in the `config.yaml` just add your plugin in the list
```yaml
plugins:
  - name: wiki
  - name: weather
  - name: welcome
  - name: other_plugin
``` 

> Hint: the name is case sensitive so, take care the name in your 
> config.yaml matches the name of the yaml file of the plugin


## Write your own plugin

You need a config file for your plugin in the config dir which is by default `./config/`
```yaml
plugin:
  name: "your-plugin"
  token: "token if nesseccery"
  description: "a description is optional"
  methods:
    - name: "name_of_the_implemented_method_in_python"
      keywords:
        list:
          - "do something with $param_name"
        params:
          - name: param_name
            type: string
            description: "some description"
      answers:
        list:
          - "the answer is $answer_param"
        params:
          - name: answer_param
            description: "some description"
```

The you need to write your own class for the plugin.
> Hint: the name of the class should be the name of the file with putting the first letter to uppercase.
```
from src.plugins.plugin import Plugin
class Your-plugin(Plugin):
    def name_of_the_implemented_method_in_python(param):
        here your code...
        ...
        ...
        in the end return the answer params
        return {answer_param: 'value'}
```

If you need something from the globalconfig you need to import the  config. You can get the location
or the timezone or anything else put to the environment.
```python
from src.config import config

config.get_env('location') # will return the value
config.env_value_exists('location') # will check if the value is set
```