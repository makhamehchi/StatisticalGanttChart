import numpy as np

from StatGantt import box
import matplotlib.pyplot as plt
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    monthly_wages = (150000+100000+70000)/12
    timeout = 2000 # days
    three_month = box.Outcome(name='3month', probability=0.25, time=90, money=150000)
    six_months = box.Outcome(name='6month', probability=0.28, time=180, money=300000)
    twelve_months = box.Outcome(name='12month', probability=0.32, time=360, money=450000)
    tweintyfour_months = box.Outcome(name='24month', probability=0.15, time=720, money=600000)
    proto_outcomes = [three_month, six_months, twelve_months, tweintyfour_months]
    IRB_outcomes = [box.Outcome(name='easy', probability=.4, time=90, money=10000),
                    box.Outcome(name='some delay', probability=.3, time=120, money=20000),
                    box.Outcome(name='fivemonths', probability=.15, time=150, money=30000),
                    box.Outcome(name='six months', probability=.1, time=180, money=40000),
                    box.Outcome(name='never', probability=.05, time=365, money=40000)]
    clinical_outcomes = [box.Outcome(name='easy', probability=.2, time=90, money=50000),
                         box.Outcome(name='harder', probability=.4, time=180, money=100000),
                         box.Outcome(name='tough', probability=.25, time=360, money=200000),
                         box.Outcome(name='damned', probability=.1, time=720, money=300000),
                         box.Outcome(name='shitty', probability=.05, time=900, money=500000)]
    startbox = box.Box(name='start', sufficient=False, outcomes=[box.Outcome(name='start', probability=1.0, time=0, money=0)])
    startbox.output = True
    days = []
    money = []
    num_trials = 10000
    for i in range(num_trials): #number of trials
        money_counter = 0
        proto_box = box.Box(name='proto', sufficient=False, outcomes=proto_outcomes, inputboxes=[startbox])
        irb_box = box.Box(name='IRB', outcomes=IRB_outcomes, inputboxes=[startbox])
        clinical_box = box.Box(name='clinical', outcomes=clinical_outcomes, inputboxes=[proto_box, irb_box], sufficient=True)
        endbox = box.Box(name='end', sufficient=False,
                         outcomes=[box.Outcome(name='end', probability=1.0, time=0, money=0)], inputboxes=[clinical_box])

        all_boxes = [startbox, proto_box, irb_box, clinical_box, endbox]
        day_counter = 0
        while not endbox.output:
            if day_counter > timeout:
                print('time out! you are dead.')
                break
            for this_box in all_boxes:
                this_box.execute()
            day_counter += 1
        days.append(day_counter)
        for this_box in all_boxes:
            money_counter += this_box.money
        money.append(money_counter + monthly_wages*day_counter/30)
    print(days[-1])
    print(money[-1])
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle('Monte Carlo Gant simulation of seed phase- 10k Samples')
    hist, bins = np.histogram(days, 10)
    ax[0].fill_between(bins[:-1], 0, hist/num_trials)
    ax[0].set_xlabel('number of days')
    ax[0].set_ylabel('probability density')
    ax[0].set_ylim([0,0.25])

    hist, bins = np.histogram(money, 10)
    ax[1].fill_between(bins[:-1], 0, hist/num_trials)
    ax[1].set_xlabel('money needed [$]')
    ax[1].set_ylabel('probability density')
    ax[1].set_ylim([0,0.25])
    plt.show()

