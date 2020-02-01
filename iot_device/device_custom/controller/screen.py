# Holds the class to control all the buttons and screen application

# Imports
from graphics import *
import time

# Config
BUTTON_SIZE_X = 80
BUTTON_SIZE_Y = 40
BUTTON_PADDING = 10

# Class definition
class Screen:
    """Controls all the buttons and button definitions"""
    def __init__(self, xSize:int, ySize:int):
        """Main initializer"""
        # Create window
        self.window = GraphWin("Controller", xSize, ySize)

        # Remove title bar
        self.window.master.overrideredirect(True)   
        self.window.master.geometry("+0+0")

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

            # Draw the button shape
            button.shape.draw(self.window)
            button.text.draw(self.window)

            if button.gridAligned:
                # Set button position
                button.setPos(10 + (BUTTON_SIZE_X + BUTTON_PADDING) * column, 50 + (BUTTON_SIZE_Y + BUTTON_PADDING) * row)

                # Increment row and or column
                column += 1

                if column >= self.window.getWidth() // (BUTTON_SIZE_X + BUTTON_PADDING):
                    column = 0
                    row += 1

    def undrawButtons(self):
        """Undraw all the buttons"""
        for button in self.buttons:
            # Undraw and remove the shape
            button.shape.undraw()
            button.text.undraw()

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

    def press(self):
        """Runs checkClick after getting a keypress"""
        cPos = self.window.getMouse()
        self.checkClick(cPos)

# Parent class for buttons
class Button:
    def __init__(self, name:str, gridAligned:bool):
        # Initialize
        self.name = name
        self.shape = Rectangle(Point(0, 0), Point(BUTTON_SIZE_X, BUTTON_SIZE_Y))
        self.text = Text(self.shape.getCenter(), name)
        self.gridAligned = gridAligned

        # Set colors
        self.shape.setFill("white")

    # Draw function
    def draw(self, window):
        self.shape.draw(window)
        self.text.draw(window)

    # Set position function
    def setPos(self, x, y):
        """Sets position of the button on the screen"""
        # Get current position
        curX = self.shape.getP1().getX()
        curY = self.shape.getP1().getY()

        # Move to new position
        self.shape.move(x - curX, y - curY)
        self.text.move(x - curX, y - curY)

    # Use function
    def use(self):
        # Overriden function
        pass

# Children classes for buttons and the different types
class Push(Button):
    """Push button, executes one function when pressed"""
    def __init__(self, name:str, function, gridAligned:bool = True):
        # Initialize
        super().__init__(name, gridAligned)
        self.function = function

    # Define the use
    def use(self):
        # Set color of button to be a slightly grayed out
        self.shape.setFill(color_rgb(180, 180, 180))

        # Call the function
        self.function(self.name)

        # Return color
        self.shape.setFill("white")

class Toggle(Button):
    """Toggle button, two functions executed one for on and one for off"""
    def __init__(self, name:str, onFunction, offFunction, initalState:bool = False, gridAligned:bool = True):
        # Initialize
        super().__init__(name, gridAligned)
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
            self.shape.setFill("white")
            success = self.offFunction(self.name + "_off")
        else:
            self.shape.setFill(color_rgb(180, 180, 180))
            success = self.onFunction(self.name + "_on")

        # Toggle state if the commands were successful
        if success:
            self.state = not self.state
