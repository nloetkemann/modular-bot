# modular-bot
this will be a modular bot where you can load your plugins by writing a single class your function and a yaml file as config for your plugin

the plugin will be loaded automaticaly and the command should be executed from the plugin

## Install
First install all the requirements
`pip install -r requirements.txt`

> Hint: if imdbpy wont install download the .whl file from [here](https://pypi.org/project/IMDbPY/#files) and install 
> it with pip3 install IMDbPY-6.8-py3-none-any.whl 

## Messengers

There are two possible messengers
- telegram
- discord
- (slack in progress)

Just activate it in the config.yaml

## Secrets
If you need to insert your secrets, just create a secrets.yaml file:
```yaml
secrets:
  plugins:
    - wiki: "to_be_set"
  bots:
    - telegram: "to_be_set"
  environment:
    - value: "to_be_set"
```
### Plugins with secrets
- weather [From here](https://home.openweathermap.org/users/sign_in)
- wolfram [From here](http://products.wolframalpha.com/api/)

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

> Hint2: use the Nothing plugin to catch all wrong inputs and 
> the help plugin to provide help for every activated plugin.
> The Help plugin should be the last but one plugin in the list.
> The Nothing plugin should be at the end of the list

## Write your own plugin

### First a your_plugin.yaml file
You need a config file for your plugin in the config dir which is by default `./config/`
```yaml
plugin:
  name: "your_plugin"
  token: "token if nesseccery"
  description: "a description is optional"
  methods:
    - name: "name_of_the_implemented_method_in_python"
      help: 'A litle help for understanding what this method will do'
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

> The answer list will have the Syntax you wrote, so if everything is lowercase, so will your answers

### Then a Your_plugin class
Then you need to write your own class for the plugin.
> Hint: the name of the class should be the name of the file with putting the first letter to uppercase.
```
from src.yaml.plugin import Plugin
class Your_plugin(Plugin):
    def name_of_the_implemented_method_in_python(self, param):
        here your code...
        ...
        ...
        in the end return the answer params
        return {'$answer_param': 'value'} # <-- name of the key starts with $
```

If you need something from the globalconfig you need to import the  config. You can get the location
or the timezone or anything else put to the environment variables.
```python
from src.config import config

config.get_env('location') # will return the value
config.env_value_exists('location') # will check if the value is set
```

#### Required values
If a token is required for your plugin your just have to set: 
```python
class Your_plugin(Plugin):
    token_required = True
```
It will be checked on start, and will throw an exception if non is set


To make sure all parameter exists for a method you kann call:
```python
def name_of_the_implemented_method_in_python(self, param):
    self.requiere_param(param)
```

## Syntax highlighting
Because every bot has its own syntax highlighting, 
there is a formatter in the Bot class, which formates the content to
the highlighting of the messenger.

so catch all highlights, use it like that:
- to make it bold use: `**test**`
- to make it italic use: `__test__`
- for a third highlighting use `*_test*_` (will display differently 
on telegram and discord)