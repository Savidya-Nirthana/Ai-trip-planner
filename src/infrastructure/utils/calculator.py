class Calculator:
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """ 
        Multiply two integers

        Args:
            a (int): The First Integer
            b (int): The Second Integer

        Returns:
            int: The product of a and b
        """
        return a * b

    @staticmethod
    def calculate_total(*x: float) -> float:
        """
        Calculate the total of any number of floats

        Args:
            *x (float): The numbers to sum

        Returns:
            float: The sum of the numbers
        """
        return sum(x)


    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget

        Args:
            total (float): The total budget
            days (int): The number of days

        Returns:
            float: The daily budget
        """
        return total / days if days > 0 else 0