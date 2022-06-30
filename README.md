# AsteroidShooter

An old Pygame project (my first Python one) that was originally supposed to be a more gamey version of an asteroid mining text adventure I made in Java.

You play as a little white arrow and asteroids come at you. If they hit you, you lose points. Shoot them to gain points. The asteroids get faster and spawn quicker as the game continues. 

Controls:
WASD to move, mouse to aim, left click to shoot.

The only notable things in this project really are:<br>
  Everything moves around the player<br>
  Collision detection is based on distance, O(n^2) (nested for loop) for asteroids and bullets.<br>
  Movement is based on where the mouse is pointing; if it's pointing to the top right and you press A, you move towards the top left<br>
![asteroidshooter](https://user-images.githubusercontent.com/84115711/176573902-79834c52-af70-4434-8ef8-66dfd42b0246.gif)
