import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

wxRemDescription = \
"""wxRemind is a wxPython-based front-end for Remind, a powerful calendar and
alarm application. The display features a calendar and daily event list
suitable for visualizing your schedule at a glance. Dates and associated events
can be quickly selected either with the mouse or cursor keys, and dates in the
calendar are color coded to reflect the total duration of scheduled events.
wxRemind integrates with an external editor of your choice to make editing of
reminder files more efficient, provides hotkeys to quickly access the most
common Remind options and supports visual, sound and/or spoken alerts."""

wxRemClassifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Desktop Environment :: Gnome',
    'Topic :: Desktop Environment :: K Desktop Environment (KDE)',
    'Topic :: Office/Business :: Scheduling'
    ]

setup(
    name = "wxRemind",
    version = "0.6.11",
    packages = find_packages(),
    scripts = ['wxremdata', 'wxremalert', 'wxremind', 'wxremsetup'],
    author = "Daniel A. Graham",
    author_email = "daniel.graham@duke.edu",
    description = "A wxPython based GUI for Remind",
    long_description = wxRemDescription,
    classifiers = wxRemClassifiers,
    license = "GPL",
    platforms = ['Any'],
    download_url = "http://www.duke.edu/~dgraham/wxRemind/wxRemind-current.tar.gz",
    url = "http://www.duke.edu/~dgraham/wxRemind",
    keywords = "calendar alarm schedule appointments",
    data_files = [ ('', ['CHANGES', 'COPYING', 'INSTALL', 'README'])],
)
