#
# Copyright 2013-2019 Software Radio Systems Limited
#
# This file is part of srsLTE
#
# srsLTE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# srsLTE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# A copy of the GNU Affero General Public License can be found in
# the LICENSE file in the top-level directory of this distribution
# and at http://www.gnu.org/licenses/.
#

file(GLOB SOURCES "*.cc")
add_library(srsenb_mac STATIC ${SOURCES} ${SRSENB_EXT_SOURCE})
if(BUILD_DDRL)
	target_link_libraries(srsenb_mac ops_async_agent)
else(BUILD_DDRL)
	message(STATUS "DDRL build disabled")
endif(BUILD_DDRL)
install(TARGETS srsenb_mac DESTINATION ${LIBRARY_DIR})

