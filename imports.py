import customtkinter
from PIL import Image
import os
from os import walk
import pandas as pd
import requests
import websockets
import asyncio
import json
import time
from time import gmtime, strftime
import numpy as np
import statsmodels.api as sm
import warnings
from binance.um_futures import UMFutures
from config import *
warnings.filterwarnings("ignore")
import threading
import tkinter 
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup as bs
import speedtest
from pythonping import ping
from models.treayd_historical import DEPOSIT,LEVERAGE,MYDIR_COIN,MYDIR_WORKER,VOLUME
import math


from websockets import connect
