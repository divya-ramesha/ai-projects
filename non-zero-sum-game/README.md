# Description

Los Angeles Homeless Services Authority (LAHSA) and Safe Parking LA (SPLA) are two  organizations  in  Los  Angeles  that  service  the  homeless  community.  LAHSA provides beds in shelters and SPLA manages spaces in parking lots for people living in their cars. In the city’s new app for homelessness, people in need of housing can apply for a space with either service.  For this homework, you will help SPLA choose applicants  that  meet  the  SPLA  specific  requirements  for  the  space  and  that  also optimize the use of the parking lot for that week. 
Applicant information entered into the homelessness app:
Applicant ID: 5 digits
Gender: M/F/O
Age: 0-100
Pets: Y/N
Medical conditions: Y/N
Car: Y/N
Driver’s License: Y/N
Days of the week needed: 0/1 for each day of the 7 days of the week (Monday-Sunday) 

Example applicant record: 00001F020NNYY1001000 for applicant id 00001, female, 20 years old, no pets, no medical conditions, with car and driver’s license, who needs housing for Monday and Thursday.

SPLA requirements differ from LAHSA. They are both picking from the same applicant list. They each have different resources and may not be qualified to accept the same applicants. SPLA and LAHSA alternate choosing applicants one by one.  They must choose an  applicant  if there is still a  qualified  oneon the list(no  passing). SPLA applicants must have a car and driver’s license, but no medical conditions.  LAHSA shelter can only serve women over 17 years old without pets. Both SPLA and LAHSA have limited resources that must be used efficiently.  Efficiency is calculated by how many of the spaces are used during the week.  For example, a SPLA parking lot has 10 spacesand can have at most 10*7 days = 70 different applicants for the week. SPLA tries to maximize its efficiency rate.

Input.txt
10
10
1
00005
1
00002
5
00001F020NNYY1001000
00002F020NNYY1000111
00003M040NNYY1000110
00004M033NNYY1000000
00005F020NNYY1000110

Output.txt
00001

Explanation
SPLA chose 00002 first, and then LAHSA chose00005 next.00001 should be chosen because it allows SPLA to choose applicants 00001, 00003, and 00004, while LAHSA doesn’t need to choose anybody else. This is because 00001 qualifies for both, but 00003 and 00004 only qualify for SPLA. So, choosing 00001 next means that SPLA chooses all three remaining applicants, and LAHSA gets zero

# To Do

1. This is a non-zero sum game
2. Both the parties are trying to maximise their profits and its independent of each other.
3. As a result of which no alpha-beta pruning is possible
