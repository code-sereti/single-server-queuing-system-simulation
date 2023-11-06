import random
import simpy

# Constants used.
ARRIVAL_RATE = 2  # Arrival rate at which customers arrive.(2 customer per unit time)
SERVICE_RATE = 3  # Service rate at which the system serves customers.
SIMULATION_TIME = 10  # Simulation time in time units

class QueuingSystem: # Represents the queuing system itself.
    def __init__(self, env, arrival_rate, service_rate):
        self.env = env # Initialize the env
        self.queue = simpy.Resource(env, capacity=1)  # Single server.Creates a  Resource object modeling the server.
        self.arrival_rate = arrival_rate #Assigns the arrival rate parameter to the attribute.
        self.service_rate = service_rate
        

    def customer(self, name):# The method models the customer's behaviour
        arrival_time = self.env.now # Records the current simulatiion time as the customer's arrival time.
        print(f"Customer {name} arrives at {arrival_time:.2f}")#Time,name

        with self.queue.request() as request: #Initiates a request for the server self.queue
            yield request # Yield a request to allow customer to wait until the server is available

            service_start_time = self.env.now# records the current simulation time as the service time
            print(f"Customer {name} starts service at {service_start_time:.2f}")
            service_time = random.expovariate(self.service_rate)# Calculates service time by generating random numbers from exp distibutions.
            yield self.env.timeout(service_time)#  Creates a timeout event in the simulation env. The sim pauses for the duration specified by the service_time.

            service_end_time = self.env.now
            print(f"Customer {name} finishes service at {service_end_time:.2f}")
            total_time_in_system = service_end_time - arrival_time # Calculates the total time spent by the customer to be served.
            print(f"Total time in system for customer {name}: {total_time_in_system:.2f}")

def customer_generator(env, arrival_rate, queuing_system):# Function generates customers and introduces them to queuing system at specified arrival time.
    customer_id = 1 #Initalize the a variable customer_id=1  keeping track of the id assigned to the customer.
    while True:
        yield env.timeout(random.expovariate(arrival_rate))# Introduces a delay using a timeout event.The interval represents the time until the next customer arrives.
        env.process(queuing_system.customer(customer_id))# Creates a new customer by invoking the customer method. 
        customer_id += 1

# Main simulation function
def run_simulation(): # 
    env = simpy.Environment()# Manages the simulation
    queuing_system = QueuingSystem(env, ARRIVAL_RATE, SERVICE_RATE)# Creates an object, passes parrameters.
    env.process(customer_generator(env, ARRIVAL_RATE, queuing_system))# Starts the generator function as a simpy process within the env
    env.run(until=SIMULATION_TIME)# Runs until the simulation time

# Run the simulation
if __name__ == "__main__": # Ensures that 
    run_simulation()
