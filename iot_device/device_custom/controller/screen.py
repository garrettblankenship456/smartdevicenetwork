# Holds the class to control all the buttons and screen application

# Imports
from graphics import *
import time

# Class definition
class Screen:
    """Controls all the buttons and button definitions"""
    def __init__(self, xSize:int, ySize:int):
        """Main initializer"""
        # Create window
        self.window = GraphWin("Controller", xSize, ySize)

        # Remove title bar
        self.window.master.overrideredirect(True)

        # Initialize custom title
        title = Text(Point(65, 20), "Smart home")
        title.setSize(16)
        title.draw(self.window)

        # Initialize buttons
        self.buttons = []

    def drawButtons(self):
        """Draws all the buttons to the screen"""
        # Get row and column
        row = 0
        column = 0

        # Loop through each button
        for i in range(len(self.buttons)):
            # Get button to modify
            button = self.buttons[i]

            # Create shape for each button
            button.shape = Rectangle(Point(10 + 50 * column, 50 + 50 * row), Point(50 + 50 * column, 90 + 50 * row))
            button.text = Text(button.shape.getCenter(), button.name)

            # Draw the button shape
            button.shape.draw(self.window)
            button.text.draw(self.window)

            # Increment row and or column
            column += 1

            if column > self.window.getWidth() // 60:
                column = 0
                row += 1

    def undrawButtons(self):
        """Undraw all the buttons"""
        for button in self.buttons:
            # Undraw and remove the shape
            button.shape.undraw()
            button.text.undraw()
            button.shape = None
            button.text = None

    def addButton(self, button):
        """Adds a button to be drawn with the name type and function given"""
        self.undrawButtons()
        self.buttons.append(button)
        self.drawButtons()

    def delButton(self, name:str):
        """Deletes a button by name"""
        self.undrawButtons()

        # Loop through each button remove if name matches
        for i in range(len(self.buttons)):
            # Check name
            if self.buttons[i].name == name:
                # Remove it
                self.buttons.pop(i)
                break

        self.drawButtons()

    def checkClick(self, clickPos):
        """Returns true or false and executes function depending on if the button has been clicked with the position given"""
        # Declare variables to make it easier to work with
        x = clickPos.getX()
        y = clickPos.getY()

        # Check values to every button
        for button in self.buttons:
            # Get button data
            xPos1 = button.shape.getP1().getX()
            yPos1 = button.shape.getP1().getY()
            xPos2 = button.shape.getP2().getX()
            yPos2 = button.shape.getP2().getY()

            # Compare data
            if x > xPos1 and x < xPos2:
                if y > yPos1 and y < yPos2:
                    # Its been pressed
                    button.use()

                    return True

        # None ended execution so no buttons were pressed, return false
        return False

# Parent class for buttons
class Button:
    def __init__(self, name:str):
        # Initialize
        self.name = name
        self.shape = None
        self.text = None

    # Use function
    def use(self):
        # Overriden function
        pass

# Children classes for buttons and the different types
class Push(Button):
    """Push button, executes one function when pressed"""
    def __init__(self, name:str, function):
        # Initialize
        super().__init__(name)
        self.function = function

    # Define the use
    def use(self):
        # Call the function
        self.function()

class Toggle(Button):
    """Toggle button, two functions executed one for on and one for off"""
    def __init__(self, name:str, onFunction, offFunction, initalState:bool = False):
        # Initialize
        super().__init__(name)
        self.onFunction = onFunction
        self.offFunction = offFunction

        # Save state
        self.state = False

    # Define the use
    def use(self):
        # Declarations
        success = None

        # Call the function based on the state
        if self.state:
            success = self.offFunction()
        else:
            success = self.onFunction()

        # Toggle state if the commands were successful
        if success:
            self.state = not self.state


# Test function
def testFunc():
    print("Hello world")
    return True

def onFunc():
    print("On fucntion")
    return True

def offFunc():
    print("Off function")
    return True

if __name__ == "__main__":
    # Create new class and run it
    s = Screen(600, 350)

    s.addButton(Push("test", testFunc))
    s.addButton(Toggle("toggle", onFunc, offFunc))

    while True:
        cPos = s.window.getMouse()
        s.checkClick(cPos)

    s.window.getMouse()