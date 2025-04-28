from perlin_noise import PerlinNoise  # Note: you'll need to import "perlin-noise" into your pyhon interpreter.
from typing import Tuple, List, Union
import numpy as np
class NoisyFunction:
    def __init__(self,size):
        noiseMaker = PerlinNoise(octaves=4)
        self.values = []

        for r in range(size):
            row = []
            for c in range(size):
                row.append(0.5*(noiseMaker([r/size,c/size])+1))
            self.values.append(row)

    def get_size(self):
        return len(self.values)

    def actual_max(self) -> Tuple[float, Tuple[int, int]]:
        temp = np.array(self.values)
        print(f"{int(np.argmax(temp)/self.get_size())=}")
        print(f"{np.argmax(temp)%self.get_size()=}")

        return np.max(temp), (int(np.argmax(temp) / self.get_size()), np.argmax(temp) % self.get_size())

    def to_ndarray(self):
        temp = np.array(self.values)
        return (temp * 256).astype(np.uint8)

    def get_value_at(self, r: int, c: int) -> float:
        return self.values[r][c]

    def get_value_at_point(self, pt: Union[Tuple[int, int], List[int]]) -> float:
        return self.get_value_at(pt[0],pt[1])