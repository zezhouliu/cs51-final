from helpers import *
from graph_dictionary import *
import time, ast, os

def choose_option(g, start_end, locs, cities, e_file, solution_set, distance_set):
    """ User Interface """
    
    option = int(raw_input(" What would you like to do? \n \
    1: Run greedy \n \
    2: Run genetic \n \
    3: Run dynamic \n \
    4: View current path \n \
    5: Update number of cities \n \
    6: Update itinerary \n \
    0: Quit\n--> "))

    # run greedy
    if option == 1:
        # check that graph isn't too large
        while cities > 50:
            cities = int(raw_input("Greedy solution has a run time on the scale \
                                   of O(n-1!), so please choose a smaller value \
                                   for your cities! \n --> "))
        g, locs, start_end = generate_graph(cities)

        # start_timer
        t1 = time.time()

        # run greedy
        greedy_result = greedy(g, start_end, locs)

        # end timer
        t1 = round(time.time() - t1, 3)

        # update solution set
        solution_set = update_solution(solution_set, 0, greedy_result[0])
        distance_set = update_dist(distance_set, 0, greedy_result[1])

        # record solution for run-time analysis
        e_file.write("Greedy time: " + str(t1) + " for " + str(cities)
                     + " cities \n")

        print "The minimum total distance is ", greedy_result[1]
        print "Greedy algorithm took " + str(t1)+ " seconds."

    # run genetic
    elif option == 2:
        sols = []
        children = int(raw_input("How many rounds to run genetic? Please enter a \
number less than 2^25 to account for hardware limitations. \n --> "))
        print "Running... "

        # start time
        t2 = time.time()

        # generate result from tsp_genetic
        gen_result = tsp_genetic(children, sols, g, start_end, cities, locs)

        # end timer
        t2 = round(time.time() - t2, 3)

        # record solution for run-time analysis
        e_file.write("Genetic time: " + str(t2) + " for " + str(cities)
                     + " cities, " + str(children) + " crossovers \n")

        # update solution set
        solution_set = update_solution(solution_set, 1, gen_result[0])
        distance_set = update_dist(distance_set, 1, gen_result[1])
                             
        print "The best solution generated by the genetic algorithm has \
            distance of ", gen_result[1]
        print "Genetic algorithm took " + str(t2) + " seconds."

    # run dynamic
    elif option == 3:
        while cities > 25:
            cities = int(raw_input("Dynamic Programming solution takes space \
                        on the scale of O(n * 2^n) and run time of O(n^2 * 2^n) \
                        so please choose a smaller value! \n --> "))
        g, locs, start_end = generate_graph(cities)

        # start timer
        t3 = time.time()

        # dynamic result
        dynamic_result = tsp_dynamic(g)

        # end timer
        t3 = round(time.time() - t3, 3)        

        e_file.write("Dynamic, time: " + str(t3) + " for " +
                     str(cities) + " cities \n")

        # update solution set
        solution_set = update_solution(solution_set, 2, dynamic_result[0])
        distance_set = update_dist(distance_set, 2, dynamic_result[1])

        print "The minimum total distance is ", dynamic_result[1]
        print "Dynamic algorithm took " + str(t3) + " seconds."

    # print out current solutions
    elif option == 4:
        y = int(raw_input("Which solution would you like to see? \n \
                         1: greedy \n \
                         2: genetic \n \
                         3: dynamic \n --> "))
        print solution_set[y-1], distance_set[y-1]
        if((y < 1 or y > 3) or (distance_set[y - 1] == [])):
            print "Sorry, either this algorithm doesn't exist or this \
                            algorithm has not been run on the graph yet!, try again."
            choose_option(g, start_end, locs, cities, e_file, solution_set, distance_set)

        print_path(y - 1, solution_set, distance_set, start_end, cities)

    # generate new graph
    elif option == 5:
        cities = int(raw_input("How many cities should be traveled to? \
                    This will generate a new graph. \n--> "))
        g, locs, start_end = generate_graph(cities)
        solution_set = clear()
        distance_set = clear()

    # load coordinates from text file.
    elif option == 6:
        y = int(raw_input(" 1: Load coordinates from cities.txt (one per line) \n \
                2: Enter coordinates \n --> "))
        # read from file
        if y == 1:
            f = open('cities.txt', 'r')
            points = f.read().splitlines()
            locs = filter(lambda x: x != "", cities)
            for i in range(len(points)): 
                points[i] = ast.literal_eval(points[i])
            g = Graph(len(points))
            g.points = locs
            g.graph = g.generate_complete_graph()
            start_end = locs.pop()
            solution_set = clear()
            distance_set = clear()
            f.close()

        # enter coordinates
        elif y == 2:
            c = int(raw_input("How many cities will you travel to? This includes the initial city.\n--> "))
            while c < 2:
                c = int(raw_input("Please enter a number greater than 1! "))
            locations = []

            # get initial city
            x_init = int(raw_input("x-coordinate of initial city is: "))
            y_init = int(raw_input("y-coordinate of initial city is: "))
            city = (x_init, y_init)

            # get all the other cities
            for i in range(1,c):
                number = str(i + 1)
                x = int(raw_input("x-coordinate of city #"+number+" is: "))
                y = int(raw_input("y-coordinate of city #"+number+" is: "))
                locations.append((x,y))

            points = city + locations
            
            # update like everything (wipe solutions clean)
            assert (len(locations) == c-1)
            g = Graph(len(locations))
            g.points = points
            g.graph = g.generate_complete_graph()
            start_end = city
            solution_set = clear()
            distance_set = clear()
        else:
            choose_option(g, start_end, locs, cities, e_file, solution_set, distance_set)
    elif option == 0:
        e_file.close()
        return
    choose_option(g, start_end, locs, cities, e_file, solution_set, distance_set)
