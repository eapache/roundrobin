#!/usr/bin/python
#
# Round-Robin Game Scheduling Script
# Copyright 2012, Evan Huus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import sys

def rotate(list):
    'Rotates all but the first element of a list, which is fixed'
    
    temp = list[-1]
    for i in range(1,len(list)):
        list[i], temp = temp, list[i]

parser = argparse.ArgumentParser(description='A simple round-robin schedule generator')

parser.add_argument('teams', metavar='TEAMS', type=int,
        help='the number of teams that are playing')
parser.add_argument('games', metavar='GAMES', type=int,
        help='the number of games to schedule')

args = parser.parse_args()

if args.teams < 2:
    print >> sys.stderr, "You can't have fewer than two teams!"
    sys.exit(1)

if args.games < 0:
    print >> sys.stderr, "You must have at least one game!"
    sys.exit(1)

# We may need to increment team_count to deal with byes, but we
# still need the original for outputting byes as X instead of team#.
team_count = args.teams

# magic team which counts as a bye
if args.teams % 2: team_count += 1

# The maximum length of the schedule where no teams play
# each other twice
unique_schedule = team_count - 1

if args.games < unique_schedule:
    print >> sys.stderr, "Warning: you have not specified enough games for every"
    print >> sys.stderr, "team to possibly play every other team."

base_schedule = [[None for i in range(team_count)] for j in range(unique_schedule)]

team_list = [i for i in range(team_count)]

# Fill the schedule
for game in range(unique_schedule):
    for i in range(team_count):
        base_schedule[game][team_list[i]] = team_list[-i-1]
    rotate(team_list)

# Use 1-indexed values for output
for game in range(unique_schedule):
    for team in range(team_count):
        base_schedule[game][team] += 1
        # Convert byes to 'X'
        if base_schedule[game][team] > args.teams:
            base_schedule[game][team] = 'X'

# Build the final, displayable schedule
final_schedule = [['']]
final_schedule[0].extend("Team {}".format(team) for team in range(1, args.teams+1))
for game in range(args.games):
    final_schedule.append(['Game {}'.format(game+1)])
    final_schedule[-1].extend(base_schedule[game % unique_schedule][0:args.teams])

output = csv.writer(sys.stdout)
output.writerows(final_schedule)
