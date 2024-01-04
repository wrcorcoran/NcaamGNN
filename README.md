# NcaamGNN
Hi there! Welcome to NcaamGNN.

NcaamGNN is a proprietary edge-weighted link prediction GNN model used for margin of victory for college basketball games.

Currently, the project is in the data-cleansing stage. All data has been soruced, cleaned, and it is being translated into a PyTorch Geometric graph dataset.

## Technologies Used
1. Selenium
2. Pandas
3. Numpy
4. PyTorch Geometric
5. PyTorch
6. Sci-kit Learn

## Technical Details
Each node in the graph is composed of basic information about the team. This includes: name, mascot, location, all-time championship wins, etc. Then, each edge has information about the matchup.

The edges are weighted with the margin of victory (negative if a loss). These edges also have feature vectors with statistics of each team at the time of competition. This ensures that the prediction is more focused on correlation between statistics than the teams themself (however, this is considered).

> More to come.

## Acknowledgements
1. [Bart Torvik](https://barttorvik.com/trank.php#) for the tremendous collection of NCAAM stats.
2. [Gregor Weichbrodt](https://github.com/gambolputty) for his [wikitable2csv](https://github.com/gambolputty/wikitable2csv) tool.
