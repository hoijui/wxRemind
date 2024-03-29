# wxRemind

*version 0.6.18 - 2006-07-03*

*wxRemind* is a graphical front-end to [Remind], a remarkably sophisticated
calendar and alarm system. *wxRemind* is similar to [Wyrd] but is based on
[wxPython] rather than curses. The display features a calendar and daily
event list suitable for visualizing your schedule at a glance. Dates and
associated events can be quickly selected either with the mouse or cursor
keys, and dates in the calendar are color coded to reflect the total
duration of scheduled events. *wxRemind* provides an internal editor or
integrates with an external editor of your choice to make editing of
reminder files more efficient, provides hotkeys to quickly access the most
common Remind options, allows popup, sound and/or spoken alerts and can
display a postscript calendar of the selected month suitable for printing.

## Requirements

The latest version of *wxRemind* should be available at [wxRemind].

You need:

* `remind`
* `python >= 2.3`
* `wxPython >= 2.6.1`

For me (Centos 4 and python 2.3), installing `wxPython` required:

* `wxPython2.6-common-gtk2-unicode-2.6.3.0-fc2_py2.3.i386.rpm`
* `wxPython2.6-gtk2-unicode-2.6.3.0-fc2_py2.3.i386.rpm`

Note: `analogclock` is a recent addition to `wxPython` (2.6.3)
and is required for *wxRemind*.
A copy has been included in this distribution under the `wxWidgets` license
for the convenience of those with earlier versions of `wxPython` already installed.

Displaying monthly postscript calendars requires `ggv` (gnome ghostview).

Audible, spoken-message alerts require [Festival].

## Installation Alternatives

Follow one of the following alternatives.

### 1) Using `INSTALL`

Unpack the contents of the `wxRemind.tgz` in a convenient location,
open a terminal window and then at a command prompt
(not as root but as yourself):

```bash
cd <path to wxRemind directory>
python INSTALL
```

and follow the instructions.

This script prompts for a directory in your PATH
and then creates symbolic links for the wxRemind executables
(`wxremind`, `wxremalert`, `wxremdata` and `wxremsetup`) in that directory.
The link to `wxremalert` is necessary for remind to be able to use it for alerts.
The other links are for convenience.

Using `INSTALL` has the following advantages:

1. It does not require root privileges.
2. It leaves your python tree untouched.
	To remove *wxRemind*, simply delete the directory where it was unpacked
	and the three symbolic links created by `INSTALL`.
3. It runs on a wide variety of platforms without tweaking.
	Since the package files are in a sub-directory of the root directory
	where the scripts are located,
	the scripts can automatically find the package files ON ANY PLATFORM,
	without further intervention.

Proceed to [Post Installation](#post-installation).

### 2) Using `setup.py` (usually requires root privileges)

Unpack the contents of the `wxRemind.tgz` in a convenient location,
open a terminal window and then at the command prompt (as root):

```bash
cd <path to wxRemind directory>
python setup.py install
```

This will create an *egg* (a compressed ZIP file) and install it in the python tree,
usually under site-packages,
and install the scripts in your system PATH, usually in `/usr/bin/`.

Proceed to [Post Installation](#post-installation).

### 3) Using Easy Install (usually requires root privileges)

You do not need to download the tarball if you use this alternative.

Download [ez_setup.py], and run it;
this will download and install the appropriate `setuptools` egg for your Python version.
An easy_install script will be installed in the normal location for Python scripts on your platform.

Then at the command prompt (as root):

```bash
easy_install wxRemind
```

This will download and install the *egg* in the python tree.

Proceed to [Post Installation](#post-installation).

## Post Installation

At a command prompt not as root but as yourself:

```bash
wxremsetup
```

and follow the instructions. This configuration process will check for
sufficiently recent versions of `python` and `wxPython`, for the presence
of `remind`, `festival`, `ggv` and `play` in your system path and for the
existence of the default alert sound file.

It will then create `.wxremfloat` in your home directory, overwriting any
existing file. The contents of this file will make it possible for you to
use floating reminders.

Next it will check for the existence of `.reminders` and `.wxremindrc` in
your home directory. If `.reminders` exists it will be checked to make
sure that it contains an `include .wxremfloat` line. If it does not, first
a backup will be made named `.reminders.bak` and then the appropriate line
will be inserted at the beginning of the original file. If `.reminders`
does not exist, then it will be created with the necessary line as its
only content.

A new configuration file will then be created called `.wxremindrc` if this
file does not already exist and `.wxremindrc.new` otherwise. This file will
automatically contain the correct settings for `remind`, `festival`, `ggv`
and `play` and, of course, for `reminders` and `wxremfloat`.

Finally, a report of messages generated during configuration will be displayed.

**IMPORTANT**
If created by the configuration process,
it is strongly recommended that you edit `~/.wxremindrc.new`
to reflect any custom settings that you may have made in your existing `~/.wxremindrc`,
and then save `~/.wxremindrc.new` as `~/.wxremindrc`.

You can now run *wxRemind* by opening a terminal window and entering

```bash
wxremind
```

Once *wxRemind* is running, pressing `?` will bring up a display of usage
information.

```
   wxRemind (python package) Files

   wxRemAbout.py
           About page.

   wxRemAlert.py
           Used by default to produce popup/sound alerts for reminders
           triggered by remind. The default behavior can be set in
           wxRemConfig.py.

   wxRemConfig.py
           Color and other customizations. User specific customizations in
           ~/.wxremindrc override the settings in this file.

   wxRemData.py
           Provides the interface to remind.

   wxRemEdit.py
           Dialogs for creating new reminders.

   wxRemEditor.py
           Provides the internal editor.

   wxRemHelp.py
           Help page.

   wxRemHints.py
           Hints for creating reminders.

   wxRemind.py
           provides the main GUI interface.

   wxRemSetup.py
           Configuration procedures.

   wxRemSplash.py
           Splash page.

   wxRemVersion.py
           wxRemind version information.

  wxRemind scripts

   wxremind
           Used to start wxRemind at the command prompt. Takes no arguments.

   wxremdata
           Returns day schedule as console output. Optional YYYY MM DD date
           argument, defaults to today.

   wxremalert
           Produces an alert. Details in wxRemConfig.py. Can be used
           independently of wxRemind and remind.

   INSTALL, wxremsetup
           Used for dependency checks and configuration.
```

## License

```
   Copyright (c) 2006 Daniel A. Graham <[daniel.graham@duke.edu]>

   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the Free
   Software Foundation (www.gnu.org/licenses/gpl.html); either version 2 of
   the License, or (at your option) any later version. This program is
   provided in the hope that it will be useful, but without any warranty;
   without even the implied warranty of merchantability or fitness for a
   particular purpose. Details are provided in the included COPYING file.
```

[Remind]: http://www.roaringpenguin.com/penguin/open_source_remind.php
[Wyrd]: http://www.eecs.umich.edu/~pelzlpj/wyrd
[wxPython]: http://www.wxpython.org/
[wxRemind]: http://www.duke.edu/~dgraham/wxRemind
[Festival]: http://www.cstr.ed.ac.uk/projects/festival
[ez_setup.py]: http://peak.telecommunity.com/dist/ez_setup.py
[daniel.graham@duke.edu]: mailto:daniel.graham@duke.edu
