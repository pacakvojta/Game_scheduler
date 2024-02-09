# Game Scheduler

## Simple interactive python Flask App that prepares doubles pairings.
Run script to make sure that you are teammed up with different player every round and you dont face same opponent over and over again.

**How to run the script**:
Run \_\_init\_\_.py
 script to open interactive app in browser. Simply put in up to 14 players' names (leave blank those not needed) and input number of rounds (8-10 recommended). After submitting, pairings will be automatically calculated and game schedule for each round should be printed in matter of seconds (not longer than 1 minute). 
Bellow schedule, there is printed matrix of teammates and opponents to see how many times are all couples paired up and how many times you face each olayer.  

**Advantages over random pairings:**
- Always play with new teammate before playing with aynone for second time (if possible)
- There is limit on how many times you play against specific player (not optimized however)

**Conditions conditions:**
- Number of players must be at least 4 and not more than 14
- Number of rounds cant exceed 10

**Limitations and potential improvements:**
- Bruteforce technique (non-optimal way of finding pairings)
- If there are singles 1v1 games (i.e. we have 6,10,14 players), app not optimized to avoid repetitions
- If there are people resting (i.e. we have 5,9,13 players), app not optimized to switch person resting
- Extension for n-players and m-rounds
- Interactive results saving and brackets/evaluations

