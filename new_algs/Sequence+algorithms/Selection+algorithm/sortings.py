class Sorter:
    def __init__(self, comparison_number_selection=0,
                 exchange_number_selection=0, comparison_number_quick=0,
                 exchange_number_quick=0):
        self.comparison_number_selection = comparison_number_selection
        self.exchange_number_selection = exchange_number_selection
        self.comparison_number_quick = comparison_number_quick
        self.exchange_number_quick = exchange_number_quick

    def swap(self, array, first_index, second_index):
        array[first_index], array[second_index] = array[second_index], \
                                                  array[first_index]

    def selection_sort(self, rating_array=[]):
        element_index = len(rating_array) - 1
        for i in range(0, element_index):
            max_element_index = i
            for j in range(i + 1, len(rating_array)):
                self.comparison_number_selection += 1
                if rating_array[j].rating > \
                        rating_array[max_element_index].rating:
                    max_element_index = j
            self.exchange_number_selection += 1
            self.swap(rating_array, max_element_index, i)
        return rating_array

    def quick_sort(self, height_array=[]):
        self.comparison_number_quick += 1
        if len(height_array) < 2:
            return height_array
        else:
            pivot = (height_array[0]).height
            border = 0
            for j in range(1, len(height_array)):
                self.comparison_number_quick += 1
                if (height_array[j]).height < pivot:
                    self.exchange_number_quick += 1
                    self.swap(height_array, j, border + 1)
                    border += 1
            self.exchange_number_quick += 1
            self.swap(height_array, 0, border)
            first_part = self.quick_sort(height_array[:border])
            second_part = self.quick_sort(height_array[border + 1:])
            first_part.append(height_array[border])
            return first_part + second_part
