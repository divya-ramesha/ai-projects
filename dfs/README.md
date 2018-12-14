# Description

We are helping tTransportation Dept to develop a pilot scooter program for LA. There are a limited number of police officers available to monitor and address issues that may arise from scooters, ranging from traffic and safety violations to accidents with cars, bikes, other scooters and pedestrians. The scooter companies have given us access to scooter routes over the course of one day. In order to maximize the scooter activity monitored by the officers, you will take as input the route information,the monitored city area dimensions, and the number of officers available to then generate the best placement of the officers. The officers can only be in one place for one day, and there can only be one officer on each street. When an officer and scooter are at the same location at the same time, the officer is able to address a safety issue, and one “Activity point” is gained. The  goal  is  to  place  the  officers  in  locations  that  do  not conflict with each other, while maximizing the total “Activity points” for the day(12 time steps in a day).  

The problem follows these rules:

Officers cannot be in same square, same row, same column, or along the same diagonal. (Think of queens on a chess board)
Officers cannot move.
Activity points are collected at each time step t when officers are in same square as scooters. One point per each scooter. 
The grid coordinate system will be indexed starting from the top-left corner.

# To Do

1. This is similar to placing m queens on a n*n chess board such that no two queens are in same square, same row, same column, or along the same diagonal.
2. If multiple solutions are possible then we have to pick that solution which gives us maximum activity points
3. This can be implemented using dfs + backtracking