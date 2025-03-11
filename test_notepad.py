import unittest
from pywinauto import Desktop, Application
import time

class CalculatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup: Start or Connect to Calculator"""
        cls.app = Application(backend="uia").start('calc.exe')
        time.sleep(2)  # Allow time for the calculator to launch
        cls.dlg = Desktop(backend="uia").Calculator

    @classmethod
    def tearDownClass(cls):
        """Cleanup: Close Calculator"""
        cls.app.kill()

    def get_result(self):
        """Retrieve result from Calculator"""
        try:
            # Use print_control_identifiers() output to confirm correct element
            result_element = self.dlg.child_window(auto_id="CalculatorResults", control_type="Text")
            result_element.wait('visible', timeout=5)  # Wait until visible
            result_text = result_element.window_text().replace("Display is ", "").strip()
            return result_text
        except Exception as e:
            print(f"Error retrieving result: {e}")
            return None  # Return None instead of failing the test

    def test_multiplication(self):
        """Test: 2 * 3 = 6"""
        self.dlg.type_keys('2*3=')
        time.sleep(1)
        result = self.get_result()
        self.assertEqual(result, "6", "Multiplication Test Failed!")

    def test_addition(self):
        """Test: 5 + 4 = 9"""
        self.dlg.type_keys('5+4=')
        time.sleep(1)
        result = self.get_result()
        self.assertEqual(result, "9", "Addition Test Failed!")

    def test_subtraction(self):
        """Test: 8 - 3 = 5"""
        self.dlg.type_keys('8-3=')
        time.sleep(1)
        result = self.get_result()
        self.assertEqual(result, "5", "Subtraction Test Failed!")

    def test_division(self):
        """Test: 9 ÷ 3 = 3"""
        self.dlg.type_keys('9/3=')
        time.sleep(1)
        result = self.get_result()
        self.assertEqual(result, "3", "Division Test Failed!")

if __name__ == "__main__":
    unittest.main()
