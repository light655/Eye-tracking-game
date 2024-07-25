# Eye tracking game

This is a very boring "game" in which a ball moves on the screen. 
The player's eyes are tracked with the webcam using the [GazeTracking](https://github.com/antoinelame/GazeTracking) library. 

## Data recording

The position of the ball and the gazing direction of the player's eyes are plotted on a plot. 
The plot is shown after the "game" finishes, which lasts about 5 seconds.
The position data are standardised before plotting so that the two lines will overlay.

The position of the ball will be shown as blue and the gazing direction of the eyes will be shown as orange. 
Both horizontal and vertical directions are plotted in their respective plots.
If GazeTracking is unable to tracker the player's eyes, the orange line will not show.

## Usage

To run the "game", first clone the repository and initialise GazeTracking.
```
git clone https://github.com/light655/Eye-tracking-game.git
cd Eye-tracking-game
git submodule update --init
```
Then install the dependencies.
```
pip3 install -r dependencies.txt
```
Finally, run the game.
```
python3 game.py