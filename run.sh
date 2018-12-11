#!/usr/bin/env bash

python -m sc2ai.run_agent \
--map StalkersVsRoaches \
--load_model \
--norender \
--noepsilon \
--cuda \
--step_mul 8 \
--parallel 5 \
--gamma 0.95 \
--td_lambda 0.95 \
