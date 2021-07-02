# AI-Flappy_Bird with Python

An AI implementation to play Flappy Bird

## Tools used

    IDE: Pycharm Community - 2021 1.2
    Language: Python 3.9
    
## About
This project used genetic algorithm to train an AI to play Tetris.

You may need basic knowledge about genetic algorithm to get this up and running to your liking.

## Installation
You will need the following packages installed to get this project running:
* pygame 
* numpy
* Neat pyhton
  
      pip install pygame
      
      pip install neat-python

## Usage
### Running and Testing:

- Open config.txt
- Modify the variables in the following block 
  

        pop_size              = 20       #number of birds in one gen
        # node activation options
        activation_default      = tanh     # can change to another activation func( sigmoid,relu)
        activation_options      = tanh  # can change to another activation func( sigmoid,relu)
> for maximum number of generation can learn, you can change in Flappy.py, in def run(config_path)
> 
>      winner = population.run(main, 50) #change whatever number you want
> 
- Run Flappy.py
- When the trainning ends you'll receive similar output
  best solutions is the weights you have trained and looking for:
        
        ****** Running generation 0 ****** 

      Population's average fitness: 3.55500 stdev: 1.31091
      Best fitness: 6.40000 - size: (1, 3) - species 1 - id 11
      Average adjusted fitness: 0.306
      Mean genetic distance 0.919, standard deviation 0.354
      Population of 20 members in 1 species:
      ID   age  size  fitness  adj fit  stag
      ====  ===  ====  =======  =======  ====
      1    0    20      6.4    0.306     0
      Total extinctions: 0
      Generation time: 2.568 sec

## Contributors

- Nguyễn Trần Hoàng Hiếu 18520054
- Nguyễn Đức Chiến       18520528


## Credits
[NEAT Flappy Bird](https://github.com/techwithtim/NEAT-Flappy-Bird)

[Genetic algorithm basic](https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6)

[Near Perfect Tetris AI](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/)
