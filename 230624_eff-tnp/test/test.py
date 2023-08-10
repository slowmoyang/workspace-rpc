with open('./Muon_Run2022E_run.txt') as stream:
    # for _ in range(20):
    #     run_range.append(stream.readline().removesuffix('\n'))
    run_range = stream.read().split('\n')
print(run_range)

