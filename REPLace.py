#!/usr/bin/python3


# Uses a serial connection to REPL to copy dirs/files to a MicroPython instance.
# This is slow. It's just auto-writing Python commands to the REPL connection.


# This REQUIRES the pyserial module: sudo pip3 install pyserial
# Add your username to dialout: sudo adduser username dialout
# You have to log out and back in or reboot after changing dialout.

port = '/dev/cu.usbserial-0001'

# file_system_dir folder becomes the root directory on microprocessor
# If None, root directory will be current working directory
file_system_dir = None

# Any directory or file whose basename matches an item in "excludes"
# will not be copied to the MicroPython instance. So, you can run this
# script from the file_system_dir folder.

excludes = ['REPLace.py',
            'archive',
            'bin',
            '.git',
            'reference',
            ]

# FOR FILES: This is the opposite of excludes. If you list basenames here, then only
# matches to these basenames will be loaded. You can use this if you are
# editing only a few files.

includes = []
includes.append('boot.py')
includes.append('main.py')
includes.append('button.py')

# The following variable reduces upload size.
# If True, this removes blank lines, comments, and right-side whitespace.
# This is not a very smart process.
# It removes the last # in a line and everything after it.
# If a text # is in the line, put a comment # at the end of the line (level 3).
# DO NOT use this if you have blocks of text where blank lines are significant.
# DO NOT use this if you have long text with # in it.

# remove extra space and comments
smash = True

# smash non.py files
smash_all = False

# just smash, don't load
smash_only = False

# leave smashed copy of file
smash_keep = False

# smash level
# 1 = blank lines,
# 2 = full comment lines,
# 3 = end comments
# if 3, and text # is in line, you must put a # at the end of the line
smash_level = 2

# Once you set the above variables, save and run this file.
# Make sure that nothing else is using the serial port.
# Watch the screen. You'll be able to see everything it does.

# Of course, you could import this, instantiate the uploader class,
# set the variables, and then run uploader().upload(). If you want.

# ----------------------------------------------------------------------------------
import os
import sys
import time
import re
import serial
import shutil


def run():

    uploader().upload()
    input('Press ENTER to close.')


class uploader:

    # fixed values
    baudrate = 115200
    timeout = 0.1
    fileblocksize = 1024
    rbuffer = ''

    def __init__(self):

        # port
        self.port = port
        if not self.port:
            self.port = '/dev/ttyUSB0'

        # local file system dir
        self.file_system_dir = file_system_dir
        if not self.file_system_dir:
            self.file_system_dir = os.getcwd()

        # excludes
        self.excludes = excludes
        if not self.excludes:
            self.excludes = []
        elif type(self.excludes) == str:
            self.excludes = excludes.split()
        self.excludes = set([os.path.basename(x) for x in self.excludes])

        # includes
        self.includes = includes
        if not self.includes:
            self.includes = []
        elif type(self.includes) == str:
            self.includes = includes.split()
        self.includes = set([os.path.basename(x) for x in self.includes])

    def upload(self):

        print('STARTING UPLOAD...')

        # Open connection
        if not smash_only:
            self.connection = serial.Serial(port=self.port,
                                            baudrate=self.baudrate,
                                            timeout=self.timeout)
            self.connection.flush()
            self.connection.write([3, 3])  # clear = ctrl-c
            # self.connection.write([4]) # soft reboot = ctrl-d
            self.recv(done=True)  # full read

            # imports
            self.send('import os')

        # Iterate through file system
        for root, dirs, files in os.walk(self.file_system_dir):

            # Exclude directories
            for x in dirs[:]:
                if x in self.excludes:
                    dirs.remove(x)

            # Exclude files
            for x in files[:]:
                if x in self.excludes:
                    files.remove(x)
                elif includes and x not in includes:
                    files.remove(x)

            # Sort directories, files
            dirs.sort()
            files.sort()

            # Directories which need creating
            if not smash_only:
                for d in dirs:
                    path1 = os.path.join(root, d)
                    path2 = path1.replace(self.file_system_dir, '').lstrip('/')
                    dirname, basename = os.path.split(path2)
                    if dirname:
                        self.send("if '{1}' not in os.listdir('{0}'): os.mkdir('{0}/{1}')".format(dirname,basename))
                    else:
                        self.send("if '{0}' not in os.listdir(): os.mkdir('{0}')".format(basename))
                    self.send()
                    self.send("print('LIST:','{0}',os.listdir('{0}'))".format(dirname))

            # Files in directories already created
            for file in files:

                # Create a temp file
                path1 = os.path.join(root, file)
                infile = open(path1)
                path2 = 'smash_'+file
                # smash files
                if smash and (smash_all or os.path.splitext(file)[1].lower() == '.py'):
                    outfile = open(path2, mode='w')
                    for line in infile:
                        line2 = line.strip()
                        if not line2:
                            pass
                        elif line2.startswith('#') and smash_level >= 2:
                            pass
                        elif '#' in line2 and smash_level >= 2:
                            outfile.write(line.rstrip().rsplit('#',1)[0]+'\n')
                        else:
                            outfile.write(line.rstrip()+'\n')
                    outfile.close()
                    infile.close()
                # don't smash
                else:
                    shutil.copyfile(path1, path2)

                # send temp file
                if not smash_only:
                    path3 = path1.replace(self.file_system_dir, '').lstrip('/')
                    self.send("outfile=open('{}',mode='wb')".format(path3))
                    infile = open(path2, mode='rb')
                    while 1:
                        data = infile.read(self.fileblocksize)
                        if not data:
                            break
                        self.send("outfile.write({})".format(data))
                    self.send("outfile.close()")

                # remove temp file
                if not (smash_only or smash_keep):
                    os.remove(path2)

        # Close connection
        if not smash_only:
            self.connection.write([3, 3])  # clear
            self.recv(done=True)  # full read
            self.connection.close()

        print('UPLOAD COMPLETE!')

    def replace_strings(self, match_object):
        return 'X' * len(match_object.group())

    def send(self, line=''):

        self.connection.write([ord(x) for x in line+'\r'])
        self.recv()

    def recv(self, done=False):

        # collect return from serial
        while 1:
            data = self.connection.read(1024)
            if not data:
                break
            else:
                self.rbuffer += data.decode(encoding='utf-8', errors='?')
        self.rbuffer = self.rbuffer.replace('\r', '')

        # print return lines
        while '\n' in self.rbuffer:
            i = self.rbuffer.index('\n')
            line = self.rbuffer[:i]
            self.rbuffer = self.rbuffer[i+1:]
            print(line)

        if done:
            print(self.rbuffer)


if __name__ == '__main__':
    run()
