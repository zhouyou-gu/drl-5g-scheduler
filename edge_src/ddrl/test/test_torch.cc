//
// Created on 23/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include <iostream>

#include <torch/torch.h>

#include "nn_config.pb.h"
#include "update_weight.pb.h"

#include "ddrl_log.h"
#include "ddrl_nn.h"

static ddrl_log this_log("test_torch.log",true);

int main(){
	uint16_t n_ue = 5;
	uint16_t n_input_per_ue = 2;
	uint16_t node_per_layer_mul =10;
	ddrl::nn_config * config =  new ddrl::nn_config;
	config->add_af_config(ddrl::nn_config::NONE);
	config->add_af_config(ddrl::nn_config::RELU);
	config->add_af_config(ddrl::nn_config::RELU);
	config->add_af_config(ddrl::nn_config::TANH);
	
	config->add_nn_arch(n_ue*n_input_per_ue);
	config->add_nn_arch(n_ue*n_input_per_ue*node_per_layer_mul);
	config->add_nn_arch(n_ue*n_input_per_ue*node_per_layer_mul);
	config->add_nn_arch(n_ue);
	
	config->set_name("actor");
	
	
	Net n;
	n.init(*config);
	n.status();
	
	ddrl::update_model_weight u;
	u.set_allocated_nn_config(config);
	u.set_n_tensor_in_model(n.parameters().size());
	
	ddrl::model_weight * w = u.add_weight();
	w->set_tensor_index(0);
	w->set_n_dim(n.parameters()[0].dim());
	
	w->set_x_index(0);
	w->set_y_index(0);
	w->set_tau(1.);
	w->set_value(8);
	
	n.update_model_weight(u);
	
	
}