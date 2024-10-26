### 0.0.1
- Added backbone structure and updated README

## 0.1.0
- Added backbone for dependencies containerization

## 0.2.0
- Added MongoDbClient and TelegramApplication linked to IoC containers

## 0.3.0
- Added service container and modified TelegramApplication startup

## 0.4.0
- Added template container, loading of templates done now via json files configuration

## 0.5.0
- Created template service, now its injected in the telegram handlers to get conversation templates

## 0.6.0
- Changed telegram library, now using aiogram instead of pyhon-telegran-bot

## 0.7.0
- Added handlers for getting query params

### 0.7.1
- Added script for testing and removing keyboardbuttons

### 0.7.2
- Added start handler to give a description and added keyboard buttons to be used along side commands for starting handler

### 0.7.3
- Added folder and scripts for debian server management

## 0.8.0
- Added menu handler

## 0.9.0
- Added documentation for debian server deployment

## 0.10.0
- Added middleware layer for  messages rate limiting

## 0.11.0
- Added user account subscription handlers, now the telegram user is saved in a mongodb collection

## 0.12.0
- Added authorization middleware and added admin handler for approving new users

## 0.13.0
- Added EventEmitting system for notifications

## 0.14.0
- Changed application boot up, Code Refactor, Added basic loggin to bot controller

## 0.15.0
- Added Scraping templates and its service, code refactoring

## 0.16.0
- Added scraping container, created scraping service, added website register for url building

## 0.17.0
- Added exception middleware, added some logging

## 0.18.0
- Updated SearchParamsHandlers to complete url building for immobiliare.

## 0.19.0
- Added handler for setting preferred language, added preferred language to state, now the user has a session state of 5 mins

### 0.19.1
- patched bug default language not set

### 0.19.2
- Fixed user authentication in order to whitelist /subscribe command

## 0.20.0
- Fixed State problems bugs 2024/07/21.1 and 2024/07/21.2

## 0.21.0
- Added scraping logic for immobiliare, completed tasks 2024/07/23 1,2

## 0.22.0
- Added notification for new subscription, completed task 2024/07/27.1

## 0.23.0
- Added choices for only rooms rental and houses for sales, Tasks 2024/07/27.2,3

## 0.24.0
- Created event_loop in the core container and now passed when needed so that http client and telegram share the same event loop. Tasks_NewBugsIntroducing_2024/07/30_1

## 0.25.0
- Added specific error handlers, Tasks_BugsFixing_2024/07/30_1

## 0.26.0
- Added go to previous step button to search params handler, Tasks_NewBugsIntroducing_2024/07/31_1, CodeRefactor

## 0.27.0
- Added button for stopping listings posting, Tasks_NewBugsIntroducing_2024/07/30_2.1

## 0.28.0
- Added menu buttons and managed handlers for different languages, Tasks_NewBugsIntroducing_2024/08/01_2

## 0.29.0
- Reworked template loaders for telegram, now created dynamically at startup with a controller and can be accessed throught a dict using keys, Tasks_NewBugsIntroducing_2024/08/05_1

## 0.30.0
- Reworked error handling system, now inheritance is used through a centralized error_handler, Tasks_NewBugsIntroducing_2024/08/06_1

## 0.31.0
- Added DaoControllerService, now all daos are loaded dynamically at startup and are injected when needed. Tasks_NewBugsIntroducing_2024/08/05_2

## 0.32.0
- Added handlers to store and use user search parameters for the search, added new exception handler for dao operations, even_emitter now saves telegram message and query handlers, Tasks_NewBugsIntroducing_2024/08/01_1

## 0.33.0
- Fixed show search filters to handle case where no search filters are saved, Tasks_2024/08/22_1

