# Blight Discord Bot Documentation


## Overview


This discord bot manages the blight discord server's applications, verification, role syncing and more.

While all important aspects of the bot have their own section, here is a brief overview of the bot:

- ``main.py`` is the main file and starts the bot.
- ``databaseManager.py`` manages the database.
- ``hypixelAPI.py`` manages api calls.
- The ``cogs`` folder contains all of the bots cogs, which contain most of the bot's logic/features.


## Design & Structure


### Database

The database is managed by the ``databaseManager.py`` file. To manage the database, this project uses the ``sqlalchemy`` library along with ``MySQL``.

As member, channel, role and guild id's in discord.py are integers, the BigInteger data type is used to store these values within the database. While this might not be the most storage-efficient practice, it prevents issues that may be caused by the values being different types.

_Below are tables listing the tables within the database and their contents, keep in mind that these tables may be difficult to read without a markdown interpreter._


**MEMBERS**

| discordID | uuid | username |
| :-------- | :--: | -------: |
| BigInteger | String(36) | String(16) |

This table is used to store registered members. In this table, the primary key is ``discordID``, with the secondary key being ``uuid``.  


**GUILD**

_Because of the large size of this table, it will be split into multiple grids for display purposes, just keep in mind that they are all part of the same table with 1 primary key._

| guildID    | guildName  | staffRole  | adminRole  | 
| ---------- | ---------- | ---------- | ---------- |
| BigInteger | String(36) | BigInteger | BigInteger |

| guestRole | guildMemberRole | unverifiedRole | acceptedRole | mvpRole | developerRole |
| --------- | --------------- | -------------- | ------------ | ------- | ------------- |
| BigInteger | BigInteger | BigInteger | BigInteger | BigInteger | BigInteger |

| logChannel | messageLogChannel | waitingListChannel | applicationSubmissionsChannel |
| ---------- | ----------------- | ------------------ | ----------------------------- |
| BigInteger | BigInteger | BigInteger | BigInteger |

| monitoredGuilds | weekOneGexp | weekTwoGexp | weekThreeGexp | apiKey |
| --------------- | ----------- | ----------- | ------------- | ------ |
| String(999) | JSON | JSON | JSON| String(36)


This table is used to store all relevant info about the bot's configuration within the server, with permissions being loaded from the relevant fields upon startup. The bot is currently only designed to work within 1 server, however it is possible to make the bot multi-server in the future with this setup. The primary key of this table is ``guildID``.


**TICKETS**

| channelID | guildID | ownerID | panel |
| :-------: | :-----: | :-----: | :---: |
| BigInteger| BigInteger | BigInteger | String(36) |

This table is used to store tickets. At the time of writing, the only feature that uses this table is guild applications, however more uses can be added. The ``channelID`` field is the primary key.

When a ticket is created, the ``panel`` field can be used to determine which category to create the ticket in, this can be done by checking the PANELS table. If there is no panel found within the PANELS table, the ticket should be created outside of a category.


**PANELS**

| guildID | categoryID | panelName |
| :-----: | :--------: | :-------: |
| BigInteger | BigInteger | String(36) |

This table exists only to determine which discord category a ticket should be created in. As the bot only exists in one server, ``panelName`` can be used to identify any individual record, however if this changes then ``guildID`` can be used with ``panelName`` as composite keys.


**MEMBERGEXPHISTORY**

| uuid | username | thisWeekGexp | weekOneGexp | weekTwoGexp | weekThreeGexp |
| :--: | :------: | :----------: | :---------: | :---------: | :-----------: |
| String(36) | String(16) | JSON | JSON | JSON | JSON |

This table is currently unused, but exists to allow guild member activity tracking in the future. In this table, ``uuid`` is the primary key. 

To store a member's gexp, 


### Hypixel API

The bot relies on using both the hypixel api and mojang api. Currently, all api calls are managed by ``hypixelAPI.py``. This file contains a class that is used throughout the bot. For maintainability purposes, do not write any functions that make api calls outside of this class.

Keep in mind that the api key is stored within the database.


### Config

The ``config.py`` file contains some misc information about the bot, such as its token. This file is used to store information that is either too sensitive to be stored in the database, or not stored in the database due to the lack of a need for non-developers to access it.


## Logging

The ``devLogging.py`` file contains a class used by the bot to log events that occur. Currently the bot has a different levels of logging, including ``info``, ``warn``, ``error``, ``event`` and ``database``. These functions will send their own colour coded message to console, with an argument to include what module (file) logged the event. Keep in mind that this feature only logs to the console, making these logged events only available to developers.

The convention of this logging system is:

- ``info`` is for generic information that doesn't fit into any other category, but is important enough to get logged.

- ``warn`` is for when the bot encounters a non-critical error. An example of this would be an api call timing out.

- ``error`` is for critical errors that will prevent the bot from functioning. This includes failing to load role/channels upon startup, the api key being returned as invalid or the database credentials being returned as invalid.

- ``event`` is for logging user events, such as the application/verification buttons being pressed.

- ``database`` is for database events, such as a member or ticket being registered.

_As of the time of writing, this functionality is not fully implemented throughout the bot, as such many events that should be logged are not. This is across all of the categories of logging._


### Cogs

All cogs are stored within the cogs folder. Upon startup, the bot will attempt to load every _python_ file within the cogs folder as a cog. Each cog controls one aspect of the bot and should be removable without preventing any other cogs from functioning. 

Each cog has its own function for checking command permissions, these are named ``permission_check`` for interaction commands and ``legacy_permission_check`` for context commands (also known as prefix commands).


**Applications**


**Developer_Commands**

This cog contains commands designed for developer/admin use. With the exception of ``/lookup``, ``/ping`` and ``/status``, all commands within this cog require users to have either the ``developerRole`` or the ``adminRole``.

Currently, the most important commands within this cog are:

- ``/setup`` This command creates a record within the ``GUILD`` table of the database.

- ``/set-<role>-role`` Each registered role within the database has its own version of this command. The command sets the registered role to one specified by the user.

- ``/set-<channel>-channel`` Each registered channel within the database has its own version of this command. The command sets the registered channel to one specific by the user.

- ``/set-api-key`` This command sets the registered api key within the database. This api key is necessary to access the hypixel api.

- ``/lookup`` This command will send a query to the database for a member with a specific ``discordID``. If a member is found, it will respond with the member's ``discordID``, ``uuid`` and ``username``.

- ``/ping`` This command will respond with the bot's latency.

- ``/status`` This command will check that both the hypixel api and the database respond to calls without throwing an error. Additionally it will check how many players are in the in-game guild and how many users are registered within the database.

- ``b!eval`` This command executes a block of code entered by the user. Only one code block can be used.


**Games**

This cog is within the ``games.py`` file. Holding mostly context commands, this cog is for public entertainment commands/events, an example being ``b!duck``.

As all commands in this cog are non-critical and are available through the ``b!help`` command, I will not list them here.

**Leaderboards**

This cog is not currently used.

**Logging**

This cog is in the ``logging.py`` file. It is made up of event listeners. Currently, these event listeners only include message events such as deletes and edits. When one of these events occurs, it is sent to the ``messageLogChannel``.

**Moderation**

This cog is in the ``moderation.py`` file. It contains commands related to moderation and managing the server. All commands within this cog require the user to have either the ``staffRole``, ``adminRole`` or ``developerRole``.

- ``/purge`` This command deletes a number of messages determined by the user.

- ``/role`` This command toggles a specified role from a specified user. If the user has the role, it removes it, if the user doesn't have the role, the role is given. Users of this command cannot give/remove their highest role or above with this command.

- ``/kick`` This command kicks a member from the server. Users of this command cannot kick members with their highest role or above with this command.

- ``/kick`` This command kicks a member from the server. Users of this command cannot kick members with their highest role or above with this command.

- ``/mute`` This command times out a user for a specified amount of time. Users of this command cannot mute members with their highest role or above with this command.

- ``/poll`` This command sends a poll with at least 2 options. Options are made by placing the ``~`` character between options within the options field. The bot will auto react for each option.

- ``/forcelink`` This command will register a user within the database. A _valid_ username must be provided with this command, however the standard verification check is skipped with this command. This command will also apply the appropriate roles based on the username.

**Role_Syncing**

This cog is in the ``role_syncing.py`` file. It is used to ensure that all registered members have the appropriate roles based off of their guild position. Currently, the cog will start the role sync process every time a message is sent if the process is not already running.

The only command within this cog is ``/sync``, which can be used by any registered member as a way to gain the appropriate roles without waiting for the automatic role sync system. Ideally, a member will never have to use this command.

**Tickets**

This cog is in the ``tickets.py`` file. Currently, this cog contains no important features, with its only command being ``/create-panel``. The ``/create-panel`` command creates a new panel within the ``PANELS`` database table, which is currently unused.

**Verification**
