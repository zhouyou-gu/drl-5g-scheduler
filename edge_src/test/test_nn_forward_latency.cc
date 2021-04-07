/*
 * Created on 2/09/19.
 * Author: Zhouyou Gu <guzhouyou@gmail.com>.
 *
 *
 */
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <chrono>

#include <torch/torch.h>

using namespace std;

#define RELU 0
#define TANH 1
#define SIGMOID 2


class LatencyTestNet : public torch::nn::Module {
public:
	LatencyTestNet(int64_t n_layer, int64_t n_node_per_layer, int64_t af_type);
	torch::Tensor no_grad_forward(torch::Tensor input);
	torch::Tensor grad_forward(torch::Tensor input);

private:
	vector<torch::nn::Linear> list_of_linear;
	int64_t m_af_type = 0;

};
LatencyTestNet::LatencyTestNet(int64_t n_layer, int64_t n_node_per_layer, int64_t af_type): torch::nn::Module()
{
	m_af_type =af_type;
	
	for (int i = 0; i < n_layer; ++i) {
		stringstream name;
		name << "fc" << i;
		torch::nn::Linear l = register_module(name.str(),torch::nn::Linear(n_node_per_layer,n_node_per_layer));
		list_of_linear.push_back(l);
	}
}
torch::Tensor LatencyTestNet::no_grad_forward(torch::Tensor input) {
	torch::NoGradGuard guard;
	for (int i = 0; i < (int) list_of_linear.size()-1; ++i) {
		if( m_af_type == RELU)
		{
			input = torch::relu(input);
		}
		else if(m_af_type== TANH){
			input = torch::tanh(input);
		}
		else if(m_af_type== SIGMOID){
			input = torch::sigmoid(input);
		}

		input = list_of_linear.at(i)->forward(input);
	}
	input = torch::tanh(input);
	return input;
}
torch::Tensor LatencyTestNet::grad_forward(torch::Tensor input) {
	for (int i = 0; i < (int) list_of_linear.size(); ++i) {
		if( m_af_type == RELU)
		{
			input = torch::relu(input);
		}
		else if(m_af_type== TANH){
			input = torch::tanh(input);
		}
		else if(m_af_type== SIGMOID){
			input = torch::sigmoid(input);
		}
		
		input = list_of_linear.at(i)->forward(input);
	}
	return input;
}
int main(){
	torch::set_num_threads(1);
	torch::DeviceType device_type;
	if (torch::cuda::is_available()) {
		device_type = torch::kCUDA;
		cout << "Agent - Cuda available" << endl;
	} else {
		device_type = torch::kCPU;
		cout << "Agent - CPU used" << endl;
	}
	torch::Device d = torch::Device(device_type);
	torch::set_num_threads(1);
	
	for (int n = 1; n<= 100; n++) {
		LatencyTestNet a (3,n*20, RELU);
		a.to(d);
		for(int t = 0; t<10000; t++){
			vector<float > input;
			for (int i = 0; i < n*20; ++i) {
				input.push_back(((float) rand() / (RAND_MAX)));
			}
			cout << n;
			auto start = chrono::high_resolution_clock::now();
	
			torch::Tensor input_t = torch::tensor(input, torch::dtype(torch::kFloat)).to(d);
			torch::Tensor out_t;
			out_t = a.no_grad_forward(input_t.detach());
	
			vector<float> out_v(out_t.data_ptr<float>(), out_t.data_ptr<float>() + out_t.numel());
	
			auto end = chrono::high_resolution_clock::now();
	
			double time_taken =
				chrono::duration_cast<chrono::nanoseconds>(end - start).count();
	
			time_taken *= 1e-9;
	
			cout << "," << fixed << time_taken << setprecision(9);
			cout << endl;
		}
	}
	
}
