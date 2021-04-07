#
# Created on 20/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
include(FindProtobuf)
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIR})
file(GLOB SOURCES "*.proto")
protobuf_generate_cpp(PROTO_SRC PROTO_HEADER ${SOURCES})
protobuf_generate_python(PROTP_PY_SRC ${SOURCES})
message(PROTO_HEADER:${PROTO_HEADER})

#add the target for generating python files
add_custom_target(proto_py_target ALL
		DEPENDS ${PROTP_PY_SRC})

#add the library for protobuf
add_library(proto ${PROTO_HEADER} ${PROTO_SRC})

#add the target for python installation after compile
foreach(f ${PROTP_PY_SRC})
	add_custom_command(TARGET proto_py_target POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E
			copy ${f} ${PROTO_PY_DIR})
endforeach()

foreach(f ${PROTP_PY_SRC})
	add_custom_command(TARGET proto_py_target POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E
			copy ${f} ${PROTO_PY_DIR_TEST})
endforeach()

add_custom_command(TARGET proto POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E
		copy $<TARGET_FILE_NAME:proto> ${PROTO_LIB_DIR}/$<TARGET_FILE_NAME:proto>)

foreach(f ${PROTO_HEADER})
	add_custom_command(TARGET proto POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E
			copy ${f} ${PROTO_LIB_DIR})
endforeach()

###(Not in use): install the header files and library in a directory
#add_custom_command(TARGET proto POST_BUILD
#		COMMAND ${CMAKE_COMMAND} -E
#		copy $<TARGET_FILE_NAME:proto> ${PROTO_LIB_DIR_TEST}/$<TARGET_FILE_NAME:proto>)
#
#foreach(f ${PROTO_HEADER})
#	add_custom_command(TARGET proto POST_BUILD
#			COMMAND ${CMAKE_COMMAND} -E
#			copy ${f} ${PROTO_LIB_DIR_TEST})
#endforeach()