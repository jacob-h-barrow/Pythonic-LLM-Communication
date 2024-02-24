from dataclasses import dataclass

@dataclass(frozen=True)
class IPv4_Intel:
    def __init__(self, ipAddr, harmless, total, threshold):
        self.ipAddr = ipAddr
        self.harmless = harmless
        self.total = total
        self.threshold = threshold
        
    def score(self):
        return (self.harmless / self.total) * 100

    def isMalicious(self):
        return self.score() < self.threshold

    def malicious(self):
        if self.isMalicious():
            return True
        return False

    def __str__(self):
        return f'VirusTotal polled the community regarding {self.ipAddr} and got {self.total} votes, but only {self.harmless} harmless votes. According to the threshold, {self.threshold}, it is malicious: {self.malicious()}'

    # 1/Score because we want the bad ipAddrs first... so a higher score is lower and heappop'd first
    def __lt__(self, nxt):
        return (1 / self.score()) < (1 / nxt.score())
