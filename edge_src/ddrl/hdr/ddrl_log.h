//
// Created on 19/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_DDRL_LOG_H
#define DDRL_DDRL_LOG_H
#include <pwd.h>
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
/// using the log object from srsLTE
#include "srslte/common/threads.h"
#include "srslte/common/log_filter.h"
#include "srslte/common/logger_file.h"
#include "srslte/common/logger_stdout.h"

#include "ddrl_util.h"

class ddrl_log{
public:
	ddrl_log(std::string file_name, bool to_std){
		m_to_std = false;
		std::string f (getenv("HOME"));
		f.append("/ddrl_log/");
		mode_t nMode = 0777;
		mkdir(f.c_str(),nMode);
		f.append(file_name);
		std::cout << "Logging " << file_name << " to " << f << std::endl;
		m_logger_file.init(f, -1);
		m_logfilefilter.init("DDRL",&m_logger_file);
		m_logfilefilter.set_level("DEBUG");
		m_stdoutfilter.init("DDRL",&m_logger_stdout);
		m_stdoutfilter.set_level("DEBUG");
	}
	void debug(const char * message, ...)  __attribute__ ((format (printf, 2, 3))) {
		char     *args_msg = NULL;
		va_list   args;
		va_start(args, message);
		if(vasprintf(&args_msg, message, args) > 0){
			if(m_to_std){
				m_stdoutfilter.debug("[%10ld] %s", TTICounter::get_current_dl_tti(), args_msg);
			}
			m_logfilefilter.debug("[%10ld] %s", TTICounter::get_current_dl_tti(), args_msg);
		}
		va_end(args);
		free(args_msg);
	}
	
	void error(const char * message, ...)  __attribute__ ((format (printf, 2, 3))) {
		char     *args_msg = NULL;
		va_list   args;
		va_start(args, message);
		if(vasprintf(&args_msg, message, args) > 0){
			if(m_to_std){
				m_stdoutfilter.error("[%10ld] %s", TTICounter::get_current_dl_tti(), args_msg);
			}
			m_logfilefilter.error("[%10ld] %s", TTICounter::get_current_dl_tti(), args_msg);
		}
		va_end(args);
		free(args_msg);
	}
	
private:
	bool m_to_std = true;
	srslte::logger_stdout m_logger_stdout;
	srslte::logger_file   m_logger_file;
	srslte::log_filter    m_stdoutfilter ;
	srslte::log_filter    m_logfilefilter ;
};
#endif //DDRL_DDRL_LOG_H
