import unittest
from multiprocessing import Process
from threading import Timer

import main


class MyTestCase(unittest.TestCase):
    def test_connect(self):
        self.main = main
        self.connect = Process(target=self.connect)
        m = Timer(5.0, self.sendMockMessage)

        self.connect.start()
        m.start()

    def connect(self):
        self.main.main()

    def sendMockMessage(self):
        if not self.connect.is_alive():
            self.fail("Unable to connect to slack!")

        m = MockMessage()
        self.main.hi(m)
        self.assertEqual(m.text, 'Hi!')
        self.assertEqual(m.emoji, '+1')

        self.connect.terminate()

class MockMessage():
    def __init__(self):
        self.text = ''
        self.emoji = ''

    def reply(self, text):
        self.text = text

    def react(self, emojiname):
        self.emoji = emojiname


if __name__ == '__main__':
    unittest.main()
