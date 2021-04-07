//
// Created on 24/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_DDRL_NN_H
#define DDRL_DDRL_NN_H
#include <string.h>
#include <map>

#include <torch/torch.h>

#include "nn_config.pb.h"
#include "update_weight.pb.h"
using namespace torch;
using namespace torch::nn;


class Net : public torch::nn::Module {
public:
	Net();
	bool init(ddrl::nn_config config);
	bool reset_parameters();
	Tensor forward(Tensor state);
	int status();
	
	int update_model_weight(ddrl::update_model_weight update_w);
	int update_weight(ddrl::model_weight w);
	
	static std::string get_a_nn_name(std::string name, int id){
		return name.append(std::to_string(id));
	}
	static std::pair<double,double> hidden_init(torch::nn::Linear& layer) {
		double lim = 1. / sqrt(layer->weight.sizes()[0]);
		return std::make_pair(-lim, lim);
	}

private:
	bool construct_nn();
	ddrl::nn_config m_nn_config;
	std::map<uint8_t, Functional> m_afs;
	std::map<uint8_t, Linear> m_fcs;
};


#endif //DDRL_DDRL_NN_H
