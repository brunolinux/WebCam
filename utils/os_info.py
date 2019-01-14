#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os 

def isARMOS():
    return ( os.uname()[4][:3] == 'arm' ) 

