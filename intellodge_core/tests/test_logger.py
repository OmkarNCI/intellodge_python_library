# tests/test_logger.py
import unittest
from intellodge_core.logger import get_logger

class LoggerTestCase(unittest.TestCase):
    def test_logger(self):
        logger = get_logger("test")
        logger.info("Logger is working")

if __name__ == "__main__":
    unittest.main()
