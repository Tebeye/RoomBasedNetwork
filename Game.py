import socket
import argparse
import uuid
import threading
import Client


class Game:
    def __init__(self, GameID, lst=None):
        self.GameID = GameID
        if lst is None:
            lst = []
        self.lst = lst

    def AddClientIntoGame(self, myClient):
        self.lst.append(myClient)

    def initializeTheGame(self, GameID):
        if len(self.lst) != 2:
            return False
        
        return all(client.GameID == GameID for client in self.lst)
