=========================================
 Cheat for https://semantle.novalis.org/
=========================================

The cheat is very simple: We submit the three words *man, red, two* to the game
and then `triangulate´ the solution.

This works because all words are positioned in a linear vector space.  The way
this works is very similar to the way a GPS receiver calculates your position
from your distance to three satellites.

.. note::

   Everybody that knows how to use a web debugger will find an even simpler
   cheat because at the start of the game the browser will download a list of
   *all* past and future solution words.


Install
=======

Clone the repository, then:

.. code:: bash

   cd semantle-cheat
   wget https://gitlab.com/dholth/semantleless/-/blob/master/public/word2vec.db
   pip3 install -r requirements.txt
   ./init-cheat.py


Cheat
=====

Enter the three words: man, red, two into the game.

.. code:: bash

   ./cheat.py <sim_man> <sim_red> <sim_two>
