import covasim as cv
import numpy as np


def example_estimate_prob():
    import matplotlib.pyplot as plt

    # check single day estimation campaign:
    duration, coverage = (1, 0.3)
    p = cv.historical_vaccinate_prob.estimate_prob(duration=duration, coverage=coverage)
    assert(np.isclose(p, coverage))
    print('single day campaign:', coverage, '\simeq', p)

    # plot campaign coverages as a function of daily probability and campaign duration
    durations = np.arange(1, 60)
    probs = [0.0008, 0.008, 0.08, 0.8]
    plt.figure()
    for ix, prob in enumerate(probs):
        coverage = cv.historical_vaccinate_prob.NB_cdf(durations-1, 1 - prob)
        plt.plot(durations, coverage, label=prob)
    plt.legend()
    plt.xlabel('Duration of Campaign')
    plt.ylabel('Fraction of population vaccinated')
    plt.show()


def example1():
    # length of our base campaign
    duration = 30
    # estimate per-day probability needed for a coverage of 30%
    prob = cv.historical_vaccinate_prob.estimate_prob(duration=duration, coverage=0.30)
    print('using per-day probability of ', prob)

    pfizer = cv.historical_vaccinate_prob(vaccine='pfizer', days=np.arange(-duration, 0), prob=prob)
    sim = cv.Sim(interventions=pfizer, use_waning=True)

    sim.run()

    to_plot = cv.get_default_plots(kind='sim')
    to_plot['Total counts'] += ['cum_vaccinated']
    to_plot['Daily counts'] += ['new_vaccinations']
    sim.plot(to_plot=to_plot)


def example2():
    pars = {'use_waning': True}
    variants = [cv.variant('b117', days=30, n_imports=10)]
    sim = cv.Sim(pars=pars, variants=variants)

    # length of our base campaign
    duration = 30
    # estimate per-day probability needed for a coverage of 30%
    prob = cv.historical_vaccinate_prob.estimate_prob(duration=duration, coverage=0.30)
    print('using per-day probability of ', prob)

    # estimate per-day probability needed for a coverage of 30%
    prob2 = cv.historical_vaccinate_prob.estimate_prob(duration=2*duration, coverage=0.30)

    scenarios = {
        'base':{
            'name': 'baseline',
            'pars': {}
        },
        'scen1':{
            'name': 'historical_vaccinate',
            'pars': {
                'interventions':[cv.historical_vaccinate_prob(vaccine='pfizer', days=np.arange(-duration, 0), prob=prob)]
            }
        },
        'scen2': {
            'name': 'vaccinate',
            'pars': {
                'interventions': [cv.vaccinate_prob(vaccine='pfizer',days=np.arange(0, 30), prob=prob)]
            }
        },
        'scen3': {
            'name': 'historical_vaccinate into sim',
            'pars': {
                'interventions': [cv.historical_vaccinate_prob(vaccine='pfizer', days=np.arange(-30, 30), prob=prob2)]
            }
        },
    }

    scens = cv.Scenarios(sim=sim, scenarios=scenarios)

    scens.run()

    scens.plot()

def example3():
    pars = {'use_waning': True}
    variants = [cv.variant('b117', days=30, n_imports=10)]
    sim = cv.Sim(pars=pars, variants=variants)

    # length of our base campaign
    duration = 30
    # estimate per-day probability needed for a coverage of 30%
    prob = cv.historical_vaccinate_prob.estimate_prob(duration=duration, coverage=0.30)
    print('using per-day probability of ', prob)

    scenarios = {
        'scen1':{
            'name': 'both doses',
            'pars': {
                'interventions':[cv.historical_vaccinate_prob(vaccine='pfizer', days=np.arange(-duration, 0), prob=prob)]
            }
        },
        'scen3': {
            'name': 'first dose only',
            'pars': {
                'interventions': [cv.historical_vaccinate_prob(vaccine='pfizer', days=np.arange(-duration, 0), prob=prob, compliance=[1.0, 0.0])]
            }
        },
    }

    scens = cv.Scenarios(sim=sim, scenarios=scenarios)
    scens.run()
    to_plot = cv.get_default_plots(kind='scenarios')
    to_plot.pop(2)
    to_plot.update({'Cumulative vaccinations': ['cum_vaccinated', 'cum_vaccinations']})
    scens.plot(to_plot=to_plot)


def examplew0():
    cv.Sim(use_waning=True, interventions=[cv.historical_wave(120, 0.05)]).run().plot()


def examplew1():
    # run single sim
    pars = {'use_waning': True}
    variants = [cv.variant('b117', days=30, n_imports=10)]
    sim = cv.Sim(pars=pars, variants=variants)
    sim['interventions'] += [cv.historical_wave(prob=0.05, day_prior=150), cv.historical_wave(prob=0.05, day_prior=50)]
    sim.run()
    # sim.plot();
    sim.plot('variants')


def examplew2():
    pars = {'use_waning': True}
    variants = [cv.variant('b117', days=30, n_imports=10)]
    sim = cv.Sim(pars=pars, variants=variants)

    scenarios = {
        # 'base':{
        #     'name': 'baseline',
        #     'pars': {}
        # },
        'scen1':{
            'name': '1 wave',
            'pars': {
                'interventions':[cv.historical_wave(prob=0.10, day_prior=50)]
            }
        },
        'scen2': {
            'name': '2 waves',
            'pars': {
                'interventions': [cv.historical_wave(prob=0.05, day_prior=150),
                                  cv.historical_wave(prob=0.05, day_prior=50)]
            }
        }
    }

    metapars = cv.make_metapars()
    metapars.update({'n_runs':3})
    scens = cv.Scenarios(sim=sim, scenarios=scenarios, metapars=metapars)

    scens.run()

    scens.plot()

def examplep0():
    intv = cv.prior_immunity(vaccine='pfizer', days=[-30], prob=0.7)
    cv.Sim(pars={'use_waning':True}, interventions=intv).run().plot()


def examplep1():
    intv = cv.prior_immunity(120, 0.05)
    cv.Sim(pars={'use_waning':True}, interventions=intv).run().plot()


if __name__ == "__main__":

    # ## PRIOR IMMUNITY EXAMPLE
    # # use prior_immunity to add historical vaccination
    # examplep0()
    #
    # # use prior_immunity to add historical_wave
    # examplep1()

    # ## VACCINATION EXAMPLES
    #
    # # single vaccine campaign example
    # example1()
    #
    # # compare vaccinate and historical vaccinate
    # example2()
    # compare vaccinate and historical vaccinate
    example3()
    #
    # # examples using estimate_prob
    # example_estimate_prob()

    ## PREVIOUS WAVE EXAMPLES
    # # basic example
    # examplew0()
    #
    # # single vaccination example
    # examplew1()
    #
    # # multi-wave comparison
    # examplew2()
