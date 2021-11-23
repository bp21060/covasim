import numpy as np
import sciris as sc
assert sc.__version__ > '1.2.0'
import covasim as cv
import pylab as pl
 
# Define main things

# Set up a sim
base_pars = {
    'n_agents': 50_000,
    'beta': 0.015,
    'n_days': 365,
}

# Define booster
default_nab_eff = dict(
    alpha_inf      =  1.11,
    beta_inf       =  1.219,
    alpha_symp_inf = -1.06,
    beta_symp_inf  =  0.867,
    alpha_sev_symp =  0.268,
    beta_sev_symp  =  3.4
)
booster = dict(
    nab_eff=sc.dcp(default_nab_eff),
    nab_init=None,
    nab_boost=3,
    doses=1,
    interval=None,
)

# Define sequence based vaccination
def prioritize_by_age(people):
    return np.argsort(-people.age)

# Start vaccinating 100 people/day on day 30 then scale up by 100 doses/day til 65% have had a first dose
def num_doses(sim):
    if sim.t < 30:
        return 0
    elif sim.t < 50: # First doses only
        return (sim.t - 29) * 100
    elif sim.t < 55: # First and second doses
        return (sim.t-29) * 100 + (sim.t-50) * 100
    elif sim.t < 76: # Second doses only
        return (sim.t - 50) * 100
    else:
        return 0

# Now give 100 boosters a day starting from day 240
def num_boosters(sim):
    if sim.t < 240:
        return 0
    else:
        return 100

# Define the vaccine and the booster
az = cv.vaccinate_num(vaccine='az', sequence=prioritize_by_age, num_doses=num_doses)
booster_target = {'inds': lambda sim: cv.true(sim.people.vaccinations != 2), 'vals': 0} # Only give boosters to people who have had 2 doses
booster = cv.vaccinate_num(vaccine=booster, sequence=prioritize_by_age, subtarget=booster_target, num_doses=num_boosters, booster=True)

# Introduce delta on day 240 to induce a new wave
delta = cv.variant('delta', days=240, n_imports=20)

# Track doses
n_doses_baseline = []
n_doses_boosters = []

# Create sims with and without boosters
sim_baseline = cv.Sim(use_waning=True, pars=base_pars,
                      interventions=[az],
                      variants=delta,
                      label='No boosters',
                      analyzers=lambda sim: n_doses_baseline.append(sim.people.vaccinations.copy())
                      )
sim_boosters = cv.Sim(use_waning=True, pars=base_pars,
                      interventions=[az, booster],
                      variants=delta,
                      label='Boosters',
                      analyzers=lambda sim: n_doses_boosters.append(sim.people.vaccinations.copy())
                      )



def run_sims():

    sim_baseline.run()
    sim_boosters.run()

    # Create a multisim, run, and plot results
    msim = cv.MultiSim([sim_baseline, sim_boosters])
    msim.plot(to_plot=['cum_infections', 'cum_severe', 'cum_deaths','pop_nabs'])

    # Plot doses
    pl.figure()
    n_doses = np.array(n_doses_boosters)
    fully_vaccinated = (n_doses == 2).sum(axis=1)
    first_dose = (n_doses == 1).sum(axis=1)
    boosted = (n_doses > 2).sum(axis=1)
    pl.stackplot(sim_baseline.tvec, first_dose, fully_vaccinated, boosted)
    pl.legend(['First dose', 'Fully vaccinated', 'Boosted']);
    pl.show()

    pl.figure()
    n_doses = np.array(n_doses_baseline)
    fully_vaccinated = (n_doses == 2).sum(axis=1)
    first_dose = (n_doses == 1).sum(axis=1)
    boosted = (n_doses > 2).sum(axis=1)
    pl.stackplot(sim_boosters.tvec, first_dose, fully_vaccinated, boosted)
    pl.legend(['First dose', 'Fully vaccinated', 'Boosted']);
    pl.show()

    return msim


#%% Run as a script
if __name__ == '__main__':
    sc.tic()

    # Run more complex single-sim tests
    msim = run_sims()

    sc.toc()


print('Done.')

