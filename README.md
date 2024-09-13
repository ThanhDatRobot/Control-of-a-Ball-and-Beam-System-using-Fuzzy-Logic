# Control-of-a-Ball-and-Beam-System-using-Fuzzy-Logic
# Example: Fan Speed Control Based on Temperature and Humidity
Step 1: Define Input and Output Variables
Input 1 (Temperature):

Fuzzy sets:
Low
Medium
High
Input 2 (Humidity):

Fuzzy sets:
Low
Medium
High
Output (Fan Speed):

Constant values for each fuzzy set of fan speed:
Slow: 30% fan speed
Medium: 60% fan speed
Fast: 90% fan speed
Step 2: Define Control Rules
The control rules will combine temperature and humidity to determine the fan speed. Here are the basic rules:

If temperature is low and humidity is low, then fan speed is slow (30%).

Rule 1: IF Temperature is Low AND Humidity is Low THEN Fan Speed = 30
If temperature is medium and humidity is low, then fan speed is medium (60%).

Rule 2: IF Temperature is Medium AND Humidity is Low THEN Fan Speed = 60
If temperature is high and humidity is low, then fan speed is fast (90%).

Rule 3: IF Temperature is High AND Humidity is Low THEN Fan Speed = 90
If temperature is low and humidity is medium, then fan speed is slow (30%).

Rule 4: IF Temperature is Low AND Humidity is Medium THEN Fan Speed = 30
If temperature is medium and humidity is medium, then fan speed is medium (60%).

Rule 5: IF Temperature is Medium AND Humidity is Medium THEN Fan Speed = 60
If temperature is high and humidity is medium, then fan speed is fast (90%).

Rule 6: IF Temperature is High AND Humidity is Medium THEN Fan Speed = 90
If temperature is low and humidity is high, then fan speed is slow (30%).

Rule 7: IF Temperature is Low AND Humidity is High THEN Fan Speed = 30
If temperature is medium and humidity is high, then fan speed is medium (60%).

Rule 8: IF Temperature is Medium AND Humidity is High THEN Fan Speed = 60
If temperature is high and humidity is high, then fan speed is fast (90%).

Rule 9: IF Temperature is High AND Humidity is High THEN Fan Speed = 90
Step 3: Define Membership Functions
We define membership functions for temperature and humidity as follows:

Temperature:

Low: μ_low(T) = max(0, min(1, (25 - T)/10))
Medium: μ_medium(T) = max(0, min((T - 20)/5, (30 - T)/5))
High: μ_high(T) = max(0, min((T - 25)/5, 1))
Humidity:

Low: μ_low(H) = max(0, min(1, (40 - H)/20))
Medium: μ_medium(H) = max(0, min((H - 30)/10, (70 - H)/20))
High: μ_high(H) = max(0, min((H - 50)/20, 1))
Step 4: Calculate Membership Values for a Given Input
Let’s assume the actual temperature is 28°C and the humidity is 60%. We calculate the membership values for both inputs:

Temperature:

μ_low(28) = 0
μ_medium(28) = 0.4
μ_high(28) = 0.6
Humidity:

μ_low(60) = 0
μ_medium(60) = 0.5
μ_high(60) = 0.5
Step 5: Inference Using Max-Prod Method
Here are the rules that are triggered and their corresponding firing strengths:

Rule 5: IF Temperature is Medium AND Humidity is Medium THEN Fan Speed = 60

Firing strength = μ_medium(28) * μ_medium(60) = 0.4 * 0.5 = 0.2
Output value = 60
Activated output = 0.2 * 60 = 12
Rule 6: IF Temperature is High AND Humidity is Medium THEN Fan Speed = 90

Firing strength = μ_high(28) * μ_medium(60) = 0.6 * 0.5 = 0.3
Output value = 90
Activated output = 0.3 * 90 = 27
Rule 9: IF Temperature is High AND Humidity is High THEN Fan Speed = 90

Firing strength = μ_high(28) * μ_high(60) = 0.6 * 0.5 = 0.3
Output value = 90
Activated output = 0.3 * 90 = 27

Step 6: Defuzzification (Weighted Average)
Using the weighted average method, we calculate the final fan speed:

Fan Speed = (12 + 27 + 27)/(0.2 + 0.3 + 0.3) = 66/0.8 = 82.5

The final fan speed after inference is 82.5%.
