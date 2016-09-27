# Windows-Agent

Windows agent of Open-Falcon Monitor System

## Features

* Basic data collection
* IIS data collection
* SQLserver data colecttion
* HTTP api to push
* Run as window backgroud service

### Provide in Future

* Plugin schedule
* Memory cache

## Requirements

* pypiwin32
* wmi
* flask
* psutil
* winstats

## Installation

```
git clone https://github.com/AutohomeRadar/Windows-Agent
cd Windows-Agent
pip install -r requirements.txt
python agent install
python agent start
```

## Configuration

Edit the cfg.json file. You can copy it from cfg.json.example. The meaning of each key are as follow

### Basic config

| key | type | descript|
|-----|------|----|
| debug | bool | whether in debug mode or not|
| hostname | string | the same as OpenFalcon Linux agent|
| ip | string | ip address|
| heartbeat | dict | details in the later of this file |
| transfer | dict | details in the later of this file |
| http | dict | details in the later of this file |
| collector | dict | details in the later of this file |
| ignore | array | the metrics you wanna ignore |

### Heartbeat config

| key | type | descript|
|-----|------|----|
| enabled | bool | whether enable send heartbeat to hbs|
| addr | string | ip adrress of hbs|
| interval | int | intervals between two heartbeat report|
| timeout | int | timeout |

### Transfer config

| key | type | descript|
|-----|------|----|
| enabled | bool | whether enable send data to transfer|
| addr | dict of string | ip adrresses of all transfer |
| interval | int | intervals between two heartbeat report|
| timeout | int | timeout |

### Http config 
| key | type | descript|
|-----|------|----|
| enabled | bool | whether enable http api|
| listen | string | the port server listened on|

## Usage

Install the agent to register it to Service and Registry

```
python agent install
```

Start the agent 

```
python agent start
```

Stop the agent

```
python agent stop
```

Remove service

```
python agent remove
```

## Deployment

You can deploy manually

```
python agent.py install
python agent.py start
```

Update is similar to installation. But don't forget to stop the old installations at first and than install the new version.

```
python agent.py stop
## Unzip and replace all files with new version
python agent.py install
python agent.py start
```

Or You can deploy using puppet

## Developing and Contributing

You're highly encouraged to participate in the development. Please submit Issues and Pull Requests with pleasure.

## Support and Community

### QQ Group

You could join our official Open Source QQ Group 452994151.
What's more, you could join [Open-Falcon QQ Group](http://book.open-falcon.org/zh/index.html)，we are also there.

### Mail

You can contact us by <autohomeops@autohome.com.cn>.

### Bug Track

If you have any suggestions, bug reports, or annoyances please report them to our issue tracker at <https://github.com/AutohomeRadar/Windows-Agent/issues>.

### Wiki

<https://github.com/AutohomeRadar/Windows-Agent/wiki>

### Blog

The official blog of our team <http://autohomeops.corpautohome.com>
 

## License

This software is licensed under the Apache License.
See the LICENSE file in the top distribution directory for the full license text.