# How to setup and run application

## Install Dependencies:


```shell
pip install -e .
```

This will install your project in editable mode along with all the required dependencies listed in setup.cfg.

## Running the Bot

Once the installation is complete, you can run the Bot using the following command:

```shell
bot_housing_agent
```

## Explanation

The pip install -e . command installs your project and its dependencies in editable mode. This means that any changes you make to your code will be reflected immediately without having to reinstall the package.
The bot_housing_agent command (defined in your setup.cfg's console_scripts) will execute the run_bot function in your app.main module, launching your Telegram bot.