//
// Created on 24/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ddrl_log.h"
#include "ddrl_nn.h"
#include <stdexcept>
#include <string.h>

using namespace torch;
using namespace torch::nn;


static ddrl_log this_log("neural_network.log",true);


Net::Net()
{
	m_nn_config.Clear();
	m_afs.clear();
	m_fcs.clear();
	reset_parameters();
}
bool Net::init(ddrl::nn_config config) {
	m_nn_config.CopyFrom(config);
	m_afs.clear();
	m_fcs.clear();
	construct_nn();
	reset_parameters();
	return true;
}
bool Net::construct_nn() {
	if (m_nn_config.nn_arch_size()<2){
		this_log.error("At least 2 layer NN is required (%d layer in config)!!\n", m_nn_config.nn_arch_size());
		throw std::invalid_argument( "At least 2 layer NN is required !!\n");
	}
	if (m_nn_config.af_config_size() != m_nn_config.nn_arch_size()){
		this_log.error("af_config size %d should equals nn_arch _size %d!!\n", m_nn_config.af_config_size(),  m_nn_config.nn_arch_size());
		throw std::invalid_argument( "af_config size should equals nn_arch _size!!\n");
	}

	for(int i = 0; i < (int) m_nn_config.af_config_size(); i++){
		if(m_nn_config.af_config(i) != ddrl::nn_config::NONE){
			if(m_nn_config.af_config(i) == ddrl::nn_config::RELU){
				this_log.debug("add af as %s\n", get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i).c_str());
				Functional temp = register_module(get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i), Functional(torch::relu));
				m_afs.insert(std::pair<uint8_t ,Functional>(i, temp));
			} else if (m_nn_config.af_config(i) == ddrl::nn_config::TANH){
				this_log.debug("add af as %s\n", get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i).c_str());
				Functional temp = register_module(get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i), Functional(torch::tanh));
				m_afs.insert(std::pair<uint8_t ,Functional>(i, temp));
			} else if (m_nn_config.af_config(i) == ddrl::nn_config::SIGMOID){
				this_log.debug("add af as %s\n", get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i).c_str());
				Functional temp = register_module(get_a_nn_name(nn_config_af_type_Name(m_nn_config.af_config(i)), i), Functional(torch::sigmoid));
				m_afs.insert(std::pair<uint8_t ,Functional>(i, temp));
			} else {
				this_log.error("af_config invalid %d %d!!\n", i , m_nn_config.af_config(i));
			}
		}
	}
	for(int x = 0; x < (int) m_nn_config.nn_arch_size()-1;x++){
		std::stringstream ss;
		ss << "fc-" << m_nn_config.nn_arch(x) << "-" << m_nn_config.nn_arch(x+1) << "-id-";
		this_log.debug("add linear as %s\n", get_a_nn_name(ss.str(),x).c_str());
		Linear temp = register_module(get_a_nn_name(ss.str(),x), Linear(m_nn_config.nn_arch(x), m_nn_config.nn_arch(x+1)));
		m_fcs.insert(std::pair<uint8_t ,Linear>(x,temp));
	}
	return true;
}
bool Net::reset_parameters(){
	if(m_fcs.empty()){
		return false;
	}
	for(auto l = m_fcs.begin(); l != m_fcs.end(); l ++){
		std::pair<double,double> params = hidden_init(l->second);
		torch::nn::init::uniform_(l->second->weight, params.first, params.second);
	}
	torch::nn::init::uniform_(m_fcs.find(m_fcs.size()-1)->second->weight, -3e-3, 3e-3);
	return true;
}
Tensor Net::forward(Tensor x) {
	for(int i = 0; i < (int) m_fcs.size(); i ++){
		if(m_afs.find(i) != m_afs.end())
			x = m_afs.find(i)->second->forward(x);
		x = m_fcs.find(i)->second->forward(x);
	}
	if(m_afs.find(m_fcs.size()) != m_afs.end())
		x = m_afs.find(m_fcs.size())->second->forward(x);
	return x;
}
int Net::status(){
	for(int i = 0; i < m_nn_config.af_config_size(); i ++){
		this_log.debug("af at %d is %s\n", i, nn_config_af_type_Name(m_nn_config.af_config(i)).c_str());
	}
	for(int i = 0; i < m_nn_config.nn_arch_size(); i ++){
		this_log.debug("nn_arch at %d is %d\n",i,m_nn_config.nn_arch(i));
	}
	std::stringstream ss;
	for(int i = 0; i < (int) m_fcs.size(); i ++){
		if(m_afs.find(i) != m_afs.end())
			ss << m_afs.find(i)->second->name() << "\n";
		ss << m_fcs.find(i)->second->name() << "\n";
	}
	if(m_afs.find(m_fcs.size()) != m_afs.end()){
		ss << m_afs.find(m_fcs.size())->second->name() << "\n";
	}
	this_log.debug("registered %s as:\n %s\n",m_nn_config.name().c_str(),ss.str().c_str());
	return 0;
}

int Net::update_model_weight(ddrl::update_model_weight update_w) {
	torch::NoGradGuard no_grad;
	this_log.debug("update_model_weight: name: %s\n",update_w.name().c_str());
	this_log.debug("update_model_weight: n_tensor_in_model: %d\n",update_w.n_tensor_in_model());
	if ((update_w.nn_config().GetTypeName() != m_nn_config.GetTypeName()) or
	    (update_w.nn_config().SerializeAsString() != m_nn_config.SerializeAsString())){
		this_log.error("update_model_weight: configuration mismatch \n update_w.nn_config: %s \n m_nn_config: %s!!\n", update_w.nn_config().DebugString().c_str(),m_nn_config.DebugString().c_str());
		throw std::invalid_argument( "configuration mismatch !!\n");
	}
	this_log.debug("update_model_weight: N weight updated: %d\n",update_w.weight_size());
	for (size_t i = 0; i < (uint64_t) update_w.weight_size(); i++) {
		auto w = update_w.weight(i);
		update_weight(w);
	}
	return 0;
}

int Net::update_weight(ddrl::model_weight w) {
	int tensor_idx = w.tensor_index();
	int tensor_dim = w.n_dim();
	
	if (parameters()[tensor_idx].dim() != tensor_dim){
		this_log.error("update_weight: tensor dim mismatch: idx:%d, local_dim:%d new_dim:%d\n",tensor_idx,(int)parameters()[tensor_idx].dim(),tensor_dim);
		throw std::invalid_argument( "tensor dim mismatch !!\n");
	}
	torch::NoGradGuard no_grad;
	int x = w.x_index();
	int y = w.y_index();
	float tau = w.tau();
	float new_value = w.value();
	this_log.debug("update_weight: tensor_idx:%d, tensor_dim:%d, x=%d, y=%d, tau=%f, new_value=%f\n",tensor_idx, tensor_dim, x, y, tau, new_value);
	if(tensor_dim == 1){
		this_log.debug("update_weight: before update value=%f\n", *parameters()[tensor_idx][x].data_ptr<float>());
		parameters()[tensor_idx][x].copy_((1-tau) * parameters()[tensor_idx][x] +  tau * new_value);
		this_log.debug("update_weight: after  update value=%f\n",new_value);
	}
	else if(tensor_dim == 2){
		this_log.debug("update_weight: before update value=%f\n", *parameters()[tensor_idx][x][y].data_ptr<float>());
		parameters()[tensor_idx][x][y].copy_((1-tau) * parameters()[tensor_idx][x][y] +  tau * new_value);
		this_log.debug("update_weight: after  update value=%f\n",new_value);
		
	}
	else{
		this_log.error("update_weight: tensor dim not supported :%d,  <= 2 required \n",tensor_dim);
	}
	return 0;
	
	
}