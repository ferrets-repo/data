from PyCurve.vasicek import Vasicek

vasicek_model = Vasicek(0.02, 0.04, 0.001, -0.004, 50, 30 / 365)
simulation = vasicek_model.simulate_paths(2000) #Return a Simulation and then we can apply Simulation Methods
#simulation.plot_yield_curve()
simulation.plot_model()