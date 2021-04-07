/*
 * Created on 12/06/19.
 * Author: Zhouyou Gu <guzhouyou@gmail.com>.
 *
 */

#ifndef LIBOPS_API_H
#define LIBOPS_API_H

#include <stdint.h>
#define MAX_NUM_RBG 25
#define MAX_NUM_PRB 128
#define MAX_NUM_CCE 128
#define MAX_NUM_LCID 32
#define MAX_NUM_LCG 4
#define MAX_NUM_HARQ 8
#define MAX_NUM_PC 22
#define MAX_NUM_UE 20

#define HARQ_MT 0 //!< HARQ is in empty state
#define HARQ_IDLE 1 //!< HARQ is waiting ACK or NACK
#define HARQ_ACK 2 //!< HARQ is acknowledged state
#define HARQ_NACK 3 //!< HARQ is negtive-acknowledged

/*!
 * @brief the info structure of PDCCH cadidate
 */
struct pc {
	uint8_t i_cce; //!< the index of the first CCE in pc
	uint8_t al;    //!< the aggregation level of pc
};

/*!
 * @brief the info structure of bearer (LCID)
 */
struct lcid{
	uint8_t lcid; //!< the logical channel id of the bearer
	uint8_t qci; //!< the QCI of the bearer
	uint32_t l_tx; //!< the queue size of the bearer
};

/*!
 * @brief the info structure of logical channel group, UL only
 */
struct lcg{
	uint32_t bsr; //!< bsr of the lcg
	uint32_t bsr_tti; //!< the tti that the bsr is reported
	uint8_t n_lcid; //!< the number of lcid in this group
	lcid lcid_list[MAX_NUM_LCID]; //!< a list of lcid information of each logical channel
};

/*!
 * @brief the info structure of DL and UL HARQ
 */
struct harq{
	uint8_t harq_id; //!< the harq id
	uint8_t harq_state; //!< the state of the harq, e.g., empty, IDLE, ACK and NACK
	uint8_t harq_tti; //!< the number of TTI that the data has waited in the harq for ACK
	uint8_t mcs; //!< the previous mcs of the replica
	uint32_t dl_rbg_mask; //!< the previous rbg mask of the replica, DL only
	uint32_t ul_rb_start; //!< the previous first RB of UL allocation, UL only
	uint32_t ul_rb_l; //!< the previous number of RB of UL allocation, UL only
	uint8_t n_tx; //!< the number of transmission that the data replica has been sent
	uint8_t max_n_tx; //!< maximum number of transmission, UL only
};

/*!
 * @brief the info structure of dl parameter of UE
 */
struct downlink_param {
	uint8_t cqi; //!< spectrum efficiency of the UE
	uint8_t n_lcid; //!< the number of active bearers of the UE
	lcid lcid_list[MAX_NUM_LCID]; //!< the information of DL logical channel of the UE
	harq harq_list[MAX_NUM_HARQ]; //!< the state af DL harqs of the UE
};

/*!
 * @brief the info structure of ul
 */
struct uplink_param {
	uint8_t cqi; //!< spectrum efficiency of the UE
	uint8_t sr; //!< the indicater of the scheduling request
	uint32_t sr_tti; //!< the tti that sr is reported
	uint32_t phr; //!< the latest power headroom report
	uint32_t phr_tti; //!< the time of latest power headroom report
	uint8_t n_lcg; //!< the number of active LCG of the UE
	lcg lcg_list[MAX_NUM_LCG]; //!< the information of LCG of the UE
	harq this_tti_harq; //!< the information of HARQ that this UE should use (harq_id = TTI%8)
};

/*!
 * @brief the info structure of UE
 */
struct ue_param {
	uint16_t rnti; //!< the RNTI of the UE
	downlink_param dl_param; //!< the downlink parameters
	uplink_param ul_param; //!< the uplink parameters
	uint8_t n_pc; //!< the number of available PDCCH candidates of the UE
	pc pc_list[MAX_NUM_PC]; //!< the list of available PDCCH candidates of the UE
};

/*!
 * @brief the info structure of PDU of bearers
 */
struct pdu {
	uint8_t lcid; //!< the LCID of the bearer
	uint32_t pdu_size; //!< the PDU size of the bearer
};

/*!
 * @brief the info structure of DL resource allocation for UE
 */
struct dl_ra{
	uint16_t rnti; //!< the RNTI of the UE that the resources is allocated to
	uint32_t rbg_mask; //!< the allocated RBG bitmask for the UE
	pc allocated_pc; //!< the allocated PC for DL DCI of the UE
	uint8_t mcs; //!< the selecetd MCS for the UE
	uint8_t harq_id; //!< the scheduled HARQ id for the UE
	uint8_t is_newtx; //!< the indicator of newtx for bearers or HARQ retx for the UE
	uint8_t n_pdu; //!< the number of the PDU scheduled for the UE, ignored if is_newtx = 0
	pdu pdu_list[MAX_NUM_LCID]; //!< the information list of PDU scheduled for the UE, ignored if is_newtx = 0
};

/*!
 * @brief the info structure of UL resource allocation of UE
 */
struct ul_ra{
	uint16_t rnti; //!< the RNTI of the UE that the DL resources is allocated to
	uint8_t harq_id; //!< the scheduled HARQ id for the UE
	uint32_t RB_start;//!< the index of the first allocated RB in uplink
	uint32_t L; //!< the number of RB allocated in uplink
	pc allocated_pc; //!< the allocated PC for UL DCI the UE
	uint8_t mcs; //!< the selecetd MCS for the UE
	uint8_t is_newtx; //!< the indicator of newtx for bearers or HARQ retx for the UE
	uint8_t is_adaptive; //!< the indicator whether this retx is a adaptive or not for the UE,, ignored if is_newtx = 1
	uint8_t tpc; //!< the transmission power control
};

/*!
 * @brief the info structure of eNB
 */
struct enb_param {
	uint32_t dl_tti; //!< the TTI of the dl transmission to be scheduled, ul_tti = dl_tti + 4
	uint16_t n_rbg; //!< the total number of RBG
	uint16_t n_ul_prb; //!< the total number of uplink prb
	uint16_t dl_re_list[MAX_NUM_RBG]; //!< the numbers of REs in every RBG in downlink
	uint16_t ul_re_list[MAX_NUM_PRB]; //!< the numbers of REs in every RB in uplink
	uint8_t dl_rb_list[MAX_NUM_RBG]; //!< the numbers of RBs in every RBG
	uint16_t n_cce; //!< the total number of CCE
	uint8_t avaiable_dl_rb_mask[MAX_NUM_RBG]; //!< the available rb mask in DL, dl rbg may been used by BCH etc.
	uint8_t avaiable_ul_rb_mask[MAX_NUM_PRB]; //!< the available rb mask in UL, ul prb may been used by RACH PUCCH etc.
};

/*!
 * @brief the input structure of the scheduler
 */
struct input {
	uint8_t n_ue; //!< the number of active UEs
	ue_param ue_list[MAX_NUM_UE]; //!< the list of information about UE
	enb_param enb; //!< the information and state of the eNB
};

/*!
 * @brief the output strucuture of the scheduler
 */
struct output {
	uint8_t n_dl_tx; //!< the number of UEs scheduled for DL
	dl_ra dl_tx[MAX_NUM_UE]; //!< the DL resource allocations for UEs
	uint8_t n_ul_tx; //!< the number of UEs scheduled for UL
	ul_ra ul_tx[MAX_NUM_UE]; //!< the UL resource allocations for UEs
};


#endif //LIBOPS_API_H