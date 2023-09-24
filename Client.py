import socket
import argparse
import uuid
import threading



class Client:
  def __init__(self, ClientID, ClientSocket):
    self.ClientID = ClientID
    self.ClientSocket = ClientSocket

  def myfunc(self):
    print("Hello my name is " + self.name)
