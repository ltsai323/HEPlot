#include "TEfficiency.h"
#include <iostream>

int main() {
    // Example central value
    double centralValue = 5.0;

    // Confidence level (e.g., 0.683 for 68.3%)
    //double confidenceLevel = 0.683;
    double confidenceLevel = 0.95;

    double lower, upper;

    // Calculate uncertainties using Feldman-Cousins method
    TEfficiency::FeldmanCousinsInterval(centralValue, centralValue, confidenceLevel, lower, upper);

    // Print results
    std::cout << "Central Value: " << centralValue << "\n";
    std::cout << "Lower Uncertainty: " << lower << "\n";
    std::cout << "Upper Uncertainty: " << upper << "\n";

    return 0;
}
