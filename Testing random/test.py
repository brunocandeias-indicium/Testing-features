import pandas as pd

first_ = pd.read_csv("tier_1_two_phase_approach.csv")
second_ = pd.read_csv("tier_2_two_phase_approach.csv")

all_ = pd.read_csv("*.csv")

print(all_.head(5))

pd.concat([first_,second_])