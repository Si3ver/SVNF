#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, random, math
import argparse
import numpy as np

serversList = {'1671': 88137.64, '1672': 88137.64, '1673': 88137.64, '1674': 88137.64, '1675': 88137.64, '1676': 88137.64, '1677': 88137.64, '1678': 88137.64, '1679': 88137.64}
mips = 3573

maxNo = -1
maxScore = -1
for no,score in serversList.items():
    if score > maxScore:
        maxScore = score
        print('---', score, maxScore)
