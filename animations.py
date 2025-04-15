#import manim

class HeatMap:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.data_count = 0
        self.averages_on = []
        self.averages_off = []
        self.sums_on = [0] * x_size * y_size
        self.sums_off = [0] * x_size * y_size

    def add_data(self, bit_str, score):
        for i, bit in enumerate(bit_str):
            if bit == '1':
                self.sums_on[i] += score
            else:
                self.sums_off[i] += score 
            self.data_count += 1

    def calculate_averages(self):
        for on_sum, off_sum in zip(self.sums_on, self.sums_off):
            pass
