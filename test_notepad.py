import unittest
from pywinauto import Desktop, Application
import time
import win32gui
import win32con

# Helper function to restore Calculator if minimized
def restore_window(window_name):
    def callback(hwnd, extra):
        if window_name in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.EnumWindows(callback, None)
    time.sleep(2)  # Allow UI elements to reload

class CalculatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup: Start or Connect to Calculator"""
        try:
            cls.app = Application(backend="uia").connect(title="Calculator")
        except:
            cls.app = Application(backend="uia").start("calc.exe")
            time.sleep(2)

        cls.dlg = Desktop(backend="uia").Calculator

    @classmethod
    def tearDownClass(cls):
        """Cleanup: Close Calculator"""
        try:
            cls.dlg.child_window(title="Close Calculator", auto_id="Close", control_type="Button").click()
            print("Calculator closed.")
        except:
            print("Calculator was already closed or not found.")

    def setUp(self):
        """Ensure Calculator is visible before each test"""
        restore_window("Calculator")
        self.dlg.set_focus()
        time.sleep(1)

    def test_multiplication(self):
        """Test: 7 × 5 = 35"""
        dlg = self.dlg
        dlg.child_window(title="Seven", auto_id="num7Button", control_type="Button").wait('exists', timeout=5).click()
        dlg.child_window(title="Multiply by", auto_id="multiplyButton", control_type="Button").click()
        dlg.child_window(title="Five", auto_id="num5Button", control_type="Button").click()
        dlg.child_window(title="Equals", auto_id="equalButton", control_type="Button").click()
        time.sleep(1)

        result_element = dlg.child_window(auto_id="CalculatorResults", control_type="Text")
        self.assertIn("35", result_element.window_text(), "Multiplication Test Failed!")
        print("Multiplication Test Passed!")

    def test_division(self):
        """Test: 8 ÷ 2 = 4"""
        dlg = self.dlg
        dlg.child_window(title="Eight", auto_id="num8Button", control_type="Button").click()
        dlg.child_window(title="Divide by", auto_id="divideButton", control_type="Button").click()
        dlg.child_window(title="Two", auto_id="num2Button", control_type="Button").click()
        dlg.child_window(title="Equals", auto_id="equalButton", control_type="Button").click()
        time.sleep(1)

        result_element = dlg.child_window(auto_id="CalculatorResults", control_type="Text")
        self.assertIn("4", result_element.window_text(), "Division Test Failed!")
        print("Division Test Passed!")

    def test_subtraction(self):
        """Test: 9 - 4 = 5"""
        dlg = self.dlg
        dlg.child_window(title="Nine", auto_id="num9Button", control_type="Button").click()
        dlg.child_window(title="Minus", auto_id="minusButton", control_type="Button").click()
        dlg.child_window(title="Four", auto_id="num4Button", control_type="Button").click()
        dlg.child_window(title="Equals", auto_id="equalButton", control_type="Button").click()
        time.sleep(1)

        result_element = dlg.child_window(auto_id="CalculatorResults", control_type="Text")
        self.assertIn("5", result_element.window_text(), "Subtraction Test Failed!")
        print("Subtraction Test Passed!")

    def test_square_root(self):
        """Test: √16 = 4"""
        dlg = self.dlg
        dlg.child_window(title="One", auto_id="num1Button", control_type="Button").click()
        dlg.child_window(title="Six", auto_id="num6Button", control_type="Button").click()
        dlg.child_window(title="Square root", auto_id="squareRootButton", control_type="Button").click()
        time.sleep(1)

        result_element = dlg.child_window(auto_id="CalculatorResults", control_type="Text")
        self.assertIn("4", result_element.window_text(), "Square Root Test Failed!")
        print("Square Root Test Passed!")

    def test_minimize_restore(self):
        """Test: Minimize and Restore Calculator"""
        dlg = self.dlg
        dlg.minimize()
        restore_window("Calculator")

        # Reconnect after restoring
        self.app = Application(backend="uia").connect(title="Calculator")
        dlg = self.app.Calculator
        self.assertIsNotNone(dlg, "Restore Test Failed!")
        print("Minimize & Restore Test Passed!")


if __name__ == "__main__":
    unittest.main()
