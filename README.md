# MIGRATING FROM GITHUB TO GITLAB AT https://gitlab.com/SamWibatt/aicribbage - please go to that repository (unless you're already there.)

# AICribbage
Learned models for cribbage playing: discard, next card in count.

No learned players have yet been constructed - computer player is random / first legal pick.

# Status

As of (7/27/20), early. Python prototype (pybbage) that is the framework for learned players is complete and its correctness wrt American Cribbage Congress rules verified through unit testing. It has a text interface for playing it. 

**C++ development has been split off into [cribbage_cpp](https://github.com/SamWibatt/cribbage_cpp), where pybbage's functionality has been duplicated and verified through unit testing**.

# objective

* More self-teaching, this is like a "semester project" for showing I can use modern AI methods.
* Construct models for two player game, see if can transfer to others
* First concept is if I have models to:
    * decide which cards to discard from hand that's dealt
        * both as dealer and non-dealer
    * decide which card to play next in count
* will sketch design in wiki
