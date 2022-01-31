import math as math
import tkinter as tk

RESOLUTION_X = 500
RESOLUTION_Y = 500

GRID_X = 10
GRID_Y = 10

SQUARE_WIDTH = None
SQUARE_HEIGHT = None

game_state = 0

mouse_x = None
mouse_y = None

session = None

class Grid_square:
    """
    Represents a single grid square in the grid.
    """
    def __init__(self, coordinates: (int, int)) -> None:
        """
        """
        self._coordinates = coordinates
        self._is_picked = False
        self._is_dead_end = False
        self._is_start = False
        self._is_end = False
        self._is_blocker = False

    def get_coordinates(self) -> (int, int):
        """
        Returns the grid square's coordinates.
        """
        return self._coordinates

    def get_is_picked(self) -> bool:
        """
        Returns if the grid square has been picked or not.
        """
        return self._is_picked

    def set_is_picked(self, setting) -> None:
        """
        Sets the grid square to be picked or not.
        """
        self._is_picked = setting

    def get_is_start(self) -> bool:
        """
        Returns if the grid square is the start or not.
        """
        return self._is_start

    def set_is_start(self, setting) -> None:
        """
        Sets the grid square to be the start square or not.
        """
        self._is_start = setting

    def get_is_end(self) -> bool:
        """
        Returns if the grid square is the end or not.
        """
        return self._is_end

    def set_is_end(self, setting) -> None:
        """
        Sets the grid square to be the end square or not.
        """
        self._is_end = setting

    def get_is_blocker(self) -> bool:
        """
        Returns if the grid square is a blocker or not.
        """
        return self._is_blocker

    def set_is_blocker(self, setting) -> None:
        """
        Sets the grid square to be a blocker.
        """
        self._is_blocker = setting

    def get_is_dead_end(self) -> bool:
        """
        Returns if the grid square is a dead end or not.
        """
        return self._is_dead_end

    def set_is_dead_end(self, setting) -> None:
        """
        Sets the grid square to be a dead end.
        """
        self._is_dead_end = setting

    def __repr__(self) -> None:
        """
        Returns the string representation of the grid square.
        """
        return f"Grid square {self._coordinates}"

class Grid:
    """
    Represents the entire grid. Is made of grid square objects.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        """
        self._width = width
        self._height = height
        self._grid = {}
        self._start_square_coordinates = None
        self._end_square_coordinates = None
        self._current_blockers = []
        self._current_rectangles = {}

        for row in range(width):
            for column in range(height):
                position = (row, column)
                self._grid[position] = Grid_square((row, column))

    def get_grid_square(self, coordinates: (int, int)) -> Grid_square:
        """
        Returns the grid square at the inputted coordinates.
        """
        return self._grid[(coordinates[0], coordinates[1])]

    def get_start_square(self) -> Grid_square:
        """
        Returns the grid square that is the start square.
        """
        if(not self._start_square_coordinates):
            # ERROR
            return "There is no start square."
        
        return self._grid[self._start_square_coordinates]

    def set_start_square(self, coordinates: (int, int)) -> None:
        """
        Sets the inputted square to be the start square.
        If applicable, overwrittes the old inputted start square.
        """
        if(self._start_square_coordinates):
            self._grid[self._start_square_coordinates].set_is_start(False)
        
        self._start_square_coordinates = coordinates
        self._grid[self._start_square_coordinates].set_is_start(True)

    def get_end_square(self) -> Grid_square:
        """
        Returns the grid square that is the end square.
        """
        if(not self._end_square_coordinates):
            # ERROR
            return "There is no end square"
        
        return self._grid[self._end_square_coordinates]

    def set_end_square(self, coordinates: (int, int)) -> None:
        """
        Sets the inputted square to be the end square.
        If applicable, overwrittes the old inputted end square.
        If start, returns an error.
        """
        
        if(self._end_square_coordinates):
            self._grid[self._end_square_coordinates].set_is_end(False)

        self._end_square_coordinates = coordinates
        self._grid[self._end_square_coordinates].set_is_end(True)

    def get_current_blockers(self) -> dict:
        """
        Returns a dictionary of coordinate:blocker pairs
        """
        return self._current_blockers

    def set_blocker(self, coordinates: (int, int)) -> None:
        """
        Sets the inputted square to be a blocker.
        If also a start or end, returns an error instead.
        """

        self._grid[coordinates].set_is_blocker(True)

        self._current_blockers.append(coordinates)

    def reset(self) -> None:
        """
        Resets the start and end square to none.
        Also removes all blockers.
        """
        if(self._start_square_coordinates):
            self._grid[self._start_square_coordinates].set_is_start(False)
        self._start_square_coordinates = None

        if(self._end_square_coordinates):
            self._grid[self._end_square_coordinates].set_is_end(False)
        self._end_square_coordinates = None

        for item in self._current_blockers:
            self.get_grid_square(item).set_is_blocker(False)

        self._current_blockers = []

    def __repr__(self) -> None:
        """
        Returns all of the squares of the grid.
        """
        return f"{self._grid}"

class Session:
    """
    Represents the program session
    """

    def __init__(self, canvas: tk.Canvas, width: int, height: int) -> None:
        """
        Initialises the session with the given grid dimensions.
        """
        self._grid = Grid(width, height)
        self._canvas = canvas

        # defining standard units for square width and height
        global SQUARE_WIDTH
        global SQUARE_HEIGHT
        SQUARE_WIDTH = RESOLUTION_X/width
        SQUARE_HEIGHT = RESOLUTION_Y/height

        # game state number
        # 0 = selecting start
        # 1 = selecting end
        # 2 = selecting blockers
        # 3 = pathfinding
        # 4 = path not found
        # 5 = path successfully found
        global game_state
        game_state = 0

        # draw the grid
        self.draw_grid()

    def get_grid(self) -> None:
        """
        Returns the grid of the current session.
        """
        return self._grid

    def draw_grid(self) -> None:
        """
        Draws the game grid.
        """
        # print("drawing grid")  
        for square in self._grid._grid:
            self.draw_square(square)

    def draw_square(self, coordinates: (int, int)) -> None:
        """
        Draws a square at the given coordinates.
        """
        self._grid._current_rectangles[coordinates] = self._canvas.create_rectangle(coordinates[0] * SQUARE_WIDTH, coordinates[1] * SQUARE_HEIGHT, (coordinates[0] + 1) * SQUARE_WIDTH, (coordinates[1] + 1) * SQUARE_HEIGHT)

    def draw_text(self, coordinates: (int, int), message: str) -> None:
        """
        Draws a text label at the given coordinates with the given message.
        """
        self._canvas.create_text(coordinates[0] * SQUARE_WIDTH + 0.5 * SQUARE_WIDTH, coordinates[1] * SQUARE_HEIGHT + 0.5 * SQUARE_HEIGHT, text = message)

    def remove_square(self, coordinates: (int, int)) -> None:
        """
        Removes the square at the given coordinates.
        """
        if(not coordinates in self._grid._current_rectangles):
            # ERROR
            print("There exists no square at the given coordinates")
            return None

        self._canvas.delete(self._grid._current_rectangles[coordinates])
        self._grid._current_rectangles.pop(coordinates)

def main() -> None:
    """
    The main script to be run at program start.
    """
    global session

    # creates the initial GUI elements
    root = tk.Tk()
    root.title("Blind Pathfinding V1.0")
    root.geometry(f"{RESOLUTION_X}x{RESOLUTION_Y}")

    canvas = tk.Canvas(root, width = RESOLUTION_X, height = RESOLUTION_Y, bg = "maroon")

    # creates the grid
    session = Session(canvas, GRID_X, GRID_Y)

    # sets the mouse input function
    root.bind("<Button 1>", mouse_input)

    # sets the enter input function
    root.bind("<Return>", pathfinding)

    # prints the welcome message
    start_messages = ["", "Welcome to the Python Blind Pathfinder v1.",
                      "\n",
                      "This program gives the knowledge of the",
                      "start and end square coordinates to the",
                      "pathfinder, but not the coordinates of any",
                      "blockers. This can lead to some pretty",
                      "stupid behaviour sometimes, but give it",
                      "a try yourself.", "\n",
                      "To begin, use your mouse to first select",
                      "a square that will be the beginning and",
                      "then select a square that will be the end.",
                      "After this, you can place black squares that",
                      "will act as blockers. Finally, just press",
                      "ENTER on your keyboard to start the pathfinding.", "\n"]

    for message in start_messages:
        print(message)

    # packing the canvas and running the graphics
    canvas.pack()
    root.mainloop()

def mouse_input(event_mouse_pos):
    """
    Gets the mouse position in (x, y) coordinates in the window.
    Changes the grid squares to start, end or blockers if in that mode.
    """
    global mouse_x, mouse_y, game_state
    mouse_x = event_mouse_pos.x
    mouse_y = event_mouse_pos.y
    # print(mouse_x, mouse_y)
    #print(convert_pixel_to_square(mouse_x, mouse_y))
    coord_x = convert_pixel_to_square(mouse_x, mouse_y)[0]
    coord_y = convert_pixel_to_square(mouse_x, mouse_y)[1]

    if(game_state == 0):
        # if in the choosing start phase, set as start and
        # change the game phase
        session._canvas.itemconfig(session._grid._current_rectangles[(coord_x, coord_y)], fill = "green")
        session._grid.set_start_square((coord_x, coord_y))
        session.draw_text((coord_x, coord_y), "Start")
        game_state = 1

    elif(game_state == 1):
        # if in the choosing end phase, set as end and
        # change the game phase
        if((coord_x, coord_y) == session._grid._start_square_coordinates):
            # ERROR
            print("Can't select the start square to be the end square.")
            return None
        
        session._canvas.itemconfig(session._grid._current_rectangles[(coord_x, coord_y)], fill = "purple")
        session._grid.set_end_square((coord_x, coord_y))
        session.draw_text((coord_x, coord_y), "End")
        game_state = 2

    elif(game_state == 2):
        # if in the choosing blocker phase, set as blocker and
        # change the game phase
        if((coord_x, coord_y) == session._grid._start_square_coordinates):
            # ERROR
            print("Can't select the start square to be a blocker.")
            return None

        if((coord_x, coord_y) == session._grid._end_square_coordinates):
            # ERROR
            print("Can't select the end square to be a blocker.")
            return None

        if((coord_x, coord_y) in session._grid._current_blockers):
            # ERROR
            print("This square is already a blocker.")
            return None

        session._canvas.itemconfig(session._grid._current_rectangles[(coord_x, coord_y)], fill = "black")
        session._grid.set_blocker((coord_x, coord_y))

def pathfinding(event_enter):
    """
    Does the pathfinding logic and GUI updates when the enter key
    is pressed and the game is in the correct state.
    """
    global session, game_state

    # check if the game is already in pathfinding mode
    if(game_state == 3):
        # ERROR
        print("You are already pathfinding.")
        return None

    # check if a path has already been found and
    # the program is over
    if(game_state == 5):
        # ERROR
        print("A path was already found. Please restart the program to pathfind again.")
        return None

    # check if the game state is allowed to be in pathfinding mode
    # (gamestate 2)
    if(game_state != 2):
        # ERROR
        print("You cannot pathfind until setting a start and end square.")
        return None

    game_state = 3

    path = []
    possible_squares = []
    current_square = session._grid._start_square_coordinates
    session._grid.get_grid_square(current_square).set_is_picked(True)
    path.append(current_square)

    square_number = 1

    # the first element of the list should always be the start square

    while(current_square != session._grid._end_square_coordinates):
        # add the adjacent squares (including diagonals)
        # if they are not blockers
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                # if both offsets are 0, then it is the current square,
                # so break
                possible_square_coordinates = (current_square[0] + x_offset, current_square[1] + y_offset)
                
                if(x_offset == 0 and y_offset == 0):
                    # current square
                    print(f"{possible_square_coordinates} is the current square.")
                    pass
                elif(possible_square_coordinates[0] < 0 or possible_square_coordinates[0] >= GRID_X or possible_square_coordinates[1] < 0 or possible_square_coordinates[1] >= GRID_Y):
                    # out of bounds
                    print(f"{possible_square_coordinates} is out of bounds.")
                    pass
                elif(session._grid.get_grid_square(possible_square_coordinates).get_is_blocker()):
                    # is a blocker
                    print(f"{possible_square_coordinates} is a blocker.")
                    pass
                elif(session._grid.get_grid_square(possible_square_coordinates).get_is_picked()):
                    # if already picked, then ignore???????? THERE IS A MUCH BETTER WAY TO DO THIS PROBABLY
                    # LOOK INTO DEAD ENDS
                    print(f"{possible_square_coordinates} has already been tried.")
                    pass
                else:

                    # otherwise add to the possible squares list
                    #print("A")
                    possible_squares.append(possible_square_coordinates)

        # if no possible squares, then the pathfinder has failed
        if(len(possible_squares) == 0):
            # ERROR
            print("\nNo possible path.")
            print("Please restart the program to pathfind again.")

        print(f"Possible squares: {possible_squares}.")
        
        # with the possible squares, determine which to go to
        # in order of highest to lowest priority:
        # 1. end square
        # 2. square with the lowest vector hypotenuse length to the end square

        best_square = {}
        previous_best_square_coordinates = None
        best_square_coordinates = None
        for square_coordinates in possible_squares:
            # calculate vector_hypotenuse length
            # IS THERE A BETTER WAY THAN USING THE SQUARE ROOT FUNCTION?
            # THIS IS WHERE A LOT OF TIME OPTIMISATION CAN BE DONE





            vector_hypotenuse = math.sqrt(abs(square_coordinates[0] - session._grid._end_square_coordinates[0])**2 + abs(square_coordinates[1] - session._grid._end_square_coordinates[1])**2)




            
            # if first iteration, just add the first square
            if(len(best_square) == 0):
                best_square[square_coordinates] = vector_hypotenuse
                best_square_coordinates = square_coordinates
                previous_square = square_coordinates
            # if the vector hypotenuse of the new is shorter,
            # it is the new best square
            elif(best_square[previous_square] > vector_hypotenuse):
                best_square.clear()
                best_square[square_coordinates] = vector_hypotenuse
                best_square_coordinates = square_coordinates
                previous_square = square_coordinates

        # clear old possible square list
        possible_squares.clear()

        # to prevent crashes
        if(previous_best_square_coordinates == best_square_coordinates):
            break
        
        previous_best_square_coordinates = best_square_coordinates
        
        print(f"Best square: {best_square}.")

        # move to the new current_square and add it to the path
        current_square = best_square_coordinates
        path.append(current_square)
        session._grid.get_grid_square(current_square).set_is_picked(True)
        print(f"Current square: {current_square}.")

        # if we are at the end square, then we are
        # finished and we do not colour the end
        # square yellow
        if(current_square == session._grid._end_square_coordinates):
            # pathfinding is finished
            print("\nA path was successfully found!")
            print("Please restart the program to pathfind again.")
            game_state = 5

            # colour the path yellow except for the
            # first and last element
            # also add the number
            for square in path:
                if(path[0] == square or path[len(path)-1] == square):
                    pass
                else:
                    session._canvas.itemconfig(session._grid._current_rectangles[(square[0], square[1])], fill = "yellow")
                    session.draw_text((square[0], square[1]), square_number)
                    square_number += 1
            
            return None
        
        

def convert_pixel_to_square(x: int, y: int) -> (int, int):
    """
    Converts the mouse pixel coordinates to grid coordinates.
    """
    return (int((x / SQUARE_WIDTH) // 1), int((y / SQUARE_HEIGHT) // 1))

if __name__ == "__main__":
    """
    Automatically runs the main script at program start.
    """
    main()


















