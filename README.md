[![GitHub Release][releases-shield]][releases]
![GitHub all releases][download-all]
![GitHub release (latest by SemVer)][download-latest]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

# Airzone Cloud plugin for Home Assistant

## Introduction

Allow to view & control all your zones register on your Airzone Cloud ([airzonecloud.com](https://airzonecloud.com)) account from [Home Assistant](https://www.home-assistant.io/).

If you're looking for the main Airzone Cloud *Daikin* ([dkn.airzonecloud.com](https://dkn.airzonecloud.com)), use this plugin : https://github.com/max13fr/AirzonecloudDaikin-HomeAssistant

![Screenshot](screenshot.png)

## Install / upgrade

### Add module

In your home assistant directory (where you have your **configuration.yaml**) :

- create the directory **custom_components** if not already existing
- copy **custom_components/airzonecloud** directory from this github repository inside your **custom_components**. In case of upgrade, you can delete the **airzonecloud** first then copy the new one.

Finally, you should have the following tree :

- configuration.yaml
- custom_components/
  - airzonecloud/
    - \_\_init\_\_.py
    - climate.py
    - const.py
    - manifest.py

### Configure

In your **configuration.yaml** add the following lines :

```
climate:
  - platform: airzonecloud
    username: your@mail.com
    password: yourpassword
```

You're username & password should match what you use to connect to https://www.airzonecloud.com

Don't forget to restart your Home Assistant when you update your configuration.

#### Change refresh interval

Default refresh interval is **10 seconds**.

You can increase or decrease this value but be warned that you can be banned by Airzone if you refresh too often.

```
climate:
  - platform: airzonecloud
    username: your@mail.com
    password: yourpassword
    scan_interval: 5
```

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/tsenay/Airzonecloud-HomeAssistant.svg?style=for-the-badge
[commits]: https://github.com/tsenay/Airzonecloud-HomeAssistant/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/tsenay/Airzonecloud-HomeAssistant.svg?style=for-the-badge
[license]: LICENSE
[maintenance-shield]: https://img.shields.io/badge/maintainer-tsenay%20%40tsenay-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tsenay/Airzonecloud-HomeAssistant.svg?style=for-the-badge
[releases]: https://github.com/tsenay/Airzonecloud-HomeAssistant/releases
[user_profile]: https://github.com/tsenay
[download-all]: https://img.shields.io/github/downloads/tsenay/Airzonecloud-HomeAssistant/total?style=for-the-badge
[download-latest]: https://img.shields.io/github/downloads/tsenay/Airzonecloud-HomeAssistant/latest/total?style=for-the-badge
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=tesla_custom
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
