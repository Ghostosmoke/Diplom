import math


class ProbabilityCalculator:
    T0 = 5

    @staticmethod
    def root(a: float, n: int) -> float:
        """Calculate nth root of a number"""
        r = math.exp(math.log(abs(a)) / n)
        return -r if a < 0 else r

    @staticmethod
    def f_ke_1(Lam0: float) -> list[float]:
        """Density function for k=1"""
        return [Lam0]

    @staticmethod
    def f_ke_2(Lam0: float, Lam1: float) -> list[float]:
        """Density function for k=2"""
        denom = Lam1 - Lam0
        return [
            Lam0 * Lam1 / denom,
            Lam0 * Lam1 / (Lam0 - Lam1)
        ]

    @staticmethod
    def f_ke_3(Lam0: float, Lam1: float, Lam2: float) -> list[float]:
        """Density function for k=3"""
        return [
            Lam0 * Lam1 * Lam2 / ((Lam1 - Lam0) * (Lam2 - Lam0)),
            Lam0 * Lam1 * Lam2 / ((Lam0 - Lam1) * (Lam2 - Lam1)),
            Lam0 * Lam1 * Lam2 / ((Lam0 - Lam2) * (Lam1 - Lam2))
        ]

    @staticmethod
    def f_ke_4(Lam0: float, Lam1: float, Lam2: float, Lam3: float) -> list[float]:
        """Density function for k=4"""
        return [
            Lam0 * Lam1 * Lam2 * Lam3 / ((Lam1 - Lam0) * (Lam2 - Lam0) * (Lam3 - Lam0)),
            Lam0 * Lam1 * Lam2 * Lam3 / ((Lam0 - Lam1) * (Lam2 - Lam1) * (Lam3 - Lam1)),
            Lam0 * Lam1 * Lam2 * Lam3 / ((Lam0 - Lam2) * (Lam1 - Lam2) * (Lam3 - Lam2)),
            Lam0 * Lam1 * Lam2 * Lam3 / ((Lam0 - Lam3) * (Lam1 - Lam3) * (Lam2 - Lam3))
        ]

    @staticmethod
    def mom1(k: int, A: list[float]) -> float:
        """Calculate mathematical expectation (mean)"""
        return sum(1 / a for a in A[:k])

    @staticmethod
    def disp(k: int, A: list[float]) -> float:
        """Calculate variance"""
        return sum(1 / (a ** 2) for a in A[:k])

    @staticmethod
    def mom1_r(k: int, A: list[float]) -> float:
        """Expected remaining time until next event"""
        if k == 1:
            Kf = ProbabilityCalculator.f_ke_1(A[0])
        elif k == 2:
            Kf = ProbabilityCalculator.f_ke_2(A[0], A[1])
        elif k == 3:
            Kf = ProbabilityCalculator.f_ke_3(A[0], A[1], A[2])
        elif k == 4:
            Kf = ProbabilityCalculator.f_ke_4(A[0], A[1], A[2], A[3])
        else:
            raise ValueError("k must be between 1 and 4")

        numerator = sum(Kf[i] / (A[i] ** 3) for i in range(k))
        return numerator / ProbabilityCalculator.mom1(k, A)

    @staticmethod
    def fun_int(k: int, A: list[float], t: float) -> float:
        """Integral distribution function"""
        if k == 1:
            Kf = ProbabilityCalculator.f_ke_1(A[0])
        elif k == 2:
            Kf = ProbabilityCalculator.f_ke_2(A[0], A[1])
        elif k == 3:
            Kf = ProbabilityCalculator.f_ke_3(A[0], A[1], A[2])
        elif k == 4:
            Kf = ProbabilityCalculator.f_ke_4(A[0], A[1], A[2], A[3])
        else:
            raise ValueError("k must be between 1 and 4")

        return 1 - sum((Kf[i] / A[i]) * math.exp(-A[i] * t) for i in range(k))

    @staticmethod
    def fun_rt0(k: int, A: list[float], t: float) -> float:
        """Probability that remaining time is less than T0"""
        if k == 1:
            Kf = ProbabilityCalculator.f_ke_1(A[0])
        elif k == 2:
            Kf = ProbabilityCalculator.f_ke_2(A[0], A[1])
        elif k == 3:
            Kf = ProbabilityCalculator.f_ke_3(A[0], A[1], A[2])
        elif k == 4:
            Kf = ProbabilityCalculator.f_ke_4(A[0], A[1], A[2], A[3])
        else:
            raise ValueError("k must be between 1 and 4")

        mom1_val = ProbabilityCalculator.mom1(k, A)
        return 1 - sum((Kf[i] / (A[i] ** 2)) * math.exp(-A[i] * t) / mom1_val for i in range(k))

    @staticmethod
    def fi_0(L: int, k: list[int], B: list[list[float]], t: float) -> float:
        """Combined probability function for all streams"""
        p = 1.0
        for j in range(L):
            A = B[j][:k[j]]
            p *= (1 - ProbabilityCalculator.fun_rt0(k[j], A, t))
        return 1 - p

    @staticmethod
    def fi(L: int, k: list[int], B: list[list[float]], t: float) -> float:
        """Combined probability function excluding first stream"""
        p = 1.0
        for j in range(1, L):
            A = B[j][:k[j]]
            p *= (1 - ProbabilityCalculator.fun_rt0(k[j], A, t))

        A_first = B[0][:k[0]]
        return 1 - p * (1 - ProbabilityCalculator.fun_int(k[0], A_first, t))

    def calculate(self, L: int, k: list[int], lam: list[list[float]]) -> dict:
        """Main calculation method"""
        # Validate inputs
        if len(k) != L or len(lam) != L:
            raise ValueError("Input arrays must match length L")

        # Calculate components
        lam1 = lam[0][:k[0]]
        mom1_r1 = self.mom1_r(k[0], lam1)
        mom1_t1 = self.mom1(k[0], lam1)

        fi_0_val = self.fi_0(L, k, lam, self.T0)
        fi_val = self.fi(L, k, lam, self.T0)

        # Final calculation
        try:
            mZ = fi_0_val * (mom1_r1 + (mom1_t1 * fi_val) / (1 - fi_val))
        except ZeroDivisionError:
            mZ = float('inf')

        return {
            'mean_delay': mZ,
            'mom1_r1': mom1_r1,
            'fi_value': fi_val
        }


# Example usage
if __name__ == "__main__":
    pc = ProbabilityCalculator()

    # Example parameters
    L = 3  # Number of streams
    k = [2, 3, 2]  # k values for each stream
    lam = [
        [0.5, 0.3, 0, 0],  # Lambdas for stream 1 (using first 2)
        [0.4, 0.2, 0.1, 0],  # Lambdas for stream 2 (using first 3)
        [0.6, 0.4, 0, 0]  # Lambdas for stream 3 (using first 2)
    ]

    results = pc.calculate(L, k, lam)
    print("Results:")
    print(f"Mean delay: {results['mean_delay']:.2f}")
    print(f"Mom1 R1: {results['mom1_r1']:.2f}")
    print(f"FI value: {results['fi_value']:.4f}")
