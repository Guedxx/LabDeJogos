<h1 align="center">King Pong</h1>
<p align="center">
  <img src=https://github.com/Guedxx/LabDeJogos/blob/master/Sprites/INIT_madeBy.png />
</p>
<p align="center"><i>Climb the tower and become the King of Pong!</i></p>

## Table of Contents

- <a href="#about-the-project">About the Project</a>
- <a href="#features">Features</a>
- <a href="#getting-started">Getting Started</a>
  - <a href="#prerequisites">Prerequisites</a>
  - <a href="#installation">Installation</a>
  - <a href="#running-the-game">Running the Game</a>
- <a href="#gameplay">Gameplay</a>
- <a href="#code-overview">Code Overview</a>

<a name="about-the-project"></a>
## About the Project

<p>King Pong is a reimagined version of the classic Pong game, where players must climb a tower of increasing difficulty to claim the title of King. The game was developed as a collaborative project using Python, Pygame, and PPlay. Despite being created with minimal object-oriented programming, King Pong offers a fun and challenging gameplay experience.</p>

<a name="features"></a>
## Features

<ul>
  <li><b>Classic Pong Mechanics:</b> Retains the core elements of the original Pong game.</li>
  <li><b>Tower Climb Mode:</b> Progress through levels of increasing difficulty as you ascend the tower.</li>
  <li><b>Simple Yet Engaging:</b> Easy to pick up and play, with a challenging progression system.</li>
  <li><b>Power Ups:</b> To spice things up!.</li>
</ul>

<a name="getting-started"></a>
## Getting Started

<a name="prerequisites"></a>
### Prerequisites

<p>Make sure you have Python installed on your system. You'll also need the following Python libraries:</p>

<ul>
  <li><a href="https://www.pygame.org/">Pygame</a></li>
</ul>

<a name="installation"></a>
### Installation

<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/Guedxx/LabDeJogos.git
cd LabDeJogos
</code></pre>
  </li>
  <li>Install the required libraries:
    <pre><code>pip install pygame
</code></pre>
  </li>
</ol>

<a name="running-the-game"></a>
### Running the Game

<p>Run the game by executing the following command:</p>

<pre><code>python main.py
</code></pre>

<p>Enjoy the climb to become the King of Pong!</p>

<a name="gameplay"></a>
## Gameplay

<p>In King Pong, players face off against AI as they climb a tower of increasingly difficult levels. The goal is to outplay your opponent by bouncing the ball past them, taking away 3 health points makes you advance to the next stage. The higher you climb, the tougher the challenges become.</p>

<li><code>W</code>: Moves UP.</li>
<li><code>S</code>: Moves DOWN.</li>
<li><code>Space</code>: Dashes.</li>
<li><code>Momentum</code>: The more you move the faster you become. Dashing can help you gain momentum.</li>


<a name="code-overview"></a>
## Code Overview

<p>King Pong was developed with minimal object-oriented programming, as the project was created before the participants had formal education in OOP. The code may be a bit rough around the edges, but it is functional and effective.</p>

<p><b>Key Files:</b></p>
<ul>
  <li><code>main.py</code>: Contains the core gameplay mechanics.</li>
  <li><code>setup.py</code>: It's the sprite controler and holds the menu.</li>
  <li><code>animations.py</code>: Contains all the animations of the game, they were all made in pure code!</li>
  <li><code>enemysIA.py</code>: Contains all the enemys behaviour, their momentum logic and power up use.</li>
  <li><code>gamefunctions.py</code>: Contains the pause menu code.</li>
  <li><code>ingame.py</code>: Calls all the sprites in a list and Draws/Updates them.</li>
  <li><code>powerUps.py</code>: Changes the sprite of the power UP sprite in the lvl.</li>
</ul>

<p>Despite its simple structure, the codebase is a good example of early-stage game development, and we are proud of what we’ve accomplished.</p>


