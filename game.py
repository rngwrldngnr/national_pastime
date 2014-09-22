import random
from outcome import Strike, Ball, FoulBall, ForceOut, Single, Double, Triple, Run

COUNTS = {(0, 0): 00, (1, 0): 10, (2, 0): 20, (3, 0): 30,
          (0, 1): 10, (1, 1): 11, (2, 1): 21, (3, 1): 31,
          (0, 2): 02, (1, 2): 12, (2, 2): 22, (3, 2): 32}


class Game(object):

    def __init__(self, ballpark, home_team, away_team, league, rules):
        self.ballpark = ballpark
        self.league = league
        self.home_team = home_team
        self.away_team = away_team
        self.rules = rules  # Rules game will be played under
        # Prepare for game
        home_team.pitcher = home_team.pitcher
        away_team.pitcher = away_team.pitcher
        home_team.batting_order = home_team.players
        away_team.batting_order = away_team.players
        home_team.batter = home_team.batting_order[-1]  # To get decent batter up during testing
        away_team.batter = away_team.batting_order[-1]
        self.home_team.runs = self.away_team.runs = 0
        self.innings = []
        self.umpire = next(z for z in self.league.country.players if
                           z.hometown.name in ("Minneapolis", "St. Paul", "Duluth"))

    def enact(self):
        for inning_n in xrange(1, 10):
            Inning(game=self, number=inning_n)
        inning_n = 9
        while self.home_team.runs == self.away_team.runs:
            inning_n += 1
            Inning(game=self, number=inning_n)
        if self.home_team.runs > self.away_team.runs:
            self.winner = self.home_team
            self.loser = self.away_team
        else:
            self.winner = self.away_team
            self.loser = self.home_team
        print "{} has beaten {} {}-{}".format(
            self.winner.city.name, self.loser.city.name, self.away_team.runs, self.home_team.runs
        )
        self.print_box_score()
        self.home_team.runs = self.away_team.runs = 0
        self.winner.wins += 1
        self.loser.losses += 1

    def print_box_score(self):
        print '\n\n'
        print '\t\t' + '   '.join(str(i+1) for i in xrange(len(self.innings)))
        print '\t\t__________________________________'
        if len(self.away_team.city.name) >= 8:
            tabs_needed = '\t'
        else:
            tabs_needed = '\t\t'
        print (self.away_team.city.name + tabs_needed +
               '   '.join(str(inning.top.runs) for inning in self.innings) +
               '\t' + str(self.away_team.runs))
        print ''
        if len(self.home_team.city.name) >= 8:
            tabs_needed = '\t'
        else:
            tabs_needed = '\t\t'
        if self.innings[-1].bottom:
            print (self.home_team.city.name + tabs_needed +
                   '   '.join(str(inning.bottom.runs) for inning in self.innings) +
                   '\t' + str(self.home_team.runs))
        else:  # Home team didn't need to bat in bottom of the ninth inning
            print (self.home_team.city.name + tabs_needed +
                   '   '.join(str(inning.bottom.runs) for inning in self.innings[:-1]) +
                   '   -\t' + str(self.home_team.runs))
        print '\n\n\t {}\n'.format(self.away_team.name)
        print '\t\t\tAB\tR\tH\t2B\t3B\tHR\tRBI\tBB\tSO\tSB\tAVG'
        for p in self.away_team.players:
            if len(p.at_bats) > 0:
                batting_avg = round(len(p.hits)/float(len(p.at_bats)), 3)
                if batting_avg == 1.0:
                    batting_avg = '1.000'
                else:
                    batting_avg = str(batting_avg)[1:]
            else:
                batting_avg = '.000'
            while len(batting_avg) < 4:
                batting_avg += '0'
            if len(p.last_name) >= 8:
                tabs_needed = '\t'
            else:
                tabs_needed = '\t\t'
            print "{}{}{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                p.last_name, tabs_needed, p.position, len(p.at_bats), len(p.runs), len(p.hits),
                len(p.doubles), len(p.triples), len(p.home_runs), len(p.rbi),
                len(p.batting_walks), len(p.batting_strikeouts), len(p.stolen_bases), batting_avg
            )
        print '\n\n\t {}\n'.format(self.home_team.name)
        print '\t\t\tAB\tR\tH\t2B\t3B\tHR\tRBI\tBB\tSO\tSB\tAVG'
        for p in self.home_team.players:
            if len(p.at_bats) > 0:
                batting_avg = round(len(p.hits)/float(len(p.at_bats)), 3)
                if batting_avg == 1.0:
                    batting_avg = '1.000'
                else:
                    batting_avg = str(batting_avg)[1:]
            else:
                batting_avg = '.000'
            while len(batting_avg) < 4:
                batting_avg += '0'
            if len(p.last_name) >= 8:
                tabs_needed = '\t'
            else:
                tabs_needed = '\t\t'
            print "{}{}{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                p.last_name, tabs_needed, p.position, len(p.at_bats), len(p.runs), len(p.hits),
                len(p.doubles), len(p.triples), len(p.home_runs), len(p.rbi),
                len(p.batting_walks), len(p.batting_strikeouts), len(p.stolen_bases), batting_avg
            )


class Inning(object):

    def __init__(self, game, number):
        self.game = game
        self.game.innings.append(self)
        self.number = number
        self.frames = []
        # Modified by self.enact()
        self.top = None
        self.bottom = None

        self.enact()

    def enact(self):
        self.top = Frame(inning=self, top=True)
        if not (self.number >= 9 and
                self.game.home_team.runs > self.game.away_team.runs):
            self.bottom = Frame(inning=self, bottom=True)


class Frame(object):

    def __init__(self, inning, top=False, middle=False, bottom=False):
        self.inning = inning
        inning.frames.append(self)
        self.game = inning.game
        if top:
            self.half = "Top"
            self.batting_team = self.game.away_team
            self.pitching_team = self.game.home_team
        elif middle:
            self.half = "Middle"
        elif bottom:
            self.half = "Bottom"
            self.batting_team = self.game.home_team
            self.pitching_team = self.game.away_team
        # Players currently on base
        self.on_first = None
        self.on_second = None
        self.on_third = None
        # Other miscellany
        self.runs = 0  # Runs batting team has scored this inning
        self.outs = 0
        self.at_bats = []  # Appended to by AtBat.__init__()
        self.at_bat = None

        print "\n\t\t*****  {}  *****".format(self)
        self.enact()

    def enact(self):
        while self.outs < 3:
            self.at_bat = AtBat(frame=self)
            self.at_bat.enact()
            print "\n{}. {} outs. Score is {}-{}.\n".format(
                self.at_bat.result, self.outs, self.game.away_team.runs, self.game.home_team.runs
            )

    def __str__(self):
        ordinals = {
            1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
            6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth',
            11: 'eleventh', 12: 'twelfth', 13: 'thirteenth', 14: 'fourteenth',
            15: 'fifteenth', 16: 'sixteenth', 17: 'seventeenth', 18: 'eighteenth',
            19: 'nineteenth', 20: 'twentieth', 21: 'twenty-first', 22: 'twenty-second',
            23: 'twenty-third', 24: 'twenty-fourth', 25: 'twenty-fifth',
            26: 'twenty-sixth', 27: 'twenty-seventh', 28: 'twenty-eighth',
            29: 'twenty-ninth', 30: 'thirtieth', 31: 'thirty-first'
        }
        if self.inning.number in ordinals:
            if self.half == "Top":
                return "{} of the {} inning -- {} up to bat".format(
                    self.half, ordinals[self.inning.number], self.game.away_team
                )
            else:
                return "{} of the {} inning -- {} up to bat".format(
                    self.half, ordinals[self.inning.number], self.game.home_team
                )
        else:
            if self.half == "Top":
                return "{} of inning {} -- {} up to bat".format(
                    self.half, self.inning.number, self.game.away_team
                )
            else:
                return "{} of inning {} -- {} up to bat".format(
                    self.half, self.inning.number, self.game.home_team
                )

    def get_next_batter(self):
        try:
            batter_index = (
                self.batting_team.batting_order.index(self.batting_team.batter)
            )
            next_batter = self.batting_team.batting_order[batter_index+1]
        except IndexError:  # Reached end of the order, go back to top
            next_batter = self.batting_team.batting_order[0]
        return next_batter

    @property
    def baserunners(self):
        baserunners = []
        # Note: they must be appended in this order so that baserunners
        # can check if preceding runners are advancing before they
        # attempt to advance themselves
        if self.on_third:
            baserunners.append(self.on_third)
        if self.on_second:
            baserunners.append(self.on_second)
        if self.on_first:
            baserunners.append(self.on_first)
        return baserunners


class AtBat(object):

    def __init__(self, frame):
        self.frame = frame
        self.frame.at_bats.append(self)
        self.game = frame.game
        self.batter = frame.get_next_batter()
        frame.batting_team.batter = self.batter
        self.pitcher = frame.pitching_team.pitcher
        self.catcher = frame.pitching_team.catcher
        self.fielders = frame.pitching_team.fielders
        self.umpire = self.game.umpire
        self.pitches = []
        self.throw = None
        self.true_call = None  # But can't there be multiple true calls?
        # Blank count to start
        self.balls = self.strikes = 0
        self.count = 00
        # Modified below
        self.resolved = False
        self.result = None

        print "1B: {}, 2B: {}, 3B: {}, AB: {}".format(frame.on_first, frame.on_second, frame.on_third, self.batter)

    def enact(self):
        assert not self.resolved, "Call to enact() of already resolved AtBat."
        while not self.resolved:
            self.count = COUNTS[(self.balls, self.strikes)]
            # Fielders and baserunners get in position
            for player in self.fielders + self.frame.baserunners + [self.batter]:
                player.get_in_position(at_bat=self)
            # Pitcher prepares delivery
            self.pitcher.decide_pitch(at_bat=self)
            # The pitch...
            pitch = self.pitcher.pitch(at_bat=self)
            self.batter.decide_whether_to_swing(pitch)
            if not self.batter.will_swing:
                if not pitch.bean:
                    # Catcher attempts to receive pitch
                    pitch.caught = self.catcher.receive_pitch(pitch)
                    # Umpire makes his call
                    pitch.call = pitch.would_be_call
                    if pitch.call == "Strike":
                        Strike(pitch=pitch, looking=True)
                    elif pitch.call == "Ball":
                        Ball(pitch=pitch)
                elif pitch.bean:
                    pass  # Handled automatically
            # The swing...
            elif self.batter.will_swing:
                self.batter.decide_swing(pitch)
                swing = self.batter.swing(pitch)
                if not swing.contact:
                    # Swing and a miss!
                    Strike(pitch=pitch, looking=False)
                elif swing.foul_tip:
                    foul_tip = swing.result
                    if self.catcher.receive_foul_tip():
                        Strike(pitch=pitch, looking=False, foul_tip=foul_tip)
                    else:
                        FoulBall(batted_ball=foul_tip)
                elif swing.contact:
                    # Contact is made
                    batted_ball = swing.result
                    self.throw = None
                    # Fielders read the batted ball and decide immediate goals
                    batted_ball.get_read_by_fielders()
                    for fielder in self.fielders:
                        fielder.decide_immediate_goal(batted_ball=batted_ball)
                    # for baserunner in self.frame.baserunners:
                    #    baserunner.decide_immediate_goal(batted_ball=batted_ball)
                    for _ in xrange(4):
                        batted_ball.time_since_contact += 0.1
                        # While defensive players are reading the ball, the ball
                        # starts moving and the batter starts running to first
                        # (since players have a flat-rate home-to-first speed,
                        # the delay dut to their follow-through, etc., is already
                        # factored in)
                        batted_ball.move()
                        self.batter.baserun(batted_ball=batted_ball)
                    while not batted_ball.dead:
                        batted_ball.time_since_contact += 0.1
                        if not batted_ball.fielded_by:
                            batted_ball.move()
                        if self.throw:
                            self.throw.move()
                        for baserunner in self.frame.baserunners + [self.batter]:
                            if not baserunner.safely_on_base and not baserunner.out:
                                baserunner.baserun(batted_ball=batted_ball)
                            elif baserunner.safely_home:
                                Run(frame=self.frame, runner=baserunner, batted_in_by=self.batter)
                                batted_ball.running_to_home = None
                        for fielder in self.fielders:
                            if not fielder.at_goal:
                                fielder.act(batted_ball=batted_ball)
                        # ball hasn't been fielded and there's a player with a chance
                        if not batted_ball.fielded_by and batted_ball.fielder_with_chance:
                            batted_ball.fielder_with_chance.field_ball(batted_ball=batted_ball)
                            # if not batted_ball.fielded_by:
                                # print "Error! [Difficulty: {}]".format(batted_ball.fielding_difficulty)
                        if batted_ball.fielded_by and not batted_ball.fielded_by.ready_to_throw:
                            batted_ball.fielded_by.decide_throw(batted_ball=batted_ball)
                        if not self.throw and batted_ball.fielded_by and batted_ball.fielded_by.ready_to_throw:
                            self.throw = batted_ball.fielded_by.throw(batted_ball=batted_ball)
                        if self.throw and self.throw.reached_target and not self.throw.resolved:
                            self.throw.resolved = True
                            if self.throw.runner:
                                if not self.throw.runner.safely_on_base:
                                    self.true_call = "Out"
                                    if (self.throw.runner is batted_ball.running_to_first and
                                            self.throw.runner.percent_to_base > 0.9):
                                        print "-- It's a close one at {}! Umpire {} will make the call...".format(
                                            self.throw.base, self.umpire.name
                                        )
                                        # If it's close, umpire could potentially get it wrong
                                        call = self.umpire.call_play_at_first(baserunner=self.throw.runner,
                                                                              throw=self.throw)
                                    else:
                                        call = self.true_call
                                    if call == "Out":
                                        ForceOut(at_bat=self, baserunner=self.throw.runner, base=self.throw.base,
                                                 true_call=self.true_call, forced_by=self.throw.thrown_to,
                                                 assisted_by=[self.throw.thrown_by])
                                    elif call == "Safe":
                                        # if self.batter is batted_ball.running_to_first:
                                        #     hit = Single(batted_ball=batted_ball, true_call=true_call)
                                        # elif self.batter is batted_ball.running_to_second:
                                        #     hit = Double(batted_ball=batted_ball, true_call=true_call)
                                        # hit.beat_throw_by = -0.1
                                        pass
                                elif self.throw.runner.safely_on_base and batted_ball.landed:
                                    self.true_call = "Safe"
                                    if (self.throw.runner is batted_ball.running_to_first and
                                            self.throw.percent_to_target > 0.9):
                                        print "-- It's a close one at {}! Umpire {} will make the call...".format(
                                            self.throw.base, self.umpire.name
                                        )
                                        # If it's close, umpire could potentially get it wrong
                                        call = self.umpire.call_play_at_first(baserunner=self.batter, throw=self.throw)
                                    else:
                                        call = self.true_call
                                    if call == "Safe":
                                        # if self.throw:
                                        #     beat_throw_by = 0.0
                                        #     while not self.throw.reached_target:
                                        #         self.throw.move()
                                        #         beat_throw_by += 0.1
                                        #     hit.beat_throw_by = beat_throw_by
                                        pass
                                    elif call == "Out":
                                        ForceOut(at_bat=self, baserunner=self.batter, base=self.throw.base,
                                                 true_call=self.true_call, forced_by=self.throw.thrown_to,
                                                 assisted_by=[self.throw.thrown_by])
                            elif not self.throw.runner:
                                # print "\n\nThrow is to pitcher or not in pursuit of an out, so batted ball marked dead."
                                pass
                        self.umpire.officiate(batted_ball=batted_ball)
                        if all(b.safely_on_base or b.out for b in self.frame.baserunners + [self.batter]):
                            batted_ball.dead = True
                    # Once batted ball is dead (indicated by this indent), check for whether a hit was made
                    if not self.result and self.batter.safely_on_base:
                        if not self.true_call:
                            self.true_call = "WTF?"
                        if (self.batter is batted_ball.running_to_first or
                                self.batter is batted_ball.retreating_to_first):
                            Single(batted_ball=batted_ball, true_call=self.true_call)
                        elif (self.batter is batted_ball.running_to_second or
                                self.batter is batted_ball.retreating_to_second):
                            Double(batted_ball=batted_ball, true_call=self.true_call)
                        elif (self.batter is batted_ball.running_to_third or
                                self.batter is batted_ball.retreating_to_third):
                            Triple(batted_ball=batted_ball, true_call=self.true_call)
                    # Survey for which bases are now occupied and by whom
                    if batted_ball.running_to_third and batted_ball.running_to_third.safely_on_base:
                        self.frame.on_third = batted_ball.running_to_third
                    elif batted_ball.retreating_to_third and batted_ball.retreating_to_third.safely_on_base:
                        self.frame.on_third = batted_ball.retreating_to_third
                    else:
                        self.frame.on_third = None
                    if batted_ball.running_to_second and batted_ball.running_to_second.safely_on_base:
                        self.frame.on_second = batted_ball.running_to_second
                    elif batted_ball.retreating_to_second and batted_ball.retreating_to_second.safely_on_base:
                        self.frame.on_second = batted_ball.retreating_to_second
                    else:
                        self.frame.on_second = None
                    if batted_ball.running_to_first and batted_ball.running_to_first.safely_on_base:
                        self.frame.on_first = batted_ball.running_to_first
                    elif batted_ball.retreating_to_first and batted_ball.retreating_to_first.safely_on_base:
                        self.frame.on_first = batted_ball.retreating_to_first
                    else:
                        self.frame.on_first = None
                    # TODO immediately, this, tagouts, tag-ups, etc.

    def draw_playing_field(self):
        import turtle
        self.turtle = turtle
        turtle.setworldcoordinates(-450, -450, 450, 450)
        turtle.ht()
        turtle.tracer(10000)
        turtle.penup()
        turtle.goto(-226, 226)
        turtle.pendown()
        h, k = 226, 400  # Our vertex is the center-field wall
        a = -0.0034
        for x in xrange(0, 453):
            y = (a * (x - h)**2) + k
            turtle.goto(x-226, y)
        turtle.goto(0, -60)
        turtle.goto(-226, 226)
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.dot(3)
        turtle.goto(63.5, 63.5)
        turtle.dot(3)
        turtle.goto(0, 127)
        turtle.dot(3)
        turtle.goto(-63.5, 63.5)
        turtle.dot(3)
        turtle.goto(0, 0)
        turtle.goto(226, 226)
        turtle.goto(0, 0)
        turtle.goto(-226, 226)
        turtle.penup()
        for f in self.fielders:
            f.get_in_position(at_bat=self)
            turtle.goto(f.location)
            turtle.pendown()
            turtle.color("purple")
            turtle.dot(2)
            turtle.penup()
        for b in self.frame.baserunners:
            b.get_in_position(at_bat=self)
            turtle.goto(b.location)
            turtle.pendown()
            turtle.color("blue")
            turtle.dot(2)
            turtle.penup()
        turtle.update()

    def new_test(self, pitch_coords=None, count=32, power=0.8, uf=None):
        import time
        self.turtle.clearscreen()
        self.draw_playing_field()
        p = self.pitcher
        b = self.batter
        c = self.catcher
        if count is None:
            count = random.choice((00, 01, 02,
                               10, 11, 12,
                               20, 21, 22,
                               30, 31, 32))
        if not self.pitches:
            count = 00
        self.count = count
        contact = False
        while not contact:
            for fielder in self.fielders:
                fielder.get_in_position(at_bat=self)
            p.decide_pitch(at_bat=self)
            if pitch_coords:
                p.intended_x, p.intended_y = pitch_coords
            pitch = p.pitch(at_bat=self)
            b.decide_whether_to_swing(pitch)
            if not b.will_swing:
                pitch.call = pitch.would_be_call
            elif b.will_swing:
                b.decide_swing(pitch)
                b.power = power
                if uf:
                    b.incline = uf
                swing = b.swing(pitch)
                contact = swing.contact
                if contact:
                    print "\n\tThe ball is hit!\n"
                    bb = swing.result
                    turtle = self.turtle
                    turtle.penup()
                    time_since_contact = 0.0
                    for fielder in self.fielders:
                        fielder.decide_immediate_goal(batted_ball=bb)
                    for i in xrange(4):
                        time_since_contact += 0.1
                        bb.batter.baserun(bb)
                        print "Time: {}".format(time_since_contact)
                        bb.act(time_since_contact=time_since_contact)
                        turtle.goto(bb.location)
                        if bb.height < 8.5:
                            turtle.color("green")
                        else:
                            turtle.color("red")
                        turtle.dot(2)
                        turtle.update()
                        print '\n'
                        if bb.height <= 0 and not bb.stopped:
                            print "\t\tBOUNCE"
                        time.sleep(0.03)
                    fielding_chance_resolved = False
                    while not fielding_chance_resolved:
                        time_since_contact += 0.1
                        bb.batter.baserun(bb)
                        print "Time: {}".format(time_since_contact)
                        bb.act(time_since_contact=time_since_contact)
                        print "Height: {}".format(round(bb.height, 2))
                        print "Vel: {}".format(round(bb.speed, 2))
                        print "Baserunner %: {}".format(round(bb.batter.percent_to_base, 2))
                        turtle.goto(bb.location)
                        if bb.height < 8.5:
                            turtle.color("green")
                        else:
                            turtle.color("red")
                        if bb.height <= 0 and not bb.stopped:
                            print "\t\tBOUNCE"
                        turtle.dot(2)
                        turtle.update()
                        for f in self.fielders:
                            f.act(batted_ball=bb)
                            turtle.goto(f.location)
                            if not f.at_goal:
                                turtle.color("purple")
                            else:
                                turtle.color("orange")
                            turtle.dot(2)
                            turtle.update()
                        print '\n'
                        time.sleep(0.03)
                        # Check if ball has left playing field
                        if bb.left_playing_field:
                            print "\nBall has left the playing field."
                            fielding_chance_resolved = True
                        # Check if ball has landed foul
                        elif bb.landed_foul:
                            print "\nFoul ball."
                            fielding_chance_resolved = True
                        # Check if ball rolled foul
                        elif bb.landed and bb.in_foul_territory:
                            if bb.passed_first_or_third_base or bb.touched_by_fielder:
                                print "\nFoul ball."
                                fielding_chance_resolved = True
                        # Potentially simulate a fielding attempt
                        elif (bb.obligated_fielder.at_goal and
                                bb.location == bb.obligated_fielder.immediate_goal[:2]):
                            bb.obligated_fielder.field_ball(batted_ball=bb)
                            print "Difficulty: {}".format(round(bb.fielding_difficulty, 3))
                            if bb.fielded_by:
                                if not bb.landed:
                                    print "\nOut! Caught in flight."
                                    fielding_chance_resolved = True
                                else:
                                    print "\nGround ball cleanly fielded."
                                    fielding_chance_resolved = True
                                    bb.obligated_fielder.decide_throw(bb)
                                    throw = bb.obligated_fielder.throw()
                                    while not throw.reached_target and not bb.batter.safely_on_base:
                                        time_since_contact += 0.1
                                        bb.time_since_contact += 0.1
                                        print "Time: {}".format(time_since_contact)
                                        bb.batter.baserun(bb)
                                        print "Baserunner %: {}".format(round(bb.batter.percent_to_base, 2))
                                        throw.move()
                                        print "Throw %: {}".format(round(throw.percent_to_target, 2))
                                        if bb.batter.safely_on_base and throw.reached_target:
                                            print "Tie goes to the runner - Safe!"
                                        elif bb.batter.safely_on_base:
                                            print "Safe!"
                                        elif throw.reached_target:
                                            print "Force out!"
                            elif not bb.fielded:
                                print "ERROR!"
                                fielding_chance_resolved = True
                    return bb