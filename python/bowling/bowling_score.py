#!/usr/bin/python
#
# Python script that calculates and returns the total score of a game of
# bowling.
#
# Rules:
# To briefly summarize the scoring for this form of bowling:
#  - One game of bowling is made up of ten frames.
#  - In each frame, the bowler has two throws to knock down all the pins.
#  - Possible results for a frame:
#  -- Strike ('X'): the bowler knocks down all 10 pins on the first throw. The
#     frame is over early. The score for the frame is 10 plus the total pins
#     knocked down on the next two throws.
#  -- Spare ('/'): the bowler knocks down all 10 pins using two throws. The
#     score for the frame is 10 plus the number of pins knocked down on the
#     next throw.
#  -- Open frame: the bowler knocks down less than 10 pins with his two throws.
#     The score for the frame is the total number of pins knocked down.
#  - The game score is the total of all frame scores.
#  - Special rules for the 10th frame:
#  -- A strike in the tenth frame gives the bowler two bonus throws, to fill
#     out the scoring formula for the last frame.
#  -- A spare in the tenth frame gives the bowler one bonus throw, to fill out
#     the scoring formula for the last frame.
#  -- These throws count as part of the 10th frame.
#  -- The process does not repeat - for example, knocking down all 10 pins on a
#     bonus throw does not provide any additional bonus throws.
#
# Following cases are outside the scope of the current exercise:
# - Check for valid throws (like scores that add to 11)
# - Check for the correct number of throws and frames
# - Provide any intermediate scores - it only has to provide the final score


import sys


def total_score(input):
    """
    Parses a user input string and calculates the total score of the submitted
    bowling game.

    @type input: str
    @param input: String representing the throws of a single bowling game (split
                  into frames). Eg. '12-34-5/-0/-X-X-X-X-X-X-XX'
    @rtype: int
    @return: Total calculated score.
    """
    throws = parse_input(input)
    return score(throws)


def parse_input(input):
    """
    Utility method that transforms an input string (in a predefined format)
    into a list of elements that represent each throw taken in a single game.

    Example:
    An input of '01-5/-0/-23-X-X-X-X-X-X-XX' will return the following list:
    [0, 1, 5, 5, 0, 10, 2, 3, 10, 10, 10, 10, 10, 10, 10, 10]

    @type input: str
    @param input: String of bowling scores split into frames and separated by
                  hyphens. Strikes are represented as 'X', spares are
                  represented as '/' and misses are represented as '0'.
    @rtype: list
    @return: List of integers where each element represents a single
             throw (in the order taken).
    """
    if not input:
        return []
    throws = []
    # iterate over each frame in the list, substitute special characters for
    # numeric values and populate the 'throws' list
    for frame in input.split('-'):
        # replace all strikes with a value of 10
        if frame[0] == 'X':
            throws.append(10)
            # special case for bonus frame
            if len(frame) == 2:
                if frame[1] == 'X':
                    throws.append(10)
                else:
                    throws.append(int(frame[1]))
        elif frame.endswith('/'):
            # value of '/' is 10 minus the previous index, eg 5/ = 10 - 5 = 5
            throws.extend([int(frame[0]), 10 - int(frame[0])])
        else:
            # if no special characters exist in the frame, cast values to
            # integers and append to the list
            throws.extend(map(int, frame))
    return throws


def score(throws, frame=1, total=0):
    """
    Recursive method that calculates the score of the bowling game one frame
    at a time and returns the total.

    @type throws: list
    @param throws: List of elements (throws) to be totaled.
    @type frame: int
    @param frame: Index of the frame being calculated. Default value: 1
    @type total: int
    @param total: Running total of the bowling game score. Default value: 0
    @rtype: int
    @returns: Final calculated total of the bowling game.
    """
    # exit case (frame 10 calculated or incomplete game)
    if frame > 10 or not throws:
        return total
    # strike
    elif throws[0] == 10:
        # bonus = next two throws following current frame
        bonus = 0
        # edge case logic for incomplete game
        if len(throws) >= 3:
            bonus = sum(throws[1:3])
        elif len(throws) > 1:
            bonus = throws[1]
        # pop off first index, increment frame count, update total
        return score(throws[1:], frame + 1, total + 10 + bonus)
    # spare
    elif sum(throws[0:2]) == 10:
        # bonus = next throw following current frame
        bonus = 0
        # edge case logic for incomplete game
        if len(throws) >= 3:
            bonus = throws[2]
        # pop off first two indexes, increment frame count, update total
        return score(throws[2:], frame + 1, total + 10 + bonus)
    # closed frame
    else:
        total += sum(throws[0:2])
        # pop off first two indexes, increment frame count, update total
        return score(throws[2:], frame + 1, total)


def run_tests():
    tests = [(300, 'X-X-X-X-X-X-X-X-X-X-XX'),  # perfect game
             (90, '45-54-36-27-09-63-81-18-90-72'),  # all closed frames
             (150, '5/-5/-5/-5/-5/-5/-5/-5/-5/-5/-5'),  # all spares
             # closed frames / bonus throw
             (96, '45-54-36-27-09-63-81-18-90-7/-5'),
             # 'sprike' (0 -> spare) / bonus spare
             (108, '12-34-0/-0/-X-X-00-18-72-X-0/'),
             # all spares / bonus strike
             (155, '0/-19-28-37-46-55-64-73-82-91-X'),
             # all gutter balls, request bumpers
             (0, '00-00-00-00-00-00-00-00-00-00'),
             # empty input
             (0, ''),
             # incomplete game with closed frames
             (15, '01-23-45'),
             # incomplete game with trailing strike
             (25, '01-23-45-X'),
             # incomplete game with strike in 10th frame and no bonus frame
             (270, 'X-X-X-X-X-X-X-X-X-X'),
             # incomplete game with single strike in bonus frame
             (290, 'X-X-X-X-X-X-X-X-X-X-X'),
             # incomplete game with spare
             (25, '01-23-45-6/'),
             # incomplete game with spare in 10th frame and no bonus frame
             (145, '5/-5/-5/-5/-5/-5/-5/-5/-5/-5/'),
             # extended frames (not calculated)
             (300, 'X-X-X-X-X-X-X-X-X-X-XX-X-X-X-X-X-X')]
    for score, input in tests:
        result = "Testing: %s = %d: %s"
        try:
            assert score == total_score(input), 'FAIL'
            print result % (input, score, 'PASS')
        except AssertionError, e:
            print result % (input, score, e)

if __name__ == "__main__":
    """
    Script entry point. Accepts a list of string inputs separated by spaces
    or runs a set of predefined unit tests if no arguments are provided.
    """
    if len(sys.argv) > 1:
        for input in sys.argv[1:]:
            print "Input: %s Total: %d" % (input, total_score(input))
    else:
        run_tests()
