from dataclasses import dataclass

@dataclass
class Hit:
    timestamp: int
    past_five_mins: int = 1
    count: int = 1

    def update(self):
        self.count += 1

    def hits(self):
        return self.count

    def get(self):
        return self.timestamp

    # Option to change the time zone here
    def __repr__(self):
        return self.get()

    # Option to change the format for logging purposes
    def __str__(self):
        return str(self.__repr__)

class HitCounter:
    def __init__(self):
        self.hits = []
        self.length = 0

    def hit(self, timestamp: int) -> None:
        if self.length and self.hits[-1].get() == timestamp:
            self.hits[-1].update()
        else:
            self.hits.append(Hit(timestamp))
            self.length += 1

    def getHits(self, timestamp: int) -> int:
        hits = 0

        for idx in range(self.length - 1, -1, -1):
            diff = timestamp - (item := self.hits[idx]).get()
            if diff < 300 and diff >= 0:
                hits += item.hits()
            else:
                break

        return hits

