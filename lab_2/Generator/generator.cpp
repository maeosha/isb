#include <iostream>
#include <random>

void get_pseudorandom_sequence(){
    /*
    *Generating a pseudorandom bit sequence
    */
    std::random_device rd;
    std::mt19937 engine;
    engine.seed(rd());

    std::uniform_int_distribution dist(0, 1);

    for (size_t index = 0; index < 128; index++){
        std::cout << dist(engine);
    }
}

int main(){
    get_pseudorandom_sequence();
}