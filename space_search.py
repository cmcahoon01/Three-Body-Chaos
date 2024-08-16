from simulation import Simulation
from tracking import Tracker
from constants import *
import optuna


def main():
    study = optuna.create_study(direction='maximize')
    study.optimize(run_trial, n_trials=1000)
    print('Best parameters:', study.best_params)
    print('Best score:', study.best_value)


def run_trial(trial):
    # Initialize the parameters dictionary to be passed to your simulation
    parameters = {}
    # Iterate over the parameter domains and suggest values for each parameter
    for param_name, (low, high) in parameter_domains.items():
        parameters[param_name] = trial.suggest_float(param_name, low, high)

    simulation = Simulation(parameters, 50)
    tracker = Tracker(simulation)
    simulation.tracker = tracker

    simulation.run()
    score = tracker.lifetime
    return score


if __name__ == "__main__":
    main()
