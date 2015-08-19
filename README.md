# Manhattan College Scheduler

Purpose: take the hassle out of scheduling classes

Scheduling period at college is always exciting. The freedom to choose what classes you want to take and when you want to take them is very liberating. However, it comes with some drawbacks. Every time you think you have the perfect schedule, your last class conflicts with the rest. After seeing my peers spend hours sketching schedule possibilities on several pages of notebook paper, I decided to take action.

When you input the classes you want to take next semester, the program will automatically find every combination of class sections that do not cause a time conflict. You can even set filters like earliest class start time and latest class end time, or you can manually lock a section to get that professor you really want.

The schedule options are displayed to you visually, so you can save the one you want, print it, and show all your friends what classes you are taking right on the spot.

(not compatible with Python 3)

Usage:

1. Run app.py
2. Navigate to 127.0.0.1:5000
3. Enter required classes; each on its own line
  * Format
    * Any section: MATH 185
    * Only these sections: MATH 185 +01,02
    * All but these sections: MATH 185 -01,02
4. Enter start and end time limits for classes (optional)
5. Click submit
