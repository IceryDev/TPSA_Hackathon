# Optimal Battery Placement for Renewable Energy Integration

A machine learning and optimization-based approach to determine optimal battery storage placement in electrical grids to minimize renewable energy curtailment.

## Project Overview

This project uses a **Genetic Algorithm** combined with **PyPSA (Python for Power System Analysis)** network optimization to identify the most effective location and configuration for deploying battery storage systems in power grids. The goal is to maximize the utilization of renewable energy (particularly wind) by reducing curtailment (wasted renewable energy).

## Problem Statement

Modern electrical grids with high penetration of renewable energy sources (wind, solar) face significant challenges:
- **Curtailment**: Renewable energy generation often exceeds demand, forcing operators to waste excess energy
- **Energy Storage**: Battery storage can absorb surplus energy and dispatch it when needed
- **Placement Optimization**: The physical location and connectivity of the battery directly impact its effectiveness

This project addresses the question: *Where should a battery be placed, and how many grid connections should it have, to maximize renewable energy utilization?*

## Technical Approach

### 1. **Genetic Algorithm (GA)**
The project employs a genetic algorithm to search the solution space efficiently:
- **Population**: Multiple candidate locations (lon, lat pairs) on land
- **Fitness Function**: Percentage of renewable curtailment reduction achieved
- **Operators**:
  - **Selection**: Elite selection (carry top performers forward)
  - **Crossover**: Blend parent coordinates to create offspring
  - **Mutation**: Gaussian perturbation (~15 km standard deviation)
- **Termination**: Fixed number of generations

### 2. **PyPSA Network Optimization**
For each candidate location and connection count (k), the algorithm:
1. Adds a new bus and battery storage unit at the candidate location
2. Creates potential transmission lines to the k nearest buses at the target voltage level
3. Runs optimization to:
   - **First pass**: Rank connections by economic preference
   - **Second pass**: Re-optimize with only top k connections
4. Measures the resulting renewable curtailment reduction

### 3. **Candidate Elimination Strategy**
- Only evaluate locations on land (using Cartopy/Natural Earth data)
- Focus on buses at the same voltage level as the new battery (avoids transformer requirements)
- Search within a geographic bounding box derived from existing network topology

### 4. **Time Complexity**
**O(G·P·K·S)** where:
- **G**: Number of generations (default: 5)
- **P**: Population size (default: 10)
- **K**: Connection counts to test (default: [1,2,3,4,5])
- **S**: Solver time per network optimization

Typical execution: ~9 minutes for 500 total optimization runs

## Configuration Parameters

```python
# Genetic Algorithm Settings
POP_SIZE = 10          # Population size
GENERATIONS = 5        # Number of generations
ELITE_SIZE = 3         # Elite members carried forward
MUTATION_STD = 0.15    # Mutation standard deviation (degrees, ~15km)

# Network Location
x, y = -8.5, 54.5      # Initial coordinates
new_bus_v_nom = 110    # Voltage level (kV)

# Connection Analysis
k_list = [1, 2, 3, 4, 5]  # Connection counts to evaluate

# Battery Parameters
p_nom_max = 2_000      # Maximum power capacity (MW)
capital_cost = 75_000  # Annual cost (€/MW)
max_hours = 4          # Energy storage duration (hours)
efficiency = 0.95      # Round-trip efficiency

# Transmission Line Cost
line_cost_per_mw_km = 300  # €/(MW·km)
x_per_km = 0.35            # Reactance (ohm/km)
r_per_km = 0.12            # Resistance (ohm/km)

# Curtailment Penalty
curtailment_penalty = 100  # €/MWh (encourages waste reduction)
```

## Key Functions

### Utility Functions

- **`total_curtailment_mwh(network, renewable_carriers)`**: Calculates total renewable energy curtailment in MWh
- **`haversine_km(lon0, lat0, lon1, lat1)`**: Computes great-circle distance between two points
- **`surplus_waste_reduction_pct(network, curtailment_before, curtailment_after)`**: Calculates percentage of curtailment avoided
- **`is_on_land(lon, lat)`**: Validates candidate location is not in the ocean

### Core Algorithm

- **`random_land_point()`**: Generates random coordinates on land within the search box
- **`evaluate_location(cand_x, cand_y)`**: Evaluates a candidate location across all k values
- **Genetic Algorithm Loop**: Population generation, scoring, elite selection, and reproduction

## Usage

### Prerequisites

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Running the Analysis

1. **Prepare network data**: Place PyPSA network files (.nc format) in the `networks/` directory
2. **Configure parameters**: Edit the configuration section in the notebook
3. **Run the notebook**: Execute cells sequentially in Jupyter

Example output:
```
Generation 0: best fitness so far = 6.234% at (-7.9234, 54.5123) with k=3
Generation 1: best fitness so far = 7.192% at (-8.1456, 54.6234) with k=4
...
GA result: best location = (-8.0911, 54.6080), k=5, fitness = 7.190%

Optimal battery placement solution
======================================
Connection count (K):              5
Selected location (longitude):     -8.0911°
Selected location (latitude):      54.6080°
Curtailment before installation:   5,602.35 MWh
Curtailment after installation:    1,886.77 MWh
Renewable waste reduction:         7.19%
Battery energy capacity:           1,299.40 MWh
```

## Visualizations

The project generates a network map showing:
- **Blue nodes**: Demand buses (loads)
- **Orange nodes**: Newly placed battery storage
- **Green nodes**: Wind power generators
- **Red nodes**: Other power sources (fossil fuel, hydro, etc.)
- **Lines**: Transmission connections, including new lines from the battery

## Input Data

The project works with PyPSA network files containing:
- **Buses**: Grid nodes with demand/supply
- **Generators**: Power sources (wind, solar, fossil fuels)
- **Loads**: Energy demand
- **Lines**: Transmission infrastructure
- **Time series data**: Hourly profiles for generation and demand

### Example Scenarios
- `SV2024_north-west.nc`: Summer, 2024 baseline
- `WP2024_north-west.nc`: Winter peak, 2024
- `SV2033_north-west.nc`: Summer, 2033 forecast
- `WP2033_north-west.nc`: Winter peak, 2033 forecast

## Output Results

For the optimal solution, the project reports:
- **Optimal location**: Geographic coordinates (latitude, longitude)
- **Connection count (K)**: Number of transmission lines to connect
- **Battery capacity**: Optimal power (MW) and energy (MWh) sizing
- **Curtailment reduction**: MWh and percentage reduction in wasted renewable energy
- **Dispatch reduction**: Percentage change in dispatch-down penalties

## Dependencies

- **PyPSA**: Power system analysis and optimization
- **HiGHS**: Linear programming solver
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Cartopy**: Visualization and geospatial data
- **Shapely**: Geometric operations (land detection)
- **NetworkX**: Network algorithms
- **GeoPandas**: Geographic data analysis

## References

- PyPSA Documentation: https://pypsa.io/
- Natural Earth Data: https://www.naturalearthdata.com/
- Cartopy: https://scitools.org.uk/cartopy/