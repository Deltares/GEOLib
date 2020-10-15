from enum import IntEnum


class ProbabilisticCalculationType(IntEnum):
    SettlementsDeterministic = -1
    BandWidthOfSettlementsFOSM = 0
    ProbabilityOfFailureFORM = 1
    BandWidthAndProbabilityOfFailureMonteCarlo = 2
